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

cont_re = re.compile(r'<gr:continuation>(.+)</gr:continuation>')
def get_cont(content):
	m = cont_re.search(content)
	if m:
		return m.group(1)
        else:
                return None

def get_feeds(base_url, header):
        cont_url = base_url
        while True:
                try:
                        request = urllib2.Request(cont_url, None, header)
                        response = urllib2.urlopen(request)
                        content = response.read()
                        yield content
                        cont = get_cont(content)
                        if not cont: break
                        cont_url = '%s&c=%s' % (base_url, cont)
                        #print >>sys.stderr, 'cont_url: %s' % cont_url
                except Exception as err:
                        print >>sys.stderr, 'Error getting feeds! >_<', err
                        raise err

def main():
        fs = 'gr_feeds'
        posts = 1000
        if (len(sys.argv) >= 1):
                fs = sys.argv[1]
        if (len(sys.argv) > 2):
                posts = int(sys.argv[2])
        fmt = '%%s.%%0%dd.xml' % 3
        header = gr_auth('genronmappu@gmail.com', 'matsumoto')
        #print >>sys.stderr, 'header:', header
        base_url = 'https://www.google.com/reader/atom/?n=%d' % posts
        for i, feed in enumerate(get_feeds(base_url, header)):
                file = fmt % (fs, i)
                print >>sys.stderr, 'Making file %s ...' % file
                with open(file, 'w') as fh:
                        print >>fh, feed

if __name__ == '__main__':
        main()
