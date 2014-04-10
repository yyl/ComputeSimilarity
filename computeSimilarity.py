#!/usr/bin/python

import requests
import sys
import json
import nltk
from requests_oauthlib import OAuth1Session
from secrets import *

# nltk corpus download to /Users/yulongyang/nltk_data

## to write tweets into local file
def dumpTweets(tag, tweets):
    with open("%s.txt" % tag, "w+") as f:
        for tweet in tweets:
            f.write(tweet.encode('utf-8') + "\n")

## to decode incoming tweet
def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

## get tweets given the hashtag
def getTweets(tag):
	SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
	SEARCH_KEYS = {'language':'en', 'filter_level':'medium', 'result_type':'recent', 'q':'#%s' % tag, 'count':200}
	oauth = OAuth1Session(APP_KEY, client_secret=APP_SECRET,
                          resource_owner_key=ACCESS_TOKEN,
                          resource_owner_secret=ACCESS_TOKEN_SECRET)
	response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
	if response.status_code == 200:
		robj = response.json()
		tweets = [to_unicode_or_bust(tweet['text']) for tweet in robj['statuses']]
        dumpTweets(tag, tweets)

def main(tag1, tag2):
    ## get tweets for two tags
	#getTweets(tag1)
	#getTweets(tag2)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Duuuuuuuuuugh!!"
        print "Usage: ./computeSimilarity.py hashtag1 hashtag2"
        exit(0)
    main(sys.argv[1], sys.argv[2])
