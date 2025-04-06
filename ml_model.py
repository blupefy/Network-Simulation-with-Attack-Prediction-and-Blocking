#!/usr/bin/env python3
"""
Machine Learning Model for Network Attack Detection
This script implements a machine learning model to predict network attacks.
"""

import os
import sys
import time
import json
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/ml_model.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ml_model')

class NetworkAttackModel:
    """
    Machine Learning Model for Network Attack Detection
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the ML model
        
        Args:
            model_path (str): Path to saved model file
        """
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_path = model_path
        
        # Create directories if they don't exist
        if not os.path.exists('../data/ml'):
            os.makedirs('../data/ml')
        if not os.path.exists('../results/ml'):
            os.makedirs('../results/ml')
        
        # Load model if path is provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            logger.info("No model path provided or model file not found. A new model will be created.")
    
    def load_model(self, model_path):
        """
        Load a saved model
        
        Args:
            model_path (str): Path to saved model file
            
        Returns:
            bool: True if model was loaded successfully, False otherwise
        """
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            
            logger.info(f"Model loaded successfully from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def save_model(self, model_path=None):
        """
        Save the model to a file
        
        Args:
            model_path (str): Path to save model file
            
        Returns:
            str: Path to saved model file
        """
        if self.model is None:
            logger.error("No model to save")
            return None
        
        if model_path is None:
            model_path = f"../data/ml/network_attack_model_{int(time.time())}.pkl"
        
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_columns': self.feature_columns
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved to {model_path}")
            return model_path
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return None
    
    def prepare_data(self, normal_traffic_file, attack_traffic_file):
        """
        Prepare data for training
        
        Args:
            normal_traffic_file (str): Path to normal traffic data file
            attack_traffic_file (str): Path to attack traffic data file
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        try:
            # Load normal traffic data
            normal_df = pd.read_csv(normal_traffic_file)
            normal_df['label'] = 0  # 0 for normal traffic
            
            # Load attack traffic data
            attack_df = pd.read_csv(attack_traffic_file)
            attack_df['label'] = 1  # 1 for attack traffic
            
            # Combine datasets
            combined_df = pd.concat([normal_df, attack_df], ignore_index=True)
            
            # Drop non-feature columns
            if 'src_ip' in combined_df.columns:
                combined_df = combined_df.drop('src_ip', axis=1)
            
            # Handle missing values
            combined_df = combined_df.fillna(0)
            
            # Split features and target
            X = combined_df.drop('label', axis=1)
            y = combined_df['label']
            
            # Save feature columns
            self.feature_columns = X.columns.tolist()
            
            # Split into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            logger.info(f"Data prepared: {len(X_train)} training samples, {len(X_test)} testing samples")
            
            return X_train_scaled, X_test_scaled, y_train, y_test
        except Exception as e:
            logger.error(f"Failed to prepare data: {e}")
            return None, None, None, None
    
    def generate_synthetic_data(self, num_normal=1000, num_attack=1000):
        """
        Generate synthetic data for training when real data is not available
        
        Args:
            num_normal (int): Number of normal traffic samples to generate
            num_attack (int): Number of attack traffic samples to generate
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        logger.info(f"Generating synthetic data: {num_normal} normal samples, {num_attack} attack samples")
        
        # Define feature columns
        feature_columns = [
            'packet_count', 'packets_per_second', 'mean_packet_size', 'std_packet_size',
            'mean_time_diff', 'std_time_diff', 'tcp_ratio', 'udp_ratio', 'icmp_ratio',
            'syn_ratio', 'ack_ratio', 'unique_dst_ips', 'unique_dst_ports',
            'dst_ip_ratio', 'dst_port_ratio'
        ]
        self.feature_columns = feature_columns
        
        # Generate normal traffic data
        normal_data = []
        for _ in range(num_normal):
            # Normal traffic characteristics
            sample = {
                'packet_count': np.random.randint(10, 100),
                'packets_per_second': np.random.uniform(1, 10),
                'mean_packet_size': np.random.uniform(100, 1500),
                'std_packet_size': np.random.uniform(10, 200),
                'mean_time_diff': np.random.uniform(0.1, 1.0),
                'std_time_diff': np.random.uniform(0.01, 0.5),
                'tcp_ratio': np.random.uniform(0.5, 0.9),
                'udp_ratio': np.random.uniform(0.1, 0.3),
                'icmp_ratio': np.random.uniform(0, 0.1),
                'syn_ratio': np.random.uniform(0.1, 0.3),
                'ack_ratio': np.random.uniform(0.3, 0.7),
                'unique_dst_ips': np.random.randint(1, 5),
                'unique_dst_ports': np.random.randint(1, 10),
                'dst_ip_ratio': np.random.uniform(0.1, 0.5),
                'dst_port_ratio': np.random.uniform(0.1, 0.5),
                'label': 0  # Normal traffic
            }
            normal_data.append(sample)
        
        # Generate attack traffic data
        attack_data = []
        for _ in range(num_attack):
            # Randomly choose attack type
            attack_type = np.random.choice(['dos', 'port_scan', 'syn_flood', 'icmp_flood'])
            
            if attack_type == 'dos':
                # DoS attack characteristics
                sample = {
                    'packet_count': np.random.randint(500, 2000),
                    'packets_per_second': np.random.uniform(50, 200),
                    'mean_packet_size': np.random.uniform(100, 1500),
                    'std_packet_size': np.random.uniform(10, 200),
                    'mean_time_diff': np.random.uniform(0.005, 0.02),
                    'std_time_diff': np.random.uniform(0.001, 0.01),
                    'tcp_ratio': np.random.uniform(0.8, 1.0),
                    'udp_ratio': np.random.uniform(0, 0.2),
                    'icmp_ratio': np.random.uniform(0, 0.1),
                    'syn_ratio': np.random.uniform(0.7, 1.0),
                    'ack_ratio': np.random.uniform(0, 0.3),
                    'unique_dst_ips': np.random.randint(1, 3),
                    'unique_dst_ports': np.random.randint(1, 3),
                    'dst_ip_ratio': np.random.uniform(0.01, 0.1),
                    'dst_port_ratio': np.random.uniform(0.01, 0.1),
                    'label': 1  # Attack traffic
                }
            elif attack_type == 'port_scan':
                # Port scan characteristics
                sample = {
                    'packet_count': np.random.randint(100, 500),
                    'packets_per_second': np.random.uniform(10, 50),
                    'mean_packet_size': np.random.uniform(60, 100),
                    'std_packet_size': np.random.uniform(5, 20),
                    'mean_time_diff': np.random.uniform(0.02, 0.1),
                    'std_time_diff': np.random.uniform(0.005, 0.02),
                    'tcp_ratio': np.random.uniform(0.9, 1.0),
                    'udp_ratio': np.random.uniform(0, 0.1),
                    'icmp_ratio': np.random.uniform(0, 0.05),
                    'syn_ratio': np.random.uniform(0.9, 1.0),
                    'ack_ratio': np.random.uniform(0, 0.1),
                    'unique_dst_ips': np.random.randint(1, 3),
                    'unique_dst_ports': np.random.randint(50, 200),
                    'dst_ip_ratio': np.random.uniform(0.01, 0.1),
                    'dst_port_ratio': np.random.uniform(0.5, 1.0),
                    'label': 1  # Attack traffic
                }
            elif attack_type == 'syn_flood':
                # SYN flood characteristics
                sample = {
                    'packet_count': np.random.randint(500, 2000),
                    'packets_per_second': np.random.uniform(50, 200),
                    'mean_packet_size': np.random.uniform(60, 100),
                    'std_packet_size': np.random.uniform(5, 15),
                    'mean_time_diff': np.random.uniform(0.005, 0.02),
                    'std_time_diff': np.random.uniform(0.001, 0.01),
                    'tcp_ratio': np.random.uniform(0.95, 1.0),
                    'udp_ratio': np.random.uniform(0, 0.05),
                    'icmp_ratio': np.random.uniform(0, 0.05),
                    'syn_ratio': np.random.uniform(0.95, 1.0),
                    'ack_ratio': np.random.uniform(0, 0.05),
                    'unique_dst_ips': np.random.randint(1, 3),
                    'unique_dst_ports': np.random.randint(1, 5),
                    'dst_ip_ratio': np.random.uniform(0.01, 0.1),
                    'dst_port_ratio': np.random.uniform(0.01, 0.1),
                    'label': 1  # Attack traffic
                }
            else:  # icmp_flood
                # ICMP flood characteristics
                sample = {
                    'packet_count': np.random.randint(500, 2000),
                    'packets_per_second': np.random.uniform(50, 200),
                    'mean_packet_size': np.random.uniform(60, 100),
                    'std_packet_size': np.random.uniform(5, 15),
                    'mean_time_diff': np.random.uniform(0.005, 0.02),
                    'std_time_diff': np.random.uniform(0.001, 0.01),
                    'tcp_ratio': np.random.uniform(0, 0.05),
                    'udp_ratio': np.random.uniform(0, 0.05),
                    'icmp_ratio': np.random.uniform(0.95, 1.0),
                    'syn_ratio': np.random.uniform(0, 0.05),
                    'ack_ratio': np.random.uniform(0, 0.05),
                    'unique_dst_ips': np.random.randint(1, 3),
                    'unique_dst_ports': np.random.randint(1, 3),
                    'dst_ip_ratio': np.random.uniform(0.01, 0.1),
                    'dst_port_ratio': np.random.uniform(0.01, 0.1),
                    'label': 1  # Attack traffic
                }
            
            attack_data.append(sample)
        
        # Combine normal and attack data
        all_data = normal_data + attack_data
        df = pd.DataFrame(all_data)
        
        # Save synthetic data to CSV files
        normal_df = df[df['label'] == 0]
        attack_df = df[df['label'] == 1]
        
        normal_df.to_csv('../data/ml/synthetic_normal_traffic.csv', index=False)
        attack_df.to_csv('../data/ml/synthetic_attack_traffic.csv', index=False)
        
        # Split features and target
        X = df.drop('label', axis=1)
        y = df['label']
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        logger.info(f"Synthetic data generated and prepared: {len(X_train)} training samples, {len(X_test)} testing samples")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """
        Train the machine learning model
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            bool: True if model was trained successfully, False otherwise
        """
        try:
            # Create and train the model
            logger.info("Training Random Forest Classifier...")
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train, y_train)
            
            logger.info("Model training completed")
            return True
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            return False
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the model performance
        
        Args:
            X_test: Testing features
            y_test: Testing labels
            
        Returns:
            dict: Evaluation metrics
        """
        if self.model is None:
            logger.error("No model to evaluate")
            return None
        
        try:
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            # Calculate feature importances
            feature_importances = self.model.feature_importances_
            
            # Create metrics dictionary
            metrics = {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1),
                'confusion_matrix': conf_matrix.tolist(),
                'feature_importances': {
                    feature: float(importance)
         
(Content truncated due to size limit. Use line ranges to read in chunks)