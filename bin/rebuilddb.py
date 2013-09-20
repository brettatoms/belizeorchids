#!/usr/bin/env python

from __future__ import print_function
import json
import os
import sys

import requests

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

db_url='https://brettatoms.iriscouch.com/orchids'
#user = os.environ["CLOUDANT_USER"]
#password = os.environ["CLOUDANT_PASSWORD"]

for row in rows:
    print(row)
    response = requests.post(db_url, data=json.dumps(row),
                             headers={"Content-Type": "application/json"},
                             #auth=(user, password)
    )
    assert response.status_code == 201, "Error: {}".format(response.status_code)

print("{} orchids inserted".format(len(rows)))
