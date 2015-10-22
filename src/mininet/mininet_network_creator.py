#!/usr/bin/python

__author__ = 'Giovanni Cammarata'
__email__ = "cammarata.giovanni@gmail.com"
__license__ = "Apache License"
__version__ = "1.0"

from src.utils.serialization import serializator
from src.topology import topology

import time

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

mininet = None


def create_network(json_file):
    print("creating network from file " + json_file)
    network = topology.Topology(serializator.from_json_file(json_file))
    print("Creating network " + network.ID)

    global mininet
    mininet = Mininet(topo=None, link=TCLink, build=False, switch=OVSKernelSwitch)

    controller = network.controller
    print("Adding the controller {} {}:{}".format(controller.ID, controller.IP, controller.port))
    mininet.addController(controller.ID, controller=RemoteController, ip=controller.IP, port=controller.port)

    switches = network.switches
    hosts = network.hosts

    print("Switches: " + str(switches.__len__()))
    print("Hosts: " + str(hosts.__len__()))

    print("\nCreating Switches")
    mininet_switches = {}
    for switch in switches:
        s = create_switch(switch, 'OpenFlow13')
        mininet_switches[switch.ID] = s

    print("\nCreating Hosts")
    mininet_hosts = {}
    for host in hosts:
        h = create_host(host)
        mininet_hosts[host.ID] = h

    print("\nCreating Links")
    links = network.links
    for link in links:
        create_link(link, mininet_switches, mininet_hosts)

    print('\n\n*** Starting network\n')
    mininet.start()

    sleep_time = 25
    print('*** SLEEPING {}s'.format(sleep_time))
    time.sleep(sleep_time)
    print('*** Doing ping')
    mininet.pingAll()
    time.sleep(10)

    print('\n*** Network started')


def create_switch(switch, openflowVersion):
    switch_id = switch.ID
    switch_ip = switch.IP
    print("Creating switch: {} {} {}".format(switch_id, switch.description, switch_ip))
    s = mininet.addSwitch(switch_id, cls=OVSSwitch, protocols=openflowVersion)
    s.cmd('ifconfig {} {}'.format(switch_id, switch_ip))
    # s = switch
    return s


def create_host(host):
    host_ip = host.IP
    host_id = host.ID
    print("Creating switch: {} {} {}".format(host_id, host.description, host_ip))
    h = mininet.addHost(host_id, ip=host_ip)
    # h = host
    return h


def create_link(link, switches, hosts):
    src = link.src
    dst = link.dst
    options = link.options
    linkopts = dict(bw=options.bw, delay=options.delay, loss=options.loss, use_htb=options.use_htb)

    src_node = get_node(src, switches, hosts)
    dst_node = get_node(dst, switches, hosts)

    print("Creating link [{}-{}] with options {}".format(src, dst, linkopts))
    mininet.addLink(src_node, dst_node, **linkopts)


def get_node(node_id, switches, hosts):
    if node_id in switches.keys():
        return switches[node_id]
    else:
        return hosts[node_id]


def stop():
    print('\n*** Stopping the network')
    mininet.stop()
