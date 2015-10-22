__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'


class Link(object):
    def __init__(self, obj):
        self.src = obj["src"]
        self.dst = obj["dst"]
        self.options = Link_Option(obj["options"])


class Link_Option(object):
    def __init__(self, obj):
        self.bw = obj["bw"]
        self.delay = obj["delay"]
        self.loss = obj["loss"]
        self.use_htb = obj["use_htb"]