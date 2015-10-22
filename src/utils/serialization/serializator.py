# Filename: serializator.py

__author__ = 'Giovanni Cammarata <cammarata.giovanni@gmail.com>'

import json


def from_json(json_str):
    return json.loads(json_str)


def from_json_file(json_file):
    with open(json_file) as json_file:
        return json.load(json_file)
