#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re

# utf-8 i/o plz!
import sys
import codecs 
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getwriter('utf-8')(sys.stdin)

links = {}
rlinks = {}
blogs = {}

t = SoupStrainer('a', href=re.compile('http'))
def get_links(x):
	'''Retrieve links from blog posts in XML file.'''
	d = feedparser.parse(x)
	for e in d.entries:
		try:
			l = e.link
			b = e.source.link
			
			try:
				blogs.setdefault(l, set())
				blogs[l].add(b)
				links.setdefault(l, [])

				p = None
				if 'summary' in e:
					p = e.summary
				elif 'subtitle' in e:
					p = e.subtitle
				elif 'content' in e and 'value' in e.content:
					p = e.content.value
#				else:
#					p = urllib2.urlopen(l)
				s = BeautifulSoup(p, parseOnlyThese=t)
#				print >>sys.stderr, s.prettify()

				for a in s.findAll('a'):
					h = a['href']
					links[l].append(h)
					rlinks.setdefault(h, [])
					rlinks[h].append(l)
					blogs.setdefault(h, set())
					blogs[h].add(b)
#					print >>sys.stderr, h

				print >>sys.stderr, "WIN! \(^o^)/", l

			except Exception, err:
				print >>sys.stderr, "FAIL! >_<", err, l
	
		except Exception, err:
			print >>sys.stderr, "EPIC FAIL! Orz", err, e.id

def fmt_rlinks():
	'''Throw away link spam and self-referential links.'''
	for l in rlinks:
		rlinks[l] = set([x for x in rlinks[l] if blogs[x]!=blogs[l] and x!=l])

def print_rlinks():
	'''Print reverse links if they aren't self-refererential.'''
	for l in sorted(set(rlinks), key=lambda x: len(rlinks[x]), reverse=True):
		d = rlinks[l]
		if len(d) > 0:
			print >>sys.stdout, len(d), l, d

if len(sys.argv) > 1:
	for x in sys.argv[1:]:
		get_links(x)
	fmt_rlinks()
	print_rlinks()
else:
	print >>sys.stderr, 'usage: pr-links.py <google-reader.xml> [<google-reader.xml> ...]'
