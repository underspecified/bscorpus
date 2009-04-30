#!/usr/bin/python2.5

#from __future__ import with_statement
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

def gr_print_feeds(url,header,FILE):
	reader_req = urllib2.Request(url,None,header)
	reader_resp = urllib2.urlopen(reader_req)
	reader_resp_content = reader_resp.read()
	print >>FILE, reader_resp_content

if (len(sys.argv)>3):
	fs = sys.argv[1]
	posts = int(sys.argv[2])
	iters = int(sys.argv[3])
else:
	fs = "gr-feeds"
	posts = 10000
	iters = 10

fmt = "%%s.%%0%dd.xml" % len(str(iters-1))
header = gr_mk_header(gr_auth('genronmappu@gmail.com','matsumoto'))
base_url = 'http://www.google.com/reader/atom/?n=%d' % posts
cont_url = base_url + '&c'

try:
	file = fmt % (fs,0)
	print >>sys.stderr, "Making file %s ..." % file
	FH = open(file,"w")
	gr_print_feeds(base_url,header,FH)
finally:
	FH.close()

for i in range(1,iters):
	try:
		file = fmt % (fs,i)
		print >>sys.stderr, "Making file %s ..." % file
		FH = open(file,"w")
		gr_print_feeds(cont_url,header,FH)
	finally:
		FH.close()