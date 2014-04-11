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
FILTER_URL = 'https://stream.twitter.com/1.1/statuses/sample.json'
FILTER_PARAMS = {'language':'en', 'filter_level':'medium'}
oauth = OAuth1Session(APP_KEY, client_secret=APP_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)
AMOUNT = 100

## to write tweets into local file
def dumpTweets(tag, tweets):
    with open("tweets%s/%s.txt" % (AMOUNT, tag.lstrip('#')), "a+") as f:
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

## get tweets given the hashtag
def getMoreTweets(tag):
    print "Getting more tweets for %s..." % tag
    SEARCH_KEYS['q'] = tag
    count = 0
    response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
    while count < AMOUNT:
        response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
        if response.status_code == 200:
            robj = response.json()
            tweets = (decode_to_unicode(tweet['text']) for tweet in robj['statuses'])
            dumpTweets(tag, tweets)
            ids = (int(tweet.get('id')) for tweet in robj['statuses'])
            SEARCH_KEYS['max_id'] = min(ids) - 1
            count += 100
            if count%500 == 0:
                print "getting %s tweets..." % count

'''
## use streaming API to get more tweets per tag
def getMoreTweets(tag):
    print "Getting more tweets for %s..." % tag
    THRESHOLD = 500
    FILTER_PARAMS['track'] = tag
    restream = oauth.get(FILTER_URL, stream=True, params=FILTER_PARAMS)
    count = 0
    tweets = []
    for line in restream.iter_lines():
        if line:
            tweet = json.loads(line).get(u'text', False)
            if tweet:
                count += 1
                tweets.append(decode_to_unicode(tweet))
                print tweet
            if count%100 == 0:
                print "getting %s tweets..." % count
            if count == THRESHOLD:
                break
    dumpTweets(tag, tweets)
'''

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
        getMoreTweets(line.rstrip())

if __name__ == '__main__':
    main()
