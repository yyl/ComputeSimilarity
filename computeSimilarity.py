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

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# nltk corpus download to /Users/yulongyang/nltk_data
AMOUNT = 2000
## bar plot
def barplot(scores):
    font = {'size': 10}
    plt.rc('font', **font)
    fig, ax = plt.subplots()
    names = [item[0] for item in scores]
    y_pos = np.arange(len(names))
    plt.barh(y_pos, [item[1] for item in scores], align='center', alpha=0.4)
    plt.yticks(y_pos, names)
    plt.title('Similarity score based on tokenized tfidf scores with %s tweets per tag' % AMOUNT)
    plt.tight_layout()
    fig.savefig('hashtag_similarity%s.png' % AMOUNT, bbox_inches=0)

## rip off directory stuff and suffix from the filename
def getTagName(filename):
    return os.path.basename(filename).rstrip(".txt")

## tokenizer
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

## get words for each tag
## lower them down and remove punctuation
def getWords(tag):
    with open('%s.txt' % tag, 'r') as f: 
        text = f.read()
        lowers = text.lower()
    return lowers.translate(None, string.punctuation)

## given two docs, compute the similarity
## D<w1, w2, ...> and cosine similarity
def pairwiseSim(doc1, doc2):
    tfidf = TfidfVectorizer(tokenizer=getTokens, stop_words='english').fit_transform([doc1, doc2])
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity[0,1]

def getScores(foldername):
    scores = {}
    token_dict = {}
    for filename in walker(foldername):
        token_dict[filename] = open(filename, "r").read().lower().translate(None, string.punctuation)
    for f1, f2 in itertools.combinations(token_dict.items(), 2):
        score = pairwiseSim(f1[1], f2[1])
        print "%10s %10s %5.5f" % (getTagName(f1[0]), getTagName(f2[0]), score)
        pair_name = "#%s v. #%s" % (getTagName(f1[0]), getTagName(f2[0]))
        scores[pair_name] = score
    # sort scores based on score
    return sorted(scores.iteritems(), key=lambda t:t[1])

def main():
    scores = getScores("tweets%s" % AMOUNT)
    barplot(scores)

if __name__ == '__main__':
    main()
