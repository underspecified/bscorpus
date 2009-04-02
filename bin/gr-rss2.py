#!/usr/bin/python2.5

import urllib
import urllib2
import re

login = 'genronmappu@gmail.com'
password = 'matsumoto'
source = 'gPowered'

google_url = 'http://www.google.com'
reader_url = google_url + '/reader'
login_url = 'https://www.google.com/accounts/ClientLogin'
token_url = reader_url + '/api/0/token'
subscription_list_url = reader_url + '/api/0/subscription/list'
reading_url = reader_url + '/atom/user/-/state/com.google/reading-list'
read_items_url = reader_url + '/atom/user/-/state/com.google/read'
reading_tag_url = reader_url + '/atom/user/-/label/%s'
starred_url = reader_url + '/atom/user/-/state/com.google/starred'
subscription_url = reader_url + '/api/0/subscription/edit'
get_feed_url = reader_url + '/atom/feed/'