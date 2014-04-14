#!/usr/bin/python
from utility import *
import requests
import json
import string
from requests_oauthlib import OAuth1Session
from secrets import *
'''
A script utilize Twitter API to
1. obtain tweet texts given a tag
2. obtain entities of tweets associated with the given tag
3. obtain trending hashtags given WOID of the location

For the first 2 functions It reads tags from the file 'tags.txt'

NYC woid for trend topic
[{u'name': u'New York', u'countryCode': u'US', u'url': u'http://where.yahooapis.com/v1/place/2459115', u'country': u'United States', u'parentid': 23424977, u'placeType': {u'code': 7, u'name': u'Town'}, u'woeid': 2459115}]
'''

## some global variables
TRENDS_URL = 'https://api.twitter.com/1.1/trends/place.json'
TRENDS_PARAMS = {'language':'en', 'filter_level':'medium', 'id':2459115}
SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
SEARCH_KEYS = {'language':'en', 'filter_level':'medium', 'result_type':'recent', 'count':100}
oauth = OAuth1Session(APP_KEY, client_secret=APP_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)
## the amount of tweets crawled per tag
AMOUNT = 4000

## given a list of tweet texts, write tweets into local file
## filename is the tag without #
def dumpTweets(tag, tweets, foldername):
    # check the dir, create it if not exsit
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    # create a file named with the tag
    # write every tweet into the file
    with open("%s/%s.txt" % (foldername, tag.lstrip('#')), "a+") as f:
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

## given AMOUNT, get large amount of tweets given the hashtag
## by continuously pulling from API and keeping track of max_id
## also obtain all entities from the tweets
def getMoreTweets(tag):
    print "Getting more tweets for %s..." % tag
    SEARCH_KEYS['q'] = tag
    count = 0
    response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
    while count < AMOUNT:
        response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
        if response.status_code == 200:
            robj = response.json()
            # decode and get tweet text
            tweets = (decode_to_unicode(tweet['text']) for tweet in robj['statuses'])
            dumpTweets(tag, tweets, "tweets%d" % AMOUNT)
            ids = (int(tweet.get('id')) for tweet in robj['statuses'])
            # keep track of max_id to avoid repeat task
            SEARCH_KEYS['max_id'] = min(ids) - 1
            count += 100
            # log progress
            if count%500 == 0:
                print "getting %s tweets..." % count

## similar to getMoreTweets but only obtain all entities from the tweets
def getMoreEntities(tag):
    print "Getting entities of %d tweets for %s..." % (AMOUNT, tag)
    # specify the querying tag
    SEARCH_KEYS['q'] = tag
    # keep track of tweets processed
    count = 0
    response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
    while count < AMOUNT:
        response = oauth.get(SEARCH_URL, params=SEARCH_KEYS)
        if response.status_code == 200:
            robj = response.json()
            # try to get all entities
            group_entities = (decode_to_unicode(tweet['entities'] for tweet in robj['statuses']))
            # get all hashtags
            hashtags = (item for hashtag_list in (entities.get('hashtags', []) for entities in group_entities) for item in hashtag_list)
            hashtag_texts = (hasht.get('text', '') for hasht in hashtags)
            dumpTweets(tag, hashtag_texts, "entities2000")
            # get all user mentions
            mentions = (item for mention_list in (entities.get('user_mentions', []) for entities in group_entities) for item in mention_list)
            mention_texts = (mentiont.get('name', '') for mentiont in mentions)
            dumpTweets(tag, mention_texts, "entities")
            # keep track of max_id to avoid repeat pulling
            ids = (int(tweet.get('id', 0)) for tweet in robj['statuses'])
            earliest = min(ids)
            if earliest == 0:
                print "no more tweets for %s" % tag
                break
            SEARCH_KEYS['max_id'] = earliest - 1
            count += 100
            # log progress
            if count%500 == 0:
                print "processing %s tweets..." % count

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

## get tags from trending topics
def getTags():
    response = oauth.get(TRENDS_URL, params=TRENDS_PARAMS)
    if response.status_code == 200:
        robj = response.json()
        # choose only hashtags from trending topics
        trends = (decode_to_unicode(trend['name']) for trend in robj[0]['trends'] if trend['name'].startswith('#'))
        # write them into trends.txt file
        with open("trends.txt", "w+") as f:
            for t in trends:
                f.write(t.encode('utf-8') + '\n')

def main():
    getTags()
    for line in open("trends.txt", "r"):
        getMoreEntities(line.rstrip())
        #getMoreTweets(line.rstrip())

if __name__ == '__main__':
    main()
