#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import os
import re

from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()
if (len(args) > 0):
    old = args[0]
    if os.path.exists(old):
        os.rename(old, "%d-%s" % (int(os.path.getmtime(old)), old))
