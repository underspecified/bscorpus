#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from grutils import *

# utf-8 i/o plz!
import sys
import codecs 
stdout = codecs.getwriter('utf-8')(sys.stdout)
stdin = codecs.getwriter('utf-8')(sys.stdin)
stderr = codecs.getwriter('utf-8')(sys.stderr)

if len(sys.argv) == 2:
	unpickle_data(sys.argv[1])
	print_rlinks()
else:
	print >>stderr, 'usage: gr-discussion.py <rss-feed.pkl>'
