__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'


class Iperf(object):
    def __init__(self, obj):
        self.src = obj["src"]
        self.dst = obj["dst"]
        self.start = obj["start"]
        self.time = obj["time"]
        self.bw = obj["bw"]
