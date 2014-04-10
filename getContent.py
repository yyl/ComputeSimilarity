#!/usr/bin/python
from utility import *
import requests
import json
import string
from requests_oauthlib import OAuth1Session
from secrets import *

'''
return a list of hashtags from trending topics
'''
TRENDS_URL = 'https://api.twitter.com/1.1/trends/place.json'
PARAMS = {'language':'en', 'filter_level':'medium', 'id':1}
SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
SEARCH_KEYS = {'language':'en', 'filter_level':'medium', 'result_type':'recent', 'count':100}
oauth = OAuth1Session(APP_KEY, client_secret=APP_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)

## to write tweets into local file
def dumpTweets(tag, tweets):
    with open("tweets/%s.txt" % tag.lstrip('#'), "w+") as f:
        for tweet in tweets:
            f.write(tweet.encode('utf-8') + "\n")

## get tweets given the hashtag
def getTweets(tag):
    SEARCH_KEYS['q'] = tag
    response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
    if response.status_code == 200:
        robj = response.json()
        tweets = [decode_to_unicode(tweet['text']) for tweet in robj['statuses']]
        dumpTweets(tag, tweets)

def getTags():
    response = oauth.get(TRENDS_URL, params=PARAMS)
    if response.status_code == 200:
        robj = response.json()
        trends = (decode_to_unicode(trend['name']) for trend in robj[0]['trends'] if trend['name'].startswith('#'))
        with open("tags.txt", "r") as f:
            new_trends = (trend for trend in trends if trend not in f.read())
        with open("tags.txt", "a+") as f:
            for t in new_trends:
                f.write(t.encode('utf-8') + '\n')

def main():
    #getTags()
    for line in open("tags.txt", "r"):
        getTweets(line.rstrip())

if __name__ == '__main__':
    main()
