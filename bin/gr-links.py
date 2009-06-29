#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import socket, urllib2
import re

# timeout in seconds
timeout = 3
socket.setdefaulttimeout(timeout)

# utf-8 i/o plz!
import sys
import codecs 
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getwriter('utf-8')(sys.stdin)

titles = SoupStrainer('title')
def get_title(h):
	'''Retrieve title of a web page.'''
	try:
		s = BeautifulSoup(urllib2.urlopen(h), parseOnlyThese=titles)
		return s.title.string.strip()
	except Exception, err:
		return ''

blog = {}
links = {}
rlinks = {}
tags = {}
rtags = {}
title = {}

google_tags = set([u'fresh', u'read', u'reading-list'])
anchors = SoupStrainer('a', href=re.compile('http'))

def get_links(x):
	'''Retrieve links from blog posts in XML file.'''
	d = feedparser.parse(x)
	for e in d.entries:
		try:
			b = e.source.link # blog source
			i = e.title       # blog post title
			l = e.link        # link to blog post

			# try to get permalink by following redirects
			try:
				if b not in l: l = urllib2.urlopen(l).geturl()
			except Exception, err:
				pass

			try:	
				blog[l] = b
				tags[l] = set([t.label or t.term for t in e.tags if t.label or t.term]) - google_tags
#				print >>sys.stderr, tags[l]
				for t in tags[l]:
					rtags.setdefault(t, set())
					rtags[t].add(l)
				title[l] = i

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

				# index links in blog post summary
				links.setdefault(l, [])
				for a in s.findAll('a'):
					h = a['href']
					blog.setdefault(h, '')
					links[l].append(h)
					rlinks.setdefault(h, [])
					rlinks[h].append(l)
					tags.setdefault(h, set())
#					title.setdefault(h, get_title(h))
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
	for l in sorted([l for l in rlinks if l not in blog.values()],
					key=lambda x: len(rlinks[x]), reverse=True):
		d = rlinks[l]
		i = [title[i] for i in d if i in title]
		t = sorted(reduce(set.union, [tags[l]]+[tags[z] for z in d if z in tags]))
		if len(d) > 1:
			print >>sys.stdout, len(d), get_title(l), l, i, t, d

if len(sys.argv) > 1:
	for x in sys.argv[1:]:
		get_links(x)
	fmt_rlinks()
	print_rlinks()
else:
	print >>sys.stderr, 'usage: pr-links.py <rss-feed.xml> [<rss-feed.xml> ...]'
