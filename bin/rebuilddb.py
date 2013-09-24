#!/usr/bin/env python

from __future__ import print_function
import json
import os
import sys

import gridfs
import pymongo

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datapath = os.path.join(basepath, 'data')
orchids_csv = os.path.join(datapath, "orchids.csv")

# read in the orchid data
rows = []
for line in open(orchids_csv):
    line = line.strip()
    row = dict(name=line)
    rows.append(row)

# read environment variables
rcfile = os.path.join(os.environ['HOME'], ".belizeorchids")
if os.path.exists(rcfile) and os.path.isfile(rcfile):
    for line in open(rcfile):
        try:
            name, value = line.split('=')
            if isinstance(name, str) and isinstance(value, str):
                os.environ[name.strip()] = str(value).strip()
        except Exception as exc:
            print(line)
            print(exc)

client = pymongo.MongoClient()
db = client.orchids
collection = db.orchids
collection.remove()
response = collection.insert(rows)
print("{} orchids inserted".format(len(rows)))

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

print("adding images")
thumbs = gridfs.GridFS(db, collection="thumbs")
thumbs_path = os.path.join(basepath, "images", "orchids", "256x192")
for thumb in os.listdir(thumbs_path):
    print(thumb, filename_to_latin(thumb))
    f = open(os.path.join(thumbs_path, thumb))
    thumbs.put(f, name=filename_to_latin(thumb), filename=thumb)
    f.close()
