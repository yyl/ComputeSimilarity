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

'''
A script to
1. compute similarity of pairs of Twitter hashtags
2. compute most common tokens for 2 documents
'''
## the amount of tweets proccessed, if any
AMOUNT = 4000

## bar plot
## input: a list of similarity scores associated with each pair of tags
## a bar plot of every score
def barplot(scores):
    font = {'size': 10}
    plt.rc('font', **font)
    fig, ax = plt.subplots()
    names = [item[0] for item in scores]
    y_pos = np.arange(len(names))
    plt.barh(y_pos, [item[1] for item in scores], align='center', alpha=0.4)
    plt.yticks(y_pos, names)
    plt.title('Similarity score of entities from %s tweets\nper tag w/o token "RT"\n' % AMOUNT)
    plt.tight_layout()
    fig.savefig('hashtag_similarity.png', bbox_inches=0)

## rip off directory stuff and suffix from the filename
def getTagName(filename):
    return os.path.basename(filename).rstrip(".txt")

## remove stopwords using nltk corpus
def removeStopwords(tokens):
    return (w for w in tokens if not w in stopwords.words('english'))

## given a string, remove all occurrence of rt
def removeRT(line):
    return line.translate(None, 'rt')

## tokenizer
## also apply stopwords removal and stemming
def getTokens(words):
    ## tokenize AND remove rt keyword
    #tokens = nltk.word_tokenize(words)
    tokens = (w for w in nltk.word_tokenize(words) if w != 'rt')
    ## stemming
    stemmer = PorterStemmer()
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

## given 2 docs (strings)
## 1. tokenize, remove stopwords
## 2. compute TFIDF for each token and form vectors
## 3. comptue and return pairwise consine similarity
def pairwiseSim(doc1, doc2):
    # get a vector of tfidf of tokens as features
    tfidf = TfidfVectorizer(tokenizer=getTokens, stop_words='english').fit_transform([doc1, doc2])
    # no need to normalize, since Vectorizer will return normalized tf-idf
    # compute the consine similarity of the 2 tfidf vector by dot multiplication
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity[0,1]

## given folder path
## read all files, lower all chars and remove punctuation
def getDocs(foldername):
    token_dict = {}
    # read all files into a dict
    # also lower all chars and remove punctuation
    for filename in walker(foldername):
        token_dict[filename] = open(filename, "r").read().lower().translate(None, string.punctuation)
    return token_dict

## given foldername, compute scores for each pair of tags in the folder
def getScores(foldername):
    scores = {}
    # iterate all combination of 2 tags
    for f1, f2 in itertools.combinations(getDocs(foldername).items(), 2):
        score = pairwiseSim(f1[1], f2[1])
        print "%15s %15s %5.5f" % (getTagName(f1[0]), getTagName(f2[0]), score)
        pair_name = "#%s v. #%s" % (getTagName(f1[0]), getTagName(f2[0]))
        scores[pair_name] = score
    # sort scores in descending
    return sorted(scores.iteritems(), key=lambda t:t[1])

## the main program to compute and plot similarity
def main(foldername):
    scores = getScores(foldername)
    barplot(scores)

## the main program for computing most common words
def main_mostCommon(foldername):
    tag_dict = getDocs(foldername)
    tokenized_dict = (( tag, removeStopwords(getTokens(f)) ) for tag, f in tag_dict.iteritems())
    common_words = (( getTagName(tag), Counter(tokens) ) for tag, tokens in tokenized_dict)
    print "%25s %20s %s" % ('tag name', '# of unique tokens', '10 most common tokens')
    for tag, common in common_words:
        print "%25s %20d %s" % (tag, len(common), common.most_common(10))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Duuuuuuuuuugh!!!"
        print "Usage: python script.py foldername"
        sys.exit(0)
    main(sys.argv[1])
    #main_mostCommon(sys.argv[1])
