#!/usr/bin/python
import os

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

    print('\n*** Network started. Starting tests')

    tests = network.tests
    pings = tests.ping
    iperfs = tests.iperf

    print('\n*** Starting iperf')
    if not os.path.exists("out/iperf/server/"):
        os.makedirs("out/iperf/server/")
    if not os.path.exists("out/iperf/client/"):
        os.makedirs("out/iperf/client/")
    # for iperf in iperfs:
    #     create_link(link, mininet_switches, mininet_hosts)

    print('\n*** Starting ping')

    if not os.path.exists("out/ping/"):
        os.makedirs("out/ping/")

    for png in pings:
        src = png.src
        dst = png.dst
        host = mininet_hosts[src]
        ip = network.host(dst).IP
        ping(src, dst, host, ip, src + '-' + dst + '-ping.txt')


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


def iperf_server(switch, port):
    switch.cmd('nohup iperf3 -s -p ' + str(port) + ' -4 -i 30 &> out/iperf/server/' + str(port) + '.txt&')


def iperf_client(ip, port, time, bandwith, out):
    # TCP
    command = "nohup iperf3 -c " + ip + " -p " + port + " -t " + str(
        time) + " -b " + bandwith + "M -4 -Z -i 30 &> out/iperf/client/" + out + "&"

    # UDP
    # command = "nohup iperf3 -c "+ ip +" -p "+ port +" -t "+ time +" -u -b " + bandwith +"M -4 -Z -i 30 &> out/"+out+"&"

    return command


def iperf_sleep(sleepTime, ip, port, time, bandwith, out):
    command = "sleep " + sleepTime + " && "
    command += iperf_client(ip, port, time, bandwith, out)
    return command


def ping(src,dst,host, ip, count, interval, out):
    print("Starting ping [{}-{}]".format(src, dst))
    host.cmd("nohup ping -c " + str(count) + " -i " + str(interval) + " " + ip + " &> out/ping/" + out + "&")


def stop():
    print('\n*** Stopping the network')
    mininet.stop()
