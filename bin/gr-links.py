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
blog = {}
tags = {}
rtags = {}
title = {}

anchors = SoupStrainer('a', href=re.compile('http'))
def get_links(x):
	'''Retrieve links from blog posts in XML file.'''
	d = feedparser.parse(x)
	for e in d.entries:
		try:
			l = e.link # link to blog post
			b = e.source.link # blog source
			i = e.title # blog post title

			# try to get permalink by following redirects
			try:
				if b not in l:
					l = urllib2.urlopen(l).geturl()
			except Exception, err:
				pass
	
			try:	
				blog[l] = b
				title[l] = i
				tags[l] = set([t.label or t.term for t in e.tags if t.label or t.term]) 
				tags[l] -= set([u'fresh', u'reading-list'])
#				print >>sys.stderr, tags[l]
				for t in tags[l]:
					rtags.setdefault(t, set())
					rtags[t].add(l)
				links.setdefault(l, [])

				# get blog post summary by trying several RSS aliases
				p = None
				if 'summary' in e:
					p = e.summary
				elif 'subtitle' in e:
					p = e.subtitle
				elif 'content' in e and 'value' in e.content:
					p = e.content.value
#				else:
#					p = urllib2.urlopen(l)

				# parse the html
				s = BeautifulSoup(p, parseOnlyThese=anchors)
#				print >>sys.stderr, s.prettify()

				for a in s.findAll('a'):
					h = a['href']
					links[l].append(h)
					rlinks.setdefault(h, [])
					rlinks[h].append(l)
					blog.setdefault(h, '')
					tags.setdefault(h, set())
#					print >>sys.stderr, h

				print >>sys.stderr, "WIN! \(^o^)/", l

			except Exception, err:
				print >>sys.stderr, "FAIL! >_<", err, l
	
		except Exception, err:
			print >>sys.stderr, "EPIC FAIL! Orz", err, e.id

def fmt_rlinks():
	'''Throw away link spam and self-referential links.'''
	for l in rlinks:
		# only keep non-self-referential reverse links that are from different blogs
		rlinks[l] = set([x for x in rlinks[l] if x!=l and blog[x]!=blog[l]])

def print_rlinks():
	'''Print reverse links if they aren't self-refererential.'''
	for l in sorted(rlinks, key=lambda x: len(rlinks[x]), reverse=True):
		d = rlinks[l]
		i = [title[i] for i in d if i in title]
		t = sorted(reduce(set.union, [tags[l]]+[tags[z] for z in d if z in tags]))
		if len(d) > 1:
			print >>sys.stdout, len(d), l, d, i, t

if len(sys.argv) > 1:
	for x in sys.argv[1:]:
		get_links(x)
	fmt_rlinks()
	print_rlinks()
else:
	print >>sys.stderr, 'usage: pr-links.py <rss-feed.xml> [<rss-feed.xml> ...]'
