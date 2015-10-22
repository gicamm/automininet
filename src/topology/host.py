__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'


class Host(object):
    def __init__(self, obj):
        self.ID = obj["ID"]
        self.IP = obj["ip"]
        self.description = obj["description"]
