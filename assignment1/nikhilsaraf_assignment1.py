#!/usr/bin/python

import urllib
import json

response = urllib.urlopen("http://search.twitter.com/search.json?q=Twitter")
print json.load(response)
