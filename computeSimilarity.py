#!/usr/bin/python

from secrets import *
from utility import *

import requests
import sys
import os
import json
from collections import Counter
import itertools
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
from requests_oauthlib import OAuth1Session
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk corpus download to /Users/yulongyang/nltk_data

## tokenize tweets
## also apply stopwords removal and stemming
def getTokens(words):
    tokens = nltk.word_tokenize(words)
    '''
    ## stopwords removal
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    '''
    ## stemming
    stemmer = PorterStemmer()
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

## rip off directory stuff and suffix from the filename
def getTagName(filename):
    return os.path.basename(filename).rstrip(".txt")

## get words for each tag
## lower them down and remove punctuation
def getWords(tag):
    with open('%s.txt' % tag, 'r') as f: 
        text = f.read()
        lowers = text.lower()
    return lowers.translate(None, string.punctuation)

## given two docs, compute the similarity
def pairwiseSim(doc1, doc2):
    tfidf = TfidfVectorizer(tokenizer=getTokens, stop_words='english').fit_transform([doc1, doc2])
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity[0,1]


def main():
    token_dict = {}
    for filename in walker("tweets"):
        token_dict[filename] = open(filename, "r").read()
    for f1, f2 in itertools.combinations(token_dict.items(), 2):
        print "%10s %10s %5.15f" % (getTagName(f1[0]), getTagName(f2[0]), pairwiseSim(f1[1], f2[1]))

if __name__ == '__main__':
    main()
