#!/usr/bin/python2.7

import re
import sys
import urllib
import urllib2

def gr_auth(user, passwd):
	'''Authenticate to obtain Auth token'''
	#auth_url = 'https://accounts.google.com/o/oauth2/auth'
	#auth_req_data = urllib.urlencode(
	#	{'client_id': '985064621815.apps.googleusercontent.com', }
        #)
	auth_url = 'https://www.google.com/accounts/ClientLogin'
	auth_req_data = urllib.urlencode(
                {'Email':user, 'Passwd':passwd, 'service':'reader', 
                 'continue':'http://www.google.com/',
                 'accountType': 'HOSTED_OR_GOOGLE'}
        )
	auth_req = urllib2.Request(auth_url, data=auth_req_data)
	auth_resp = urllib2.urlopen(auth_req)
	auth_resp_content = auth_resp.read()
	auth = dict(
                x.split('=') 
                for x in auth_resp_content.split('\n') 
                if x
        )
        #print >>sys.stderr, 'auth:', auth
        return {'Authorization': 'GoogleLogin auth=%s' % auth['Auth']}

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
		cont_url = "%s&c=%s" % (url,cont)
		print >>sys.stderr, "\tcont_url: %s" % cont_url
		return cont_url
	return None

def main():
        fs = "gr-feeds"
        posts = 1000
        iters = 10
        if (len(sys.argv)>=1):
                fs = sys.argv[1]
        if (len(sys.argv)>2):
                posts = int(sys.argv[2])
        fmt = "%%s.%%0%dd.xml" % 2
        header = gr_auth('genronmappu@gmail.com', 'matsumoto')
        print >>sys.stderr, 'header:', header
        base_url = 'https://www.google.com/reader/atom/?n=%d' % posts
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

if __name__ == '__main__':
        main()
