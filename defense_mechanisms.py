#!/usr/bin/env python3
"""
Defense Mechanisms Module for Network Simulation Environment
This script implements various defense mechanisms to detect and block network attacks.
"""

import logging
import os
import sys
import time
import threading
import json
import pandas as pd
import numpy as np
from collections import defaultdict, deque
from scapy.all import IP, TCP, UDP, ICMP, sniff, get_if_list
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/defense_mechanisms.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('defense_mechanisms')

class PacketFeatureExtractor:
    """
    Extract features from network packets for attack detection
    """
    
    def __init__(self):
        """Initialize the feature extractor"""
        logger.info("Initializing packet feature extractor")
    
    def extract_features(self, packet):
        """
        Extract features from a packet
        
        Args:
            packet: Scapy packet object
            
        Returns:
            dict: Dictionary of features
        """
        features = {
            'timestamp': time.time(),
            'packet_size': len(packet),
            'has_ip': 0,
            'has_tcp': 0,
            'has_udp': 0,
            'has_icmp': 0,
            'ip_src': None,
            'ip_dst': None,
            'ip_ttl': None,
            'tcp_sport': None,
            'tcp_dport': None,
            'tcp_flags': None,
            'udp_sport': None,
            'udp_dport': None,
            'icmp_type': None
        }
        
        # Extract IP layer features
        if IP in packet:
            features['has_ip'] = 1
            features['ip_src'] = packet[IP].src
            features['ip_dst'] = packet[IP].dst
            features['ip_ttl'] = packet[IP].ttl
        
        # Extract TCP layer features
        if TCP in packet:
            features['has_tcp'] = 1
            features['tcp_sport'] = packet[TCP].sport
            features['tcp_dport'] = packet[TCP].dport
            features['tcp_flags'] = packet[TCP].flags
        
        # Extract UDP layer features
        if UDP in packet:
            features['has_udp'] = 1
            features['udp_sport'] = packet[UDP].sport
            features['udp_dport'] = packet[UDP].dport
        
        # Extract ICMP layer features
        if ICMP in packet:
            features['has_icmp'] = 1
            features['icmp_type'] = packet[ICMP].type
        
        return features


class TrafficAnalyzer:
    """
    Analyze network traffic to detect anomalies and attacks
    """
    
    def __init__(self, window_size=60, threshold_multiplier=3):
        """
        Initialize the traffic analyzer
        
        Args:
            window_size (int): Time window size in seconds for traffic analysis
            threshold_multiplier (float): Multiplier for threshold calculation
        """
        self.window_size = window_size
        self.threshold_multiplier = threshold_multiplier
        self.feature_extractor = PacketFeatureExtractor()
        
        # Traffic statistics
        self.packet_count = 0
        self.packet_window = deque()
        self.ip_src_counts = defaultdict(int)
        self.ip_dst_counts = defaultdict(int)
        self.port_counts = defaultdict(int)
        self.tcp_syn_counts = defaultdict(int)
        self.icmp_counts = defaultdict(int)
        
        # Baseline statistics (normal traffic)
        self.baseline = {
            'packets_per_second': 0,
            'unique_src_ips': 0,
            'unique_dst_ips': 0,
            'syn_ratio': 0,
            'icmp_ratio': 0
        }
        
        # Attack detection thresholds
        self.thresholds = {
            'packets_per_second': 0,
            'unique_src_ips': 0,
            'syn_ratio': 0,
            'icmp_ratio': 0,
            'connection_ratio': 0
        }
        
        # Detection results
        self.detected_attacks = []
        
        # Create directories for data if they don't exist
        if not os.path.exists('../data/traffic'):
            os.makedirs('../data/traffic')
        if not os.path.exists('../data/detections'):
            os.makedirs('../data/detections')
        
        logger.info(f"Traffic analyzer initialized with window size {window_size}s")
    
    def process_packet(self, packet):
        """
        Process a packet and update traffic statistics
        
        Args:
            packet: Scapy packet object
        """
        # Extract features
        features = self.feature_extractor.extract_features(packet)
        
        # Update packet count
        self.packet_count += 1
        
        # Add packet to window
        self.packet_window.append(features)
        
        # Remove old packets from window
        current_time = time.time()
        while self.packet_window and (current_time - self.packet_window[0]['timestamp']) > self.window_size:
            old_features = self.packet_window.popleft()
            
            # Decrement counters for old packet
            if old_features['ip_src']:
                self.ip_src_counts[old_features['ip_src']] -= 1
                if self.ip_src_counts[old_features['ip_src']] <= 0:
                    del self.ip_src_counts[old_features['ip_src']]
            
            if old_features['ip_dst']:
                self.ip_dst_counts[old_features['ip_dst']] -= 1
                if self.ip_dst_counts[old_features['ip_dst']] <= 0:
                    del self.ip_dst_counts[old_features['ip_dst']]
            
            # Decrement port counters
            if old_features['tcp_dport']:
                port_key = f"TCP:{old_features['tcp_dport']}"
                self.port_counts[port_key] -= 1
                if self.port_counts[port_key] <= 0:
                    del self.port_counts[port_key]
            
            if old_features['udp_dport']:
                port_key = f"UDP:{old_features['udp_dport']}"
                self.port_counts[port_key] -= 1
                if self.port_counts[port_key] <= 0:
                    del self.port_counts[port_key]
            
            # Decrement TCP SYN counter
            if old_features['tcp_flags'] and 'S' in old_features['tcp_flags'] and not 'A' in old_features['tcp_flags']:
                src_key = old_features['ip_src']
                self.tcp_syn_counts[src_key] -= 1
                if self.tcp_syn_counts[src_key] <= 0:
                    del self.tcp_syn_counts[src_key]
            
            # Decrement ICMP counter
            if old_features['has_icmp']:
                src_key = old_features['ip_src']
                self.icmp_counts[src_key] -= 1
                if self.icmp_counts[src_key] <= 0:
                    del self.icmp_counts[src_key]
        
        # Update counters for new packet
        if features['ip_src']:
            self.ip_src_counts[features['ip_src']] += 1
        
        if features['ip_dst']:
            self.ip_dst_counts[features['ip_dst']] += 1
        
        # Update port counters
        if features['tcp_dport']:
            port_key = f"TCP:{features['tcp_dport']}"
            self.port_counts[port_key] += 1
        
        if features['udp_dport']:
            port_key = f"UDP:{features['udp_dport']}"
            self.port_counts[port_key] += 1
        
        # Update TCP SYN counter
        if features['tcp_flags'] and 'S' in features['tcp_flags'] and not 'A' in features['tcp_flags']:
            src_key = features['ip_src']
            self.tcp_syn_counts[src_key] += 1
        
        # Update ICMP counter
        if features['has_icmp']:
            src_key = features['ip_src']
            self.icmp_counts[src_key] += 1
    
    def establish_baseline(self, duration=300):
        """
        Establish baseline statistics for normal traffic
        
        Args:
            duration (int): Duration in seconds to collect baseline statistics
        """
        logger.info(f"Establishing baseline traffic statistics for {duration} seconds")
        
        # Clear existing statistics
        self.packet_window.clear()
        self.ip_src_counts.clear()
        self.ip_dst_counts.clear()
        self.port_counts.clear()
        self.tcp_syn_counts.clear()
        self.icmp_counts.clear()
        
        # Start packet capture for baseline
        start_time = time.time()
        
        # Wait for duration
        while time.time() - start_time < duration:
            time.sleep(1)
        
        # Calculate baseline statistics
        window_duration = min(self.window_size, time.time() - start_time)
        if window_duration <= 0:
            window_duration = 1  # Avoid division by zero
        
        self.baseline['packets_per_second'] = len(self.packet_window) / window_duration
        self.baseline['unique_src_ips'] = len(self.ip_src_counts)
        self.baseline['unique_dst_ips'] = len(self.ip_dst_counts)
        
        # Calculate SYN ratio (SYN packets / total packets)
        total_syn_packets = sum(self.tcp_syn_counts.values())
        self.baseline['syn_ratio'] = total_syn_packets / max(1, len(self.packet_window))
        
        # Calculate ICMP ratio (ICMP packets / total packets)
        total_icmp_packets = sum(self.icmp_counts.values())
        self.baseline['icmp_ratio'] = total_icmp_packets / max(1, len(self.packet_window))
        
        # Set thresholds based on baseline
        self.thresholds['packets_per_second'] = self.baseline['packets_per_second'] * self.threshold_multiplier
        self.thresholds['unique_src_ips'] = self.baseline['unique_src_ips'] * self.threshold_multiplier
        self.thresholds['syn_ratio'] = max(0.5, self.baseline['syn_ratio'] * self.threshold_multiplier)
        self.thresholds['icmp_ratio'] = max(0.3, self.baseline['icmp_ratio'] * self.threshold_multiplier)
        self.thresholds['connection_ratio'] = 0.7  # Ratio of connections to a single destination
        
        logger.info(f"Baseline established: {self.baseline}")
        logger.info(f"Thresholds set: {self.thresholds}")
        
        # Save baseline to file
        with open('../data/traffic/baseline.json', 'w') as f:
            json.dump({
                'baseline': self.baseline,
                'thresholds': self.thresholds
            }, f, indent=2)
    
    def detect_attacks(self):
        """
        Detect attacks based on current traffic statistics
        
        Returns:
            list: List of detected attacks
        """
        detected = []
        current_time = time.time()
        
        # Calculate current statistics
        window_duration = min(self.window_size, current_time - self.packet_window[0]['timestamp'] if self.packet_window else 0)
        if window_duration <= 0:
            window_duration = 1  # Avoid division by zero
        
        packets_per_second = len(self.packet_window) / window_duration
        unique_src_ips = len(self.ip_src_counts)
        
        # Calculate SYN ratio (SYN packets / total packets)
        total_syn_packets = sum(self.tcp_syn_counts.values())
        syn_ratio = total_syn_packets / max(1, len(self.packet_window))
        
        # Calculate ICMP ratio (ICMP packets / total packets)
        total_icmp_packets = sum(self.icmp_counts.values())
        icmp_ratio = total_icmp_packets / max(1, len(self.packet_window))
        
        # Check for DoS attack (high packet rate)
        if packets_per_second > self.thresholds['packets_per_second']:
            attack = {
                'type': 'DoS',
                'timestamp': current_time,
                'confidence': min(1.0, packets_per_second / self.thresholds['packets_per_second']),
                'details': {
                    'packets_per_second': packets_per_second,
                    'threshold': self.thresholds['packets_per_second']
                }
            }
            detected.append(attack)
            logger.warning(f"DoS attack detected: {packets_per_second:.2f} packets/s (threshold: {self.thresholds['packets_per_second']:.2f})")
        
        # Check for port scan (many unique destination ports)
        if len(self.port_counts) > self.thresholds['unique_src_ips'] * 5:
            # Find source IP with most port connections
            port_scan_sources = defaultdict(int)
            for features in self.packet_window:
                if features['tcp_dport'] or features['udp_dport']:
                    port_scan_sources[features['ip_src']] += 1
            
            if port_scan_sources:
                max_source = max(port_scan_sources.items(), key=lambda x: x[1])
                attack = {
                    'type': 'Port Scan',
                    'timestamp': current_time,
                    'confidence': min(1.0, len(self.port_counts) / (self.thresholds['unique_src_ips'] * 5)),
                    'details': {
                        'source_ip': max_source[0],
                        'unique_ports': len(self.port_counts),
                        'threshold': self.thresholds['unique_src_ips'] * 5
                    }
                }
                detected.append(attack)
                logger.warning(f"Port scan detected from {max_source[0]}: {len(self.port_counts)} unique ports")
        
        # Check for SYN flood (high ratio of SYN packets)
        if syn_ratio > self.thresholds['syn_ratio']:
            # Find source IP with most SYN packets
            if self.tcp_syn_counts:
                max_source = max(self.tcp_syn_counts.items(), key=lambda x: x[1])
                attack = {
                    'type': 'SYN Flood',
                    'timestamp': current_time,
                    'confidence': min(1.0, syn_ratio / self.thresholds['syn_ratio']),
                    'details': {
                        'source_ip': max_source[0],
                        'syn_ratio': syn_ratio,
                        'threshold': self.thresholds['syn_ratio']
                    }
                }
                detected.append(attack)
                logger.warning(f"SYN flood detected from {max_source[0]}: {syn_ratio:.2f} ratio (threshold: {self.thresholds['syn_ratio']:.2f})")
        
        # Check for ICMP flood (high ratio of ICMP packets)
        if icmp_ratio > self.thresholds['icmp_ratio']:
            # Find source IP with most ICMP packets
            if self.icmp_counts:
                max_source = max(self.icmp_counts.items(), key=lambda x: x[1])
                attack = {
                    'type': 'ICMP Flood',
                    'timestamp': current_time,
                    'confidence': min(1.0, icmp_ratio / self.thresholds['icmp_ratio']),
                    'details': {
                        'source_ip': max_source[0],
                        'icmp_ratio': icmp_ratio,
                        'threshold': self.thresholds['icmp_ratio']
                    }
                }
                detected.append(attack)
                logger.warning(f"ICMP flood detected from {max_source[0]}: {icmp_ratio:.2f} ratio (threshold: {self.thresholds['icmp_ratio']:.2f})")
        
        # Check for ARP spoofing (multiple MAC addresses for same IP)
        # This would require tracking ARP packets, which is not implemented in this simplified version
        
        # Update detected attacks list
        self.detected_attacks.extend(detected)
        
        # Save detection to file if attacks were detected
        if detected:
            detection_file = f"../data/detections/detection_{int(current_time)}.json"
            with open(detection_file, 'w') as f:
                json.dump(detected, f, indent=2)
        
        return detected
    
    def generate_features_for_ml(self):
        """
        Generate features for machine learning model
        
        Returns:
            pd.DataFrame: Dat
(Content truncated due to size limit. Use line ranges to read in chunks)