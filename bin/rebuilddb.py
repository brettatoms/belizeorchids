#!/usr/bin/env python

from __future__ import print_function
import json
import os
import sys

import gridfs
import pymongo
from bson.binary import Binary

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datapath = os.path.join(basepath, 'data')
orchids_csv = os.path.join(datapath, "orchids.csv")

host="localhost"
port=27017
if len(sys.argv) > 1 and  sys.argv[1] == "production":
    host="mongodb.belizeorchids.com"

print("connection to {}:{}...".format(host, port ))
client = pymongo.MongoClient(host, port)
db = client.orchids

# read in the orchid data
rows = {}
for line in open(orchids_csv):
    line = line.strip()
    rows[line] = dict(name=line, thumbs=[])


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


# add the images filenames which will be used to lookup them up on s3
thumbs_path = os.path.join(basepath, "images", "orchids", "256x192")
for filename in os.listdir(thumbs_path):
    #print(filename, ": ", filename_to_latin(filename))
    name = filename_to_latin(filename)
    rows[name]["thumbs"].append(filename)

orchids = db.orchids
orchids.remove()
orchids.create_index([("name", pymongo.DESCENDING)], unique=True)
response = orchids.insert(rows.values())
print("{} orchids inserted".format(len(rows)))
