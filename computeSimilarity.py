#!/usr/bin/python

import requests
import sys
import json
from requests_oauthlib import OAuth1Session
from secrets import *

def getTweets(tag):
	SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
	SEARCH_KEYS = {'language':'en', 'filter_level':'medium', 'result_type':'recent', 'q':'#%s' % tag, 'count':10}
	oauth = OAuth1Session(APP_KEY, client_secret=APP_SECRET,
                          resource_owner_key=ACCESS_TOKEN,
                          resource_owner_secret=ACCESS_TOKEN_SECRET)
	response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
	if response.status_code == 200:
		robj = response.json()
		return [tweet.text for tweet in robj['statuses']]

def main(tag1, tag2):
	tweets1 = getTweets(tag1)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Duuuuuuuuuugh!!"
        print "Usage: ./computeSimilarity.py hashtag1 hashtag2"
		exit(0)
	main(sys.argv[1], sys.argv[2])
