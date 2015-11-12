__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'


class Ping(object):
    def __init__(self, obj):
        self.src = obj["src"]
        self.dst = obj["dst"]
        self.start = obj["start"]
        self.time = obj["time"]
        self.interval = obj["interval"]
