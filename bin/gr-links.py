#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

from grutils import *

# utf-8 i/o plz!
import sys
import codecs 
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getwriter('utf-8')(sys.stdin)

if len(sys.argv) > 2:
	for x in sys.argv[2:]:
		get_links(x)
	pickle_data(sys.argv[1])

else:
	print >>sys.stderr, 'usage: gr-links.py <rss-feed.pkl> <rss-feed.xml> [<rss-feed.xml> ...]'
