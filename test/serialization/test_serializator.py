__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'

# from utils import
from src.utils.serialization import serializator

json='{"ID":"internet2-l3-t1","version":"v1","author":"Giovanni Cammarata <cammarata.giovanni@gmail.com>","ofVersion":"OpenFlow13"}'


topology = serializator.from_json(json)
print topology
print (topology['ID'])

topology = serializator.from_json_file("../../resources/topologies/internet2-le-v1.json")
print topology
print (topology['hosts'])
