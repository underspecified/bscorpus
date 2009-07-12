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
		return s.title.string.replace('\n',' ').replace('\r',' ').strip()
	except Exception, err:
		return ''

blog = {}
links = {}
rlinks = {}
tags = {}
rtags = {}
title = {}

google_tags = frozenset([u'fresh', u'read', u'reading-list'])
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
				tags[l] = frozenset([t.label or t.term for t in e.tags if t.label or t.term]) - google_tags
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

def get_blogs(_links):
	'''Return the blogs each link in a set is from, if it is identifiable.'''
#	for l in _links:
#		print >>sys.stderr, l
#		for b in set([b for b in blog.values() if b]):
#			print >>sys.stderr, "\t", b, b in l
	all_blogs = frozenset([b for b in blog.values() if b])
#	s = [b for b in all_blogs for l in _links if b in l]
#	print >>sys.stderr, s
	s = {}
	for l in _links:
		s[l] = frozenset([b for b in all_blogs if b in l])
#	print >>sys.stderr, s
	return s

def has_many_blogs(_links):
	'''Check if a set of links point to more than one known blogs.'''
	if len(_links) < 2:
		return False
	v = get_blogs(_links).values()
#	print >>sys.stderr, v, len(frozenset(v))
	return v == [frozenset([])] or len(frozenset(v))>1

def filter_rlinks():
	'''Throw away link spam and self-referential links.'''
	clinks = dict(rlinks)
	for l in clinks:
		# only keep non-self-referential reverse links that are from different blogs
		c = frozenset(clinks[l])
#		print >>sys.stderr, has_many_blogs(c), c
		if has_many_blogs(c):
			rlinks[l] = frozenset([x for x in c if x!=l])
		else:
			del rlinks[l]

def print_rlinks():
	'''Print reverse links if they aren't self-refererential.'''
	for l in sorted([l for l in rlinks if l not in blog.values()],
					key=lambda x: len(rlinks[x]), reverse=True):
		d = frozenset(rlinks[l])
		i = [title[i] for i in d if i in title]
		t = sorted(reduce(set.union, [tags[l]]+[tags[z] for z in d if z in tags]))
		print >>sys.stdout, len(d), get_title(l), l, i, t, d

if len(sys.argv) > 1:
	for x in sys.argv[1:]:
		get_links(x)
	filter_rlinks()
	print_rlinks()
else:
	print >>sys.stderr, 'usage: pr-links.py <rss-feed.xml> [<rss-feed.xml> ...]'
