__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'


class Controller(object):
    def __init__(self, obj):
        self.ID = obj["ID"]
        self.IP = obj["ip"]
        self.port = obj["port"]
