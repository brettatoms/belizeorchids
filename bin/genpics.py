#!/usr/bin/env python

from __future__ import print_function
import json
import os
import re
import subprocess
import sys

line_rx = re.compile('(?:(?P<dir>.+)\/)?(?P<file>.*){1}(?:\:(?P<comment>.*?))?')

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datapath = os.path.join(basepath, 'data')
orchids_lst = os.path.join(datapath, "orchids.lst")

dest_path = os.path.join(basepath, "images", "orchids")
thumb_path = os.path.join(dest_path, "256x192")

src_path = os.path.join("/archive/Pictures/orchids")
if not os.path.exists(src_path):
    print("image source path does not exist: " + src_path)
    sys.exit(1)


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


def create_small_image(filename):
    pass

def create_large_image(filename):
    pass

orchids_lst=os.path.abspath(os.path.join(datapath, 'orchids.lst'))
for line in open(orchids_lst):
    line = line.strip()
    match = line_rx.match(line)
    if not match:
        raise ValueError("line does not match regex: " + line)

    groups = match.groupdict()
    filename = groups["file"]
    path = os.path.join(src_path, groups["dir"], filename)
    if not os.path.exists(path):
        print("file does not exist: ", path)
        sys.exit(1)

    # create the thumbnail
    thumb_filename = os.path.join(thumb_path, filename)
    if os.path.exists(path):
        print("file already exists", thumb_filename)
        sys.exit(1)

    print("converting: ", path)
    subprocess.call(["convert", path, "-thumbnail", "256x192", thumb_filename])

    # TODO: pass image through jpegtran to make it smaller

    # TODO: create a larger version of the same image to display when we click on itpp
