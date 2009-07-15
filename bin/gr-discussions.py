#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

from grutils import *

# utf-8 i/o plz!
import sys
import codecs 
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getwriter('utf-8')(sys.stdin)

if len(sys.argv) == 2:
	unpickle_data(sys.argv[1])
	print_rlinks()
else:
	print >>sys.stderr, 'usage: gr-discussion.py <rss-feed.pkl>'
