#!/usr/bin/env python3
"""
Main script to run the network simulation system
This script provides a simple command-line interface to run the system.
"""

import os
import sys
import argparse
import logging

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.integrated_system import IntegratedSystem
from src.evaluate_performance import SystemEvaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('main')

def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Network Simulation with Attack Detection and ML Prediction'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Run simulation command
    sim_parser = subparsers.add_parser('run', help='Run the integrated simulation')
    sim_parser.add_argument('--duration', type=int, default=300,
                        help='Duration of simulation in seconds (default: 300)')
    sim_parser.add_argument('--ml-model', type=str, default=None,
                        help='Path to ML model file (default: None, will train a new model)')
    sim_parser.add_argument('--cli', action='store_true',
                        help='Start Mininet CLI after simulation')
    
    # Evaluate performance command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate system performance')
    eval_parser.add_argument('--ml-model', type=str, default=None,
                        help='Path to ML model file (default: None, will train a new model)')
    
    # Train ML model command
    train_parser = subparsers.add_parser('train', help='Train ML model only')
    
    # Common arguments
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
    
    # Create directories if they don't exist
    for directory in ['logs', 'data', 'results']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Process command
    if args.command == 'run':
        logger.info("Running integrated simulation")
        
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
            if args.cli:
                from mininet.cli import CLI
                CLI(system.net)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in simulation: {e}")
        finally:
            # Clean up
            system.cleanup()
    
    elif args.command == 'evaluate':
        logger.info("Evaluating system performance")
        
        # Create system evaluator
        evaluator = SystemEvaluator(args)
        
        try:
            # Run evaluation
            results = evaluator.run_evaluation()
            
            # Print summary
            logger.info("Evaluation completed successfully")
            logger.info(f"Average detection rate: {results['analysis']['avg_detection_rate']:.2f}")
            logger.info(f"Average blocking rate: {results['analysis']['avg_blocking_rate']:.2f}")
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in evaluation: {e}")
    
    elif args.command == 'train':
        logger.info("Training ML model")
        
        try:
            # Import ML model
            from src.ml_model import train_and_evaluate_model
            
            # Train model
            model_path = train_and_evaluate_model()
            
            if model_path:
                logger.info(f"Model trained and saved to {model_path}")
            else:
                logger.error("Failed to train model")
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error training model: {e}")
    
    else:
        logger.error("No command specified. Use --help for usage information.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
