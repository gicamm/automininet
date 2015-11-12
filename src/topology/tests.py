__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'

from ping import Ping
from iperf import Iperf


class Tests(object):
    switches = list()
    hosts = list()

    def __init__(self, obj):
        self.duration = obj["duration"]
        self.ping = list()
        tup = obj["ping"]
        for i in tup:
            self.ping.append(Ping(i))

        self.iperf = list()
        tup = obj["iperf"]
        for i in tup:
            self.iperf.append(Iperf(i))
