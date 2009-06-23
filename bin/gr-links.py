#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re
import os

# utf-8 i/o plz!
import sys
import codecs 
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getwriter('utf-8')(sys.stdin)

links = {}
rlinks = {}

t = SoupStrainer('a', href=re.compile('http'))
def get_links(x):
	'''Retrieve links from blog posts in XML file.'''
	d = feedparser.parse(x)
	for e in d.entries:
		try:
			l = e.link
			p = urllib2.urlopen(l)
			links.setdefault(l, [])
	
			s = BeautifulSoup(p, parseOnlyThese=t)
#			print >>sys.stderr, s.prettify()
			for a in s.findAll('a'):
				h = a['href']
				links[l].append(h)
				rlinks.setdefault(h, [])
				rlinks[h].append(l)
#				print >>sys.stderr, h
	
			print >>sys.stderr, "WIN! \(^o^)/", e.link
	
		except Exception, err:
			print >>sys.stderr, "FAIL! >_<", err, e.link

def print_links():
	'''Print links with counts.'''
	for a in sorted(rlinks.keys(), key=lambda x: len(rlinks[x]), reverse=True):
		print len(rlinks[a]), a
#		for l in sorted(rlinks[a]):
#			print >>sys.stderr, a, l

def print_rlinks():
	'''Print reverse links if they aren't self-refererential.'''
	for l in sorted(links):
		if l in rlinks:
			for a in sorted(rlinks[l]):
				if a != l:
					print a, l

#bshome = '%s/bscorpus' % os.environ['HOME']
#x = '%s/data/test/gr-test.xml' % bshome
#x = '%s/data/gr/gr-feeds.00.xml' % bshome

if len(sys.argv) > 1:
	for x in sys.argv[1:]:
		get_links(x)
	print_links()
	print_rlinks()
else:
	print >>sys.stderr, 'usage: pr-links.py <google-reader.xml> [<google-reader.xml> ...]'
