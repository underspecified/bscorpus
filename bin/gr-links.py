#!/usr/bin/python2.5

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re

links = {}
d = feedparser.parse(r'/Users/eric/bscorpus/data/test/gr-test.xml')
for e in d.entries[:1]:
	print e.link
	p = urllib2.urlopen(e.link)
#	a = SoupStrainer('a')
#	s = BeautifulSoup(p, parseOnlyThese=a)
	s = BeautifulSoup(p)
	print s.prettify()
	for a in s.findAll('a'):
		print a['href']
