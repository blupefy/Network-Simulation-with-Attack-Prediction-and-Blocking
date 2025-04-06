#!/usr/bin/env python3
"""
Integration Script for Network Simulation Environment
This script integrates all components of the network simulation system.
"""

import os
import sys
import time
import logging
import threading
import json
import argparse
import pandas as pd
import numpy as np
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.network_topology import NetworkSimulationTopology, setup_network
from src.attack_simulator import AttackSimulator
from src.defense_mechanisms import DefenseSystem, TrafficAnalyzer
from src.ml_model import NetworkAttackModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/integration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('integration')

class IntegratedSystem:
    """
    Integrated system that combines all components
    """
    
    def __init__(self, args):
        """
        Initialize the integrated system
        
        Args:
            args: Command line arguments
        """
        self.args = args
        self.net = None
        self.attack_simulator = None
        self.defense_system = None
        self.ml_model = None
        
        # Create directories if they don't exist
        for directory in ['../logs', '../data', '../results']:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        logger.info("Integrated system initialized")
    
    def setup_network(self):
        """
        Set up the network topology
        
        Returns:
            bool: True if network was set up successfully, False otherwise
        """
        try:
            # Set log level
            setLogLevel('info')
            
            # Create the topology
            topo = NetworkSimulationTopology()
            
            # Create and start the network
            self.net = Mininet(
                topo=topo,
                controller=Controller,
                switch=OVSKernelSwitch,
                link=TCLink,
                build=False,
                autoSetMacs=True
            )
            
            # Add controller
            self.net.addController('c0')
            
            # Build and start network
            self.net.build()
            self.net.start()
            
            # Configure firewall node
            firewall = self.net.get('firewall')
            firewall.cmd('sysctl -w net.ipv4.ip_forward=1')
            
            # Configure server
            server = self.net.get('server')
            server.cmd('python3 -m http.server 80 &')
            
            # Test connectivity
            logger.info("Testing network connectivity...")
            self.net.pingAll()
            
            logger.info("Network topology set up successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to set up network: {e}")
            return False
    
    def setup_attack_simulator(self):
        """
        Set up the attack simulator
        
        Returns:
            bool: True if attack simulator was set up successfully, False otherwise
        """
        try:
            # Get attacker and target nodes
            attacker1 = self.net.get('attacker1')
            server = self.net.get('server')
            
            # Create attack simulator
            self.attack_simulator = AttackSimulator(
                attacker_ip=attacker1.IP(),
                target_ip=server.IP(),
                interface=attacker1.defaultIntf().name
            )
            
            logger.info(f"Attack simulator set up successfully: {attacker1.IP()} -> {server.IP()}")
            return True
        except Exception as e:
            logger.error(f"Failed to set up attack simulator: {e}")
            return False
    
    def setup_defense_system(self):
        """
        Set up the defense system
        
        Returns:
            bool: True if defense system was set up successfully, False otherwise
        """
        try:
            # Get firewall node
            firewall = self.net.get('firewall')
            
            # Load ML model if available
            ml_model_path = self.args.ml_model if hasattr(self.args, 'ml_model') else None
            if not ml_model_path or not os.path.exists(ml_model_path):
                # Train a new model if not available
                logger.info("Training a new ML model...")
                self.ml_model = NetworkAttackModel()
                X_train, X_test, y_train, y_test = self.ml_model.generate_synthetic_data(
                    num_normal=1000, num_attack=1000
                )
                self.ml_model.train_model(X_train, y_train)
                self.ml_model.evaluate_model(X_test, y_test)
                ml_model_path = self.ml_model.save_model()
            
            # Create defense system
            self.defense_system = DefenseSystem(
                interface=firewall.defaultIntf().name,
                ml_model_path=ml_model_path
            )
            
            logger.info(f"Defense system set up successfully on {firewall.defaultIntf().name}")
            return True
        except Exception as e:
            logger.error(f"Failed to set up defense system: {e}")
            return False
    
    def run_simulation(self, duration=300):
        """
        Run the integrated simulation
        
        Args:
            duration (int): Duration of simulation in seconds
            
        Returns:
            dict: Simulation results
        """
        logger.info(f"Starting integrated simulation for {duration} seconds")
        
        # Start defense system in a separate thread
        defense_thread = threading.Thread(
            target=self._run_defense_system,
            args=(duration,)
        )
        defense_thread.daemon = True
        defense_thread.start()
        
        # Wait for defense system to establish baseline
        logger.info("Waiting for defense system to establish baseline...")
        time.sleep(60)
        
        # Run attack simulation
        logger.info("Starting attack simulation...")
        attack_results = self._run_attacks()
        
        # Wait for defense system to complete
        defense_thread.join(timeout=duration)
        
        # Evaluate results
        results = self._evaluate_results(attack_results)
        
        return results
    
    def _run_defense_system(self, duration):
        """
        Run the defense system
        
        Args:
            duration (int): Duration to run in seconds
        """
        try:
            # Start monitoring
            self.defense_system.start_monitoring(duration=duration)
        except Exception as e:
            logger.error(f"Error in defense system: {e}")
    
    def _run_attacks(self):
        """
        Run various attacks
        
        Returns:
            list: Attack results
        """
        attack_results = []
        
        # Get attacker and target nodes
        attacker1 = self.net.get('attacker1')
        attacker2 = self.net.get('attacker2')
        server = self.net.get('server')
        
        # Run different types of attacks
        attack_types = ['dos', 'port_scan', 'syn_flood', 'ping_flood']
        
        for attack_type in attack_types:
            # Generate random duration and intensity
            duration = 10  # Short duration for testing
            intensity = 5   # Medium intensity
            
            logger.info(f"Running {attack_type} attack (duration: {duration}s, intensity: {intensity})...")
            
            # Run the attack from attacker1
            attack_metadata = self.attack_simulator.generate_attack_data(
                attack_type, duration, intensity
            )
            
            if attack_metadata:
                attack_results.append(attack_metadata)
            
            # Wait between attacks
            time.sleep(30)
            
            # Run the same attack from attacker2 with different parameters
            attack_simulator2 = AttackSimulator(
                attacker_ip=attacker2.IP(),
                target_ip=server.IP(),
                interface=attacker2.defaultIntf().name
            )
            
            duration = 15  # Different duration
            intensity = 7  # Different intensity
            
            logger.info(f"Running {attack_type} attack from second attacker (duration: {duration}s, intensity: {intensity})...")
            
            attack_metadata = attack_simulator2.generate_attack_data(
                attack_type, duration, intensity
            )
            
            if attack_metadata:
                attack_results.append(attack_metadata)
            
            # Wait between attacks
            time.sleep(30)
        
        return attack_results
    
    def _evaluate_results(self, attack_results):
        """
        Evaluate simulation results
        
        Args:
            attack_results (list): Attack results
            
        Returns:
            dict: Evaluation results
        """
        # Get defense system metrics
        defense_metrics = self.defense_system.evaluate_performance(attack_results)
        
        # Calculate additional metrics
        total_attacks = len(attack_results)
        detected_attacks = len(self.defense_system.traffic_analyzer.detected_attacks)
        blocked_ips = len(self.defense_system.firewall.blocked_ips)
        
        detection_rate = detected_attacks / max(1, total_attacks)
        blocking_rate = blocked_ips / max(1, total_attacks)
        
        # Combine metrics
        results = {
            'total_attacks': total_attacks,
            'detected_attacks': detected_attacks,
            'blocked_ips': blocked_ips,
            'detection_rate': detection_rate,
            'blocking_rate': blocking_rate,
            'defense_metrics': defense_metrics
        }
        
        # Save results to file
        results_file = f"../results/simulation_results_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Simulation results:")
        logger.info(f"  Total attacks: {total_attacks}")
        logger.info(f"  Detected attacks: {detected_attacks}")
        logger.info(f"  Blocked IPs: {blocked_ips}")
        logger.info(f"  Detection rate: {detection_rate:.2f}")
        logger.info(f"  Blocking rate: {blocking_rate:.2f}")
        
        return results
    
    def cleanup(self):
        """Clean up resources"""
        if self.net:
            logger.info("Stopping network...")
            self.net.stop()
        
        logger.info("Cleanup complete")


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Integrated Network Simulation System')
    
    parser.add_argument('--duration', type=int, default=300,
                        help='Duration of simulation in seconds (default: 300)')
    parser.add_argument('--ml-model', type=str, default=None,
                        help='Path to ML model file (default: None, will train a new model)')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Logging level (default: INFO)')
    
    return parser.parse_args()


def main():
    """Main function"""
    # Parse arguments
    args = parse_arguments()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Create integrated system
    system = IntegratedSystem(args)
    
    try:
        # Setup components
        if not system.setup_network():
            logger.error("Failed to set up network. Exiting.")
            return 1
        
        if not system.setup_attack_simulator():
            logger.error("Failed to set up attack simulator. Exiting.")
            return 1
        
        if not system.setup_defense_system():
            logger.error("Failed to set up defense system. Exiting.")
            return 1
        
        # Run simulation
        results = system.run_simulation(duration=args.duration)
        
        # Print summary
        logger.info("Simulation completed successfully")
        logger.info(f"Detection rate: {results['detection_rate']:.2f}")
        logger.info(f"Blocking rate: {results['blocking_rate']:.2f}")
        
        # Start CLI if requested
        if hasattr(args, 'cli') and args.cli:
            CLI(system.net)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
    finally:
        # Clean up
        system.cleanup()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
