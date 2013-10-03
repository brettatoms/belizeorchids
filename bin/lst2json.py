#!/usr/bin/env python

from __future__ import print_function
import json
import os
import sys

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datapath = os.path.join(basepath, 'data')
orchids_csv = os.path.join(datapath, "orchids.csv")

orchids = {}
for line in open(orchids_csv):
    line = line.strip()
    orchids[line] = dict(images=[], synonyms=[])

def filename_to_latin(filename):
    # TODO: this could be replaced with a regex but we just want to get it working for now
    index = filename.find("-")
    if index > -1:
        filename = filename[0:index]
    else:
        filename = filename[0:filename.find(".")]
    filename = filename.replace('_', ' ').capitalize()
    filename = filename.replace(" subsp ", " subsp. ")
    filename = filename.replace(" var ", " var. ")
    return filename

missing = set()
orchid_lst=os.path.abspath(os.path.join(datapath, 'orchids.lst'))
for path in open(orchid_lst):
    path = path.strip()
    #print(filename, ": ", filename_to_latin(filename))
    parent_dir, filename = os.path.split(path)
    name = filename_to_latin(filename)
    if name in orchids:
        orchids[name]['images'].append(filename)
    else:
        missing.add(name)

data = json.dumps(orchids, sort_keys=True, indent=4, separators=(',', ': '))
print(data)
for name in sorted(missing):
    print(name)
