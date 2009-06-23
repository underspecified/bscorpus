#!/usr/bin/python2.5

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re
import os
import sys

links = {}
bshome = '%s/bscorpus' % os.environ['HOME']
x = '%s/data/test/gr-test.xml' % bshome
#x = '%s/data/gr/gr-feeds.00.xml' % bshome
d = feedparser.parse(x)
for e in d.entries:
#	print >>sys.stderr, e.link
	try:
		p = urllib2.urlopen(e.link)
#		s = BeautifulSoup(p)
		t = SoupStrainer('a', href=re.compile('http'))
		s = BeautifulSoup(p, parseOnlyThese=t)
#		print >>sys.stderr, s.prettify()
		links.setdefault(e.link, [])
		for a in s.findAll('a'):
			links[e.link].append(a['href'])
#			print >>sys.stderr, a['href']
	except:
		print >>sys.stderr, "FAIL! >_<", e.link

rlinks = {}
for l in sorted(links):
	for a in sorted(links[l]):
		rlinks.setdefault(a, [])
		rlinks[a].append(l)
#		print >>sys.stderr, l, a

#for a in sorted(rlinks.keys(), key=lambda x: len(rlinks[x]), reverse=True):
#	print len(rlinks[a]), a
#	for l in sorted(rlinks[a]):
#		print >>sys.stderr, a, l

for l in sorted(links):
	if l in rlinks:
		for a in sorted(rlinks[l]):
			if a != l:
				print a, l
