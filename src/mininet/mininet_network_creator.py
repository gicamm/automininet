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
    print('*** Please start your algorithm (30s)')
    time.sleep(30)

    print('\n*** Network started. Starting test tools')

    tests = network.tests
    pings = tests.ping
    iperfs = tests.iperf

    if iperfs != None:
        print('\n*** Starting iperf')
        # Creates folders
        if not os.path.exists("out/iperf/server/"):
            os.makedirs("out/iperf/server/")
        if not os.path.exists("out/iperf/client/"):
            os.makedirs("out/iperf/client/")

        port = 5001
        for ipf in iperfs:
            src = ipf.src
            dst = ipf.dst
            start = ipf.start
            ip = network.host(dst).IP
            dst_host = mininet_hosts[dst]
            bw = ipf.bw
            iperf_time = ipf.time
            iperf_server(dst_host, dst, port)
            src_host = mininet_hosts[src]
            src_host.cmd(iperf_client(src, dst, start, ip, port, iperf_time, bw,
                                      src + "-" + dst + "_" + str(start) + "-" + str(iperf_time) + ".txt"))
            port += 1

    if pings != None:
        print('\n*** Starting ping')

        # Creates folders
        if not os.path.exists("out/ping/"):
            os.makedirs("out/ping/")

        for png in pings:
            src = png.src
            dst = png.dst
            host = mininet_hosts[src]
            ip = network.host(dst).IP
            count = png.time
            interval = png.interval
            ping(src, dst, host, ip, count, interval, src + '-' + dst + '-ping.txt')

    info('*** TEST correctly started\n')

    # Check if duration is set
    duration = tests.duration
    if duration > 0:
        print("\nThe test's duration is [{}s]. Wait...".format(duration))
        time.sleep(duration)
        print('\n*** TEST correctly completed\n')
    else:
        info('*** Running CLI\n')
        CLI(mininet)
        info('*** Stopping network')
        mininet.stop()


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


def iperf_server(host, id, port):
    print("Creating iperf server on [{}:{}]".format(id, port))
    host.cmd('nohup iperf3 -s -p ' + str(port) + ' -4 -i 30 &> out/iperf/server/' + id + "-" + str(port) + '.txt&')


def iperf_client(src, dst, start, ip, port, iperf_time, bandwith, out):
    print("Creating iperf client [{}-{}] on port {}".format(src, dst, port))
    if start > 0:
        command = "sleep " + str(start) + " && "
    else:
        command = ""

    # TCP
    command += "nohup iperf3 -c " + ip + " -p " + str(port) + " -t " + str(iperf_time) + " -b " + str(bandwith) + "M -4 -Z -i 30 &> out/iperf/client/" + out + "&"

    # UDP
    # command += "nohup iperf3 -c "+ ip +" -p "+ port +" -t "+ iperf_time +" -u -b " + bandwith +"M -4 -Z -i 30 &> out/"+out+"&"

    return command


def ping(src, dst, host, ip, count, interval, out):
    print("Starting ping [{}-{}]".format(src, dst))
    host.cmd("nohup ping -c " + str(count) + " -i " + str(interval) + " " + ip + " &> out/ping/" + out + "&")


def stop():
    print('\n*** Stopping the network')
    mininet.stop()
