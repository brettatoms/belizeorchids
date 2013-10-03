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
pictures_lst = os.path.join(datapath, "pictures.lst")

dest_path = os.path.join(basepath, "app", "images", "orchids")
thumb_path = os.path.join(dest_path, "256x192")

if not os.path.exists(thumb_path):
    os.mkdir(thumb_path)

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
    filename = filename.replace("_subsp_", " subsp. ")
    filename = filename.replace("_var_ ", " var. ")
    return filename.replace('_', ' ').capitalize()


def create_small_image(filename):
    pass

def create_large_image(filename):
    pass

for line in open(pictures_lst):
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
    if os.path.exists(thumb_filename):
        # TODO: create a command line arg to overwrite files if they exists
        #print("file already exists", thumb_filename)
        #sys.exit(1)
        pass
    else:
        print("converting: ", path)
        subprocess.call(["convert", path, "-thumbnail", "256x192", thumb_filename])

    # TODO: pass image through jpegtran to make it smaller

    # TODO: create a larger version of the same image to display when we click
    # on itpp
