#!/usr/bin/python2.5

#from __future__ import with_statement
import re
import sys
import urllib
import urllib2

def gr_auth(user, passwd):
	'''Authenticate to obtain SID'''
	auth_url = 'https://www.google.com/accounts/ClientLogin'
	auth_req_data = urllib.urlencode({'Email':user,'Passwd':passwd})
	auth_req = urllib2.Request(auth_url, data=auth_req_data)
	auth_resp = urllib2.urlopen(auth_req)
	auth_resp_content = auth_resp.read()
	auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
	SID = auth_resp_dict["SID"]
	return SID

def gr_mk_header(SID):
	'''Create a cookie in the header using the SID'''
	header = {}
	header['Cookie'] = 'Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID
	return header

def get_cont(content):
	m = re.search(r'<gr:continuation>(.+)</gr:continuation>',content)
	if m:
		return m.group(1)
	return None

def gr_print_feeds(url,header,FILE):
	reader_req = urllib2.Request(url,None,header)
	reader_resp = urllib2.urlopen(reader_req)
	reader_resp_content = reader_resp.read()
	print >>FILE, reader_resp_content
	cont = get_cont(reader_resp_content)
	if cont:
		cont_url = "%s&c=%s" % (base_url,cont)
		print >>sys.stderr, "\tcont_url: %s" % cont_url
		return cont_url
	return None

fs = "gr-feeds"
posts = 1000
iters = 10
if (len(sys.argv)>2):
	fs = sys.argv[1]
if (len(sys.argv)>3):
	posts = int(sys.argv[2])

fmt = "%%s.%%0%dd.xml" % 2
header = gr_mk_header(gr_auth('genronmappu@gmail.com','matsumoto'))
base_url = 'http://www.google.com/reader/atom/?n=%d' % posts

i = 0
try:
	file = fmt % (fs,i)
	print >>sys.stderr, "Making file %s ..." % file
	FH = open(file,"w")
	cont_url = gr_print_feeds(base_url,header,FH)
	i = i+1
finally:
	FH.close()

#for i in range(1,iters):
while(cont_url):
	try:
		file = fmt % (fs,i)
		print >>sys.stderr, "Making file %s ..." % file
		FH = open(file,"w")
		cont_url = gr_print_feeds(cont_url,header,FH)
		i = i+1
	finally:
		FH.close()
