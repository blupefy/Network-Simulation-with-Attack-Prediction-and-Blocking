#!/usr/bin/env python3
"""
System Performance Evaluation Script
This script evaluates the performance of the integrated network simulation system.
"""

import os
import sys
import time
import json
import logging
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.integrated_system import IntegratedSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/evaluation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('evaluation')

class SystemEvaluator:
    """
    Class to evaluate the performance of the integrated system
    """
    
    def __init__(self, args):
        """
        Initialize the system evaluator
        
        Args:
            args: Command line arguments
        """
        self.args = args
        self.results_dir = '../results/evaluation'
        
        # Create results directory if it doesn't exist
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
        # Create visualizations directory if it doesn't exist
        if not os.path.exists(f"{self.results_dir}/visualizations"):
            os.makedirs(f"{self.results_dir}/visualizations")
        
        logger.info("System evaluator initialized")
    
    def run_evaluation(self):
        """
        Run the system evaluation
        
        Returns:
            dict: Evaluation results
        """
        logger.info("Starting system evaluation")
        
        # Run multiple simulations with different parameters
        simulation_results = []
        
        # Define different attack scenarios
        scenarios = [
            {'name': 'Low Intensity', 'duration': 180, 'attack_intensity': 3},
            {'name': 'Medium Intensity', 'duration': 180, 'attack_intensity': 5},
            {'name': 'High Intensity', 'duration': 180, 'attack_intensity': 8}
        ]
        
        # Run simulations for each scenario
        for scenario in scenarios:
            logger.info(f"Running simulation for scenario: {scenario['name']}")
            
            # Set scenario-specific parameters
            self.args.duration = scenario['duration']
            self.args.attack_intensity = scenario['attack_intensity']
            
            # Create and run integrated system
            system = IntegratedSystem(self.args)
            
            try:
                # Setup components
                if not system.setup_network():
                    logger.error(f"Failed to set up network for scenario: {scenario['name']}")
                    continue
                
                if not system.setup_attack_simulator():
                    logger.error(f"Failed to set up attack simulator for scenario: {scenario['name']}")
                    continue
                
                if not system.setup_defense_system():
                    logger.error(f"Failed to set up defense system for scenario: {scenario['name']}")
                    continue
                
                # Run simulation
                results = system.run_simulation(duration=scenario['duration'])
                
                # Add scenario information to results
                results['scenario'] = scenario['name']
                results['attack_intensity'] = scenario['attack_intensity']
                
                # Add results to list
                simulation_results.append(results)
                
                logger.info(f"Simulation completed for scenario: {scenario['name']}")
                logger.info(f"Detection rate: {results['detection_rate']:.2f}")
                logger.info(f"Blocking rate: {results['blocking_rate']:.2f}")
            except Exception as e:
                logger.error(f"Error in simulation for scenario {scenario['name']}: {e}")
            finally:
                # Clean up
                system.cleanup()
            
            # Wait between simulations
            time.sleep(10)
        
        # Analyze results
        analysis_results = self._analyze_results(simulation_results)
        
        # Generate visualizations
        self._generate_visualizations(simulation_results, analysis_results)
        
        # Save combined results
        combined_results = {
            'simulations': simulation_results,
            'analysis': analysis_results
        }
        
        results_file = f"{self.results_dir}/evaluation_results_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump(combined_results, f, indent=2)
        
        logger.info(f"Evaluation results saved to {results_file}")
        
        return combined_results
    
    def _analyze_results(self, simulation_results):
        """
        Analyze simulation results
        
        Args:
            simulation_results (list): List of simulation results
            
        Returns:
            dict: Analysis results
        """
        if not simulation_results:
            logger.warning("No simulation results to analyze")
            return {}
        
        # Extract metrics from all simulations
        detection_rates = [r['detection_rate'] for r in simulation_results]
        blocking_rates = [r['blocking_rate'] for r in simulation_results]
        
        # Calculate average metrics
        avg_detection_rate = np.mean(detection_rates)
        avg_blocking_rate = np.mean(blocking_rates)
        
        # Calculate standard deviation
        std_detection_rate = np.std(detection_rates)
        std_blocking_rate = np.std(blocking_rates)
        
        # Extract ML model metrics if available
        ml_metrics = []
        for result in simulation_results:
            if 'defense_metrics' in result and 'ml_metrics' in result['defense_metrics']:
                ml_metrics.append(result['defense_metrics']['ml_metrics'])
        
        # Calculate average ML metrics if available
        avg_ml_metrics = {}
        if ml_metrics:
            for metric in ['accuracy', 'precision', 'recall', 'f1_score']:
                if all(metric in m for m in ml_metrics):
                    avg_ml_metrics[metric] = np.mean([m[metric] for m in ml_metrics])
        
        # Create analysis results
        analysis_results = {
            'avg_detection_rate': float(avg_detection_rate),
            'avg_blocking_rate': float(avg_blocking_rate),
            'std_detection_rate': float(std_detection_rate),
            'std_blocking_rate': float(std_blocking_rate),
            'avg_ml_metrics': avg_ml_metrics
        }
        
        logger.info("Analysis results:")
        logger.info(f"  Average detection rate: {avg_detection_rate:.2f} (±{std_detection_rate:.2f})")
        logger.info(f"  Average blocking rate: {avg_blocking_rate:.2f} (±{std_blocking_rate:.2f})")
        
        if avg_ml_metrics:
            logger.info("  Average ML metrics:")
            for metric, value in avg_ml_metrics.items():
                logger.info(f"    {metric}: {value:.2f}")
        
        return analysis_results
    
    def _generate_visualizations(self, simulation_results, analysis_results):
        """
        Generate visualizations of evaluation results
        
        Args:
            simulation_results (list): List of simulation results
            analysis_results (dict): Analysis results
        """
        if not simulation_results:
            logger.warning("No simulation results for visualizations")
            return
        
        # 1. Detection and Blocking Rates by Scenario
        plt.figure(figsize=(10, 6))
        scenarios = [r['scenario'] for r in simulation_results]
        detection_rates = [r['detection_rate'] for r in simulation_results]
        blocking_rates = [r['blocking_rate'] for r in simulation_results]
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        plt.bar(x - width/2, detection_rates, width, label='Detection Rate')
        plt.bar(x + width/2, blocking_rates, width, label='Blocking Rate')
        
        plt.xlabel('Scenario')
        plt.ylabel('Rate')
        plt.title('Detection and Blocking Rates by Scenario')
        plt.xticks(x, scenarios)
        plt.ylim(0, 1.1)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/visualizations/rates_by_scenario.png")
        plt.close()
        
        # 2. Attack Intensity vs. Detection Rate
        plt.figure(figsize=(8, 6))
        intensities = [r['attack_intensity'] for r in simulation_results]
        detection_rates = [r['detection_rate'] for r in simulation_results]
        
        plt.scatter(intensities, detection_rates, s=100, alpha=0.7)
        
        # Add trend line
        z = np.polyfit(intensities, detection_rates, 1)
        p = np.poly1d(z)
        plt.plot(intensities, p(intensities), "r--", alpha=0.7)
        
        plt.xlabel('Attack Intensity')
        plt.ylabel('Detection Rate')
        plt.title('Attack Intensity vs. Detection Rate')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/visualizations/intensity_vs_detection.png")
        plt.close()
        
        # 3. Attack Type Distribution
        attack_types = []
        for result in simulation_results:
            if 'detected_attacks' in result['defense_metrics']:
                for attack in result['defense_metrics']['detected_attacks']:
                    if 'type' in attack:
                        attack_types.append(attack['type'])
        
        if attack_types:
            plt.figure(figsize=(8, 6))
            attack_type_counts = pd.Series(attack_types).value_counts()
            
            plt.pie(attack_type_counts, labels=attack_type_counts.index, autopct='%1.1f%%',
                   shadow=True, startangle=90)
            plt.axis('equal')
            plt.title('Distribution of Detected Attack Types')
            
            plt.tight_layout()
            plt.savefig(f"{self.results_dir}/visualizations/attack_type_distribution.png")
            plt.close()
        
        # 4. ML Model Performance Metrics
        ml_metrics = []
        for result in simulation_results:
            if 'defense_metrics' in result and 'ml_metrics' in result['defense_metrics']:
                ml_metrics.append({
                    'scenario': result['scenario'],
                    **result['defense_metrics']['ml_metrics']
                })
        
        if ml_metrics:
            metrics_df = pd.DataFrame(ml_metrics)
            
            plt.figure(figsize=(10, 6))
            metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
            
            for i, metric in enumerate(metrics_to_plot):
                if metric in metrics_df.columns:
                    plt.subplot(2, 2, i+1)
                    sns.barplot(x='scenario', y=metric, data=metrics_df)
                    plt.title(f'{metric.capitalize()}')
                    plt.ylim(0, 1.1)
                    plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig(f"{self.results_dir}/visualizations/ml_metrics.png")
            plt.close()
        
        logger.info("Visualizations generated and saved")


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Network Simulation System Evaluation')
    
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
    
    # Create system evaluator
    evaluator = SystemEvaluator(args)
    
    try:
        # Run evaluation
        results = evaluator.run_evaluation()
        
        # Print summary
        logger.info("Evaluation completed successfully")
        logger.info(f"Average detection rate: {results['analysis']['avg_detection_rate']:.2f}")
        logger.info(f"Average blocking rate: {results['analysis']['avg_blocking_rate']:.2f}")
        
        if 'avg_ml_metrics' in results['analysis'] and results['analysis']['avg_ml_metrics']:
            logger.info("Average ML metrics:")
            for metric, value in results['analysis']['avg_ml_metrics'].items():
                logger.info(f"  {metric}: {value:.2f}")
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in evaluation: {e}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
