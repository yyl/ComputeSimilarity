#!/usr/bin/python

'''
A script to plot
1. # of tweets vs. # of unique tokens
'''

from secrets import *
from utility import *
from computeSimilarity import getTokens, removeStopwords

import sys
import os
from collections import Counter, OrderedDict
import itertools
import string

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

TAGS = ["heartbleed", "ssl", "ladygaga", "justinbieber"]
TEST = ['ssl', 'heartbleed']

## plot the curve
## input: a dict of {# of tweets:# of unique tokens}
## output: a curve
def plotCurve(tokens):
    font = {'size': 12}
    plt.rc('font', **font)
    fig, ax = plt.subplots()
    p1, p2, p3, p4 = ax.plot(
            tokens['heartbleed'].keys(), tokens['heartbleed'].values(), 'r*--',
            tokens['ssl'].keys(), tokens['ssl'].values(), 'bs--',
            tokens['ladygaga'].keys(), tokens['ladygaga'].values(), 'g^--',
            tokens['justinbieber'].keys(), tokens['justinbieber'].values(), 'y*--')
    plt.legend((p1, p2, p3, p4), ('#heartbleed', '#ssl', '#ladygaga', '#justinbieber'), 'upper left', shadow=True)
    plt.title("The increasing curve of\n# of unique tokens v. # of tweets")
    plt.xlabel("Number of tweets per tag")
    plt.ylabel("Number of unique tokens per tag")
    fig.savefig('curve_of_tokens.png', bbox_inches=0)

## given tweets
## get the number of unique tokens
## along with the increase of the number of tweets processed
## step: 100, minimum 0 tweets, maximum 2000 tweets
def getIncreasingNumOfTokens(filepath):
    print "computing number of increasing tokens for %s..." % (filepath)
    num_tokens_steps = {0:0}
    # set the step for processing tweets
    steps = (i*100 for i in xrange(20))
    # read lines from the file according to the step
    for i in steps:
        with open(filepath) as ftweet:
            # read i lines of tweets
            lines = [ftweet.next().lower().translate(None, string.punctuation) for x in xrange(i)]
            # get # of unique tokens of the tokenized tweets
            # also remove rare tokens with only 1 occurrence
            num_tokens_steps[i] = len([w for w,n in Counter(removeStopwords(getTokens(''.join(lines)))).iteritems() if n != 1])
    # return sorted dict {# of tweets:# of unique tokens}
    return OrderedDict(sorted(num_tokens_steps.iteritems(), key=lambda t: t[0]))

## for all the tags
## compute the increasing curve of # of tokens v. # of tweets
## the generate the curve plot
def main(foldername):
    unique_tokens = {}
    for tag in TAGS:
        unique_tokens[tag] = getIncreasingNumOfTokens("%s/%s.txt" % (foldername, tag))
    plotCurve(unique_tokens)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Duuuuuuuuuugh!!!"
        print "Usage: python script.py foldername"
        sys.exit(0)
    main(sys.argv[1])
