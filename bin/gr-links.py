#!/usr/bin/python2.5

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re

links = {}
d = feedparser.parse(r'/home/is/eric-n/bscorpus/data/test/gr-test.xml')
for e in d.entries[:1]:
	print e.link
	p = urllib2.urlopen(e.link)
	a = SoupStrainer('a')
	links = [tag for tag in BeautifulSoup(p, parseOnlyThese=a)]
	for l in links:
		print l
