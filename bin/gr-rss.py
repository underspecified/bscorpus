#!/usr/bin/python2.5

import urllib
import urllib2

username = 'genronmappu@gmail.com'
password = 'matsumoto'

# Authenticate to obtain SID
auth_url = 'https://www.google.com/accounts/ClientLogin'
auth_req_data = urllib.urlencode({'Email': username,
                                  'Passwd': password})
auth_req = urllib2.Request(auth_url, data=auth_req_data)
auth_resp = urllib2.urlopen(auth_req)
auth_resp_content = auth_resp.read()
auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
SID = auth_resp_dict["SID"]

# Create a cookie in the header using the SID 
header = {}
header['Cookie'] = 'Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID

#reader_base_url = 'http://www.google.com/reader/api/0/subscription/list?%s'
reader_base_url = 'http://www.google.com/reader/atom/?n=100000'
reader_req_data = urllib.urlencode({'all': 'false', 
									'output': 'xml'})
reader_url = reader_base_url #% (reader_req_data)
reader_req = urllib2.Request(reader_url, None, header)
reader_resp = urllib2.urlopen(reader_req)
reader_resp_content = reader_resp.read()

print reader_resp_content
