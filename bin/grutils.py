#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import feedparser
from BeautifulSoup import BeautifulSoup, SoupStrainer
import socket, urllib2
import re
import cPickle

# timeout in seconds
timeout = 5
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

global blog, links, rlinks, tags, rtags, title, ua
blog = {}
links = {}
rlinks = {}
tags = {}
rtags = {}
title = {}
ua = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)"

def get_true_url(l):
	'''Get permalink by following any redirects.'''
	try:
		req = urllib2.Request(l, None, {'User-Agent' : ua})
		l = urllib2.urlopen(req).geturl()
#	except urllib2.HTTPError, err:
#		print >>sys.stderr, '\t', "The server couldn't fulfill the request."
#		print >>sys.stderr, '\t', 'Error code:', err.code
#	except urllib2.URLError, err:
#		print >>sys.stderr, '\t', 'We failed to reach a server.'
#		print >>sys.stderr, '\t', 'Reason:', err.reason
	except Exception, err:
		print >>sys.stderr, 'UH-OH! ^^;', err, l
		pass
	return l

def get_links(x):
	'''Retrieve links from blog posts in XML file.'''
	google_tags = set([u'fresh', u'read', u'reading-list'])
	anchors = SoupStrainer('a', href=re.compile('^http'))
	d = feedparser.parse(x)
	for e in d.entries:
		try:
			b = e.source.link # blog source
			i = e.title       # blog post title
			l = e.link        # link to blog post

			# try to get permalink by following redirects
#			print >>sys.stderr, "blog:", b, "link:", l
			if b.replace('http://', '').replace('www.', '') not in l:
				l = get_true_url(l)

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
				else:
					req = urllib2.Request(l, None, {'User-Agent' : ua})
					p = urllib2.urlopen(req).geturl()

				# parse the html
				s = BeautifulSoup(p, parseOnlyThese=anchors)
#				print >>sys.stderr, s.prettify()

				# index links in blog post summary
				links.setdefault(l, [])
				for a in s.findAll('a'):
					h = a['href']
#					h = get_true_url(h)
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
	all_blogs = frozenset([b for b in blog.values() if b])
	s = {}
	for l in _links:
		x = [b for b in all_blogs if b.replace('http://', '').replace('www.', '') in l]
		s[l] = x[0] if x else ''
#	print >>sys.stderr, s
	return s

def has_many_blogs(_links):
	'''Check if a set of links point to more than one known blogs.'''
#	if len(_links) < 2:
#		return False
	v = frozenset(get_blogs(_links).values())
#	print >>sys.stderr, v, len(frozenset(v))
#	return v == frozenset(['']) or len(v) > 1
	return len(v) > 1

def filter_rlinks():
	'''Throw away link spam and self-referential links.'''
	print >>sys.stderr, "Filtering rlinks ...",
	clinks = {}
	for l in rlinks:
		# only keep non-self-referential reverse links that are from different blogs
		c = rlinks[l]
#		print >>sys.stderr, has_many_blogs(c), c
		if has_many_blogs(c):
			clinks[l] = frozenset([x for x in c if x!=l and x not in blog.values()])
	print >>sys.stderr, "done!"
	return clinks

def print_rlinks():
	'''Print reverse links if they aren't self-refererential.'''
	clinks = filter_rlinks()
	for l in sorted(clinks, key=lambda x: len(frozenset(clinks[x])), reverse=True):
		d = frozenset(clinks[l])
		i = [title[i] for i in d if i in title]
		t = sorted(reduce(set.union, [tags[l]]+[tags[z] for z in d if z in tags]))
		print >>sys.stdout, len(d), get_title(l), l, i, t, d, frozenset(get_blogs(d).values()), has_many_blogs(d)

def pickle_data(f):
	'''Pickle data and store it to file.'''
	print >>sys.stderr, "Pickling ...",
	i = file(f, 'w')
	cPickle.dump((blog, links, rlinks, tags, rtags, title), i, 2)
	i.close()
	print >>sys.stderr, "done!"


def unpickle_data(f):
	'''Read data from file and unpickle it.'''
	print >>sys.stderr, "Unpickling ...",
	i = file(f, 'r')
	global blog, links, rlinks, tags, rtags, title
	blog, links, rlinks, tags, rtags, title = cPickle.load(i)
	i.close()
	print >>sys.stderr, "done!"
