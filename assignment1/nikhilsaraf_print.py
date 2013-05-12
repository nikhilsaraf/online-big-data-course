#!/usr/bin/python

import urllib
import json


for page in range(1,11):
	raw_response = urllib.urlopen("http://search.twitter.com"
	               + "/search.json?q=Twitter&page=" + str(page))
	json_object = json.load(raw_response)
	print "Page: " + str(page)	
	for tweet in json_object['results']:
		print tweet['text']
		print ""
