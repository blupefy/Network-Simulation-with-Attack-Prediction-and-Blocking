# Network Simulation with Attack Detection and ML Prediction

## Overview

This project implements a comprehensive network simulation environment with attack simulation, defense mechanisms, and machine learning-based attack prediction. The system allows you to:

1. Create a virtual network topology with legitimate clients, attackers, and a target server
2. Simulate various network attacks (DoS, port scanning, SYN flood, etc.)
3. Implement defense mechanisms to detect and block attacks
4. Use machine learning to predict attacks and evaluate defense effectiveness
5. Analyze system performance with detailed metrics and visualizations

## System Architecture

The system consists of the following main components:

1. **Network Topology**: Creates a virtual network using Mininet with legitimate clients, attacker nodes, a server, and a firewall/IDS node.
2. **Attack Simulator**: Generates various types of network attacks with configurable parameters.
3. **Defense Mechanisms**: Implements traffic analysis, attack detection, and IP blocking capabilities.
4. **Machine Learning Model**: Predicts attacks based on network traffic patterns and provides accuracy metrics.
5. **Integrated System**: Connects all components into a cohesive solution.
6. **Performance Evaluation**: Evaluates system effectiveness across different attack scenarios.

## Directory Structure

```
network_simulation/
├── src/
│   ├── network_topology.py      # Network topology implementation
│   ├── attack_simulator.py      # Attack simulation module
│   ├── defense_mechanisms.py    # Defense mechanisms implementation
│   ├── ml_model.py              # Machine learning model
│   ├── integrated_system.py     # Integration of all components
│   └── evaluate_performance.py  # System performance evaluation
├── data/
│   ├── attacks/                 # Attack metadata
│   ├── traffic/                 # Traffic data
│   ├── detections/              # Attack detection data
│   └── ml/                      # Machine learning data and models
├── logs/                        # System logs
└── results/                     # Performance results and visualizations
```

## Installation and Setup

### Prerequisites

- Ubuntu Linux (tested on Ubuntu 22.04)
- Python 3.10 or higher
- Mininet network emulator
- Root/sudo privileges (required for Mininet)

### Dependencies

The system requires the following Python packages:

- numpy
- pandas
- scikit-learn
- matplotlib
- tensorflow
- mininet
- scapy
- pyshark

These dependencies can be installed using:

```bash
pip3 install numpy pandas scikit-learn matplotlib tensorflow mininet scapy pyshark
```

## Usage Instructions

### Running the Integrated System

To run the complete integrated system:

```bash
cd network_simulation
sudo python3 src/integrated_system.py
```

Command-line options:
- `--duration`: Duration of simulation in seconds (default: 300)
- `--ml-model`: Path to ML model file (default: None, will train a new model)
- `--log-level`: Logging level (default: INFO)

### Evaluating System Performance

To evaluate system performance across different attack scenarios:

```bash
cd network_simulation
sudo python3 src/evaluate_performance.py
```

Command-line options:
- `--ml-model`: Path to ML model file (default: None, will train a new model)
- `--log-level`: Logging level (default: INFO)

### Running Individual Components

#### Network Topology

```bash
cd network_simulation
sudo python3 src/network_topology.py
```

#### Attack Simulator

```bash
cd network_simulation
sudo python3 src/attack_simulator.py [attacker_ip] [target_ip]
```

#### Defense Mechanisms

```bash
cd network_simulation
sudo python3 src/defense_mechanisms.py [interface] [ml_model_path]
```

#### Machine Learning Model

```bash
cd network_simulation
python3 src/ml_model.py
```

## Component Details

### Network Topology

The network topology consists of:
- 1 server (target)
- 3 legitimate clients
- 2 attacker nodes
- 1 firewall/IDS node
- 2 switches connecting all nodes

The topology is implemented using Mininet, which creates virtual hosts, switches, and links on a single machine.

### Attack Simulator

The attack simulator can generate the following types of attacks:
- **DoS (Denial of Service)**: Floods the target with a large number of packets
- **Port Scan**: Scans for open ports on the target
- **SYN Flood**: Sends a large number of SYN packets without completing the TCP handshake
- **Ping Flood**: Floods the target with ICMP echo requests
- **ARP Spoofing**: Sends fake ARP messages to associate the attacker's MAC address with the IP address of another host
- **Slowloris**: Keeps many connections open to the target by sending partial HTTP requests

Each attack can be configured with different duration and intensity parameters.

### Defense Mechanisms

The defense mechanisms include:
- **Packet Feature Extraction**: Extracts features from network packets for analysis
- **Traffic Analysis**: Analyzes network traffic to detect anomalies
- **Attack Detection**: Detects various types of attacks based on traffic patterns
- **Firewall Management**: Blocks malicious IP addresses

The defense system establishes a baseline of normal traffic and then detects deviations from this baseline.

### Machine Learning Model

The machine learning model:
- Uses a Random Forest classifier to predict attacks
- Can be trained on real or synthetic data
- Provides detailed performance metrics (accuracy, precision, recall, F1 score)
- Generates visualizations of model performance

### Performance Evaluation

The performance evaluation system:
- Runs multiple simulations with different attack scenarios
- Analyzes detection rates and blocking rates
- Evaluates ML model accuracy
- Generates visualizations of system performance

## Results and Visualizations

The system generates various visualizations to help analyze performance:
- Detection and blocking rates by attack scenario
- Attack intensity vs. detection rate
- Distribution of detected attack types
- ML model performance metrics

These visualizations are saved in the `results/evaluation/visualizations` directory.

## Extending the System

### Adding New Attack Types

To add a new attack type:
1. Add a new method to the `AttackSimulator` class in `attack_simulator.py`
2. Add the new attack type to the `attack_types` dictionary in the `__init__` method
3. Implement the attack logic in the new method

### Improving Defense Mechanisms

To enhance the defense mechanisms:
1. Add new detection methods to the `TrafficAnalyzer` class in `defense_mechanisms.py`
2. Modify the `detect_attacks` method to include the new detection logic
3. Update the `FirewallManager` class if needed

### Enhancing the ML Model

To improve the machine learning model:
1. Add new features to the `generate_features_for_ml` method in `defense_mechanisms.py`
2. Modify the `NetworkAttackModel` class in `ml_model.py` to use different algorithms or hyperparameters
3. Update the feature extraction logic if needed

## Troubleshooting

### Common Issues

1. **Permission Errors**: Mininet requires root privileges. Run the scripts with `sudo`.
2. **Network Interface Issues**: If the system can't find the network interface, specify it explicitly using command-line arguments.
3. **ML Model Errors**: If the ML model fails to load, ensure the model file exists or let the system train a new model.

### Logging

The system logs detailed information to the `logs` directory. Check these logs for troubleshooting:
- `network_topology.log`: Network topology logs
- `attack_simulation.log`: Attack simulation logs
- `defense_mechanisms.log`: Defense mechanisms logs
- `ml_model.log`: Machine learning model logs
- `integration.log`: Integrated system logs
- `evaluation.log`: Performance evaluation logs

## Conclusion

This network simulation system provides a comprehensive environment for simulating network attacks, implementing defense mechanisms, and evaluating their effectiveness using machine learning. The system is highly configurable and can be extended to include additional attack types, defense mechanisms, and machine learning models.
