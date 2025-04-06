#!/usr/bin/env python3
"""
Network Topology Implementation for Network Simulation Environment
This script defines the network topology using Mininet for simulating network attacks and defenses.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import os

class NetworkSimulationTopology(Topo):
    """
    Custom network topology class for attack simulation
    Implements a topology with:
    - 1 server (target)
    - 3 legitimate clients
    - 2 attacker nodes
    - 2 switches
    """
    
    def build(self):
        """Build the network topology"""
        
        # Add switches
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        
        # Add server (target)
        server = self.addHost('server', ip='10.0.0.100/24')
        
        # Add legitimate clients
        client1 = self.addHost('client1', ip='10.0.0.1/24')
        client2 = self.addHost('client2', ip='10.0.0.2/24')
        client3 = self.addHost('client3', ip='10.0.0.3/24')
        
        # Add attacker nodes
        attacker1 = self.addHost('attacker1', ip='10.0.0.50/24')
        attacker2 = self.addHost('attacker2', ip='10.0.0.51/24')
        
        # Add firewall/IDS node
        firewall = self.addHost('firewall', ip='10.0.0.254/24')
        
        # Connect hosts to switches
        # Legitimate clients and attackers connect to s1
        self.addLink(client1, s1, cls=TCLink, bw=10)
        self.addLink(client2, s1, cls=TCLink, bw=10)
        self.addLink(client3, s1, cls=TCLink, bw=10)
        self.addLink(attacker1, s1, cls=TCLink, bw=10)
        self.addLink(attacker2, s1, cls=TCLink, bw=10)
        
        # Connect s1 to firewall
        self.addLink(s1, firewall, cls=TCLink, bw=100)
        
        # Connect firewall to s2
        self.addLink(firewall, s2, cls=TCLink, bw=100)
        
        # Connect server to s2
        self.addLink(s2, server, cls=TCLink, bw=100)


def setup_network():
    """
    Set up and start the network simulation
    Returns the network object for further configuration
    """
    # Create the topology
    topo = NetworkSimulationTopology()
    
    # Create and start the network
    net = Mininet(
        topo=topo,
        controller=Controller,
        switch=OVSKernelSwitch,
        link=TCLink,
        build=False,
        autoSetMacs=True
    )
    
    # Add controller
    net.addController('c0')
    
    # Build and start network
    net.build()
    net.start()
    
    # Configure firewall node
    firewall = net.get('firewall')
    firewall.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    # Configure server
    server = net.get('server')
    server.cmd('python3 -m http.server 80 &')
    
    return net


def run_network_simulation():
    """
    Main function to run the network simulation
    """
    # Set log level
    setLogLevel('info')
    
    # Create log directory if it doesn't exist
    if not os.path.exists('../logs'):
        os.makedirs('../logs')
    
    # Setup the network
    info('*** Setting up network topology\n')
    net = setup_network()
    
    # Print network information
    info('*** Network topology is ready\n')
    net.pingAll()
    
    # Start CLI
    info('*** Starting CLI\n')
    CLI(net)
    
    # Stop network
    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    run_network_simulation()
