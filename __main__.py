#!/usr/bin/python

__author__ = 'Giovanni Cammarata'
__email__ = "cammarata.giovanni@gmail.com"
__license__ = "Apache License"
__version__ = "1.0"


from src.mininet import mininet_network_creator

import getopt
import sys


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print 'mininet_network_creator -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mininet_network_creator.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print 'Input file is "', inputfile
    mininet_network_creator.create_network(inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
