__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'

from switch import Switch
from host import Host
from link import Link
from controller import Controller


class Topology(object):
    switches = list()
    hosts = list()

    def __init__(self, obj):
        self.ID = obj["ID"]
        self.version = obj["version"]
        self.author = obj["author"]
        self.ofVersion = obj["ofVersion"]

        self.controller = Controller(obj["controller"])

        tup = obj["switches"]
        self.switches = list()
        for i in tup:
            self.switches.append(Switch(i))

        tup = obj["hosts"]
        self.hosts = list()
        for i in tup:
            self.hosts.append(Host(i))

        tup = obj["links"]
        self.links = list()
        for i in tup:
            self.links.append(Link(i))

    def switch_ids(self):
        return self.__ids(self.switches)

    def host_ids(self):
        return self.__ids(self.hosts)

    def __ids(self, lst):
        """

        :rtype : list
        """
        ids = list()
        for i in lst:
            ids.append(i.ID)

        return ids
