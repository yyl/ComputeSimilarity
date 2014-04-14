#!/usr/bin/python

'''
A script to plot
1. # of tweets/entities vs. # of unique tokens
2. # of entities v. similarity scores
'''

from secrets import *
from utility import *
from computeSimilarity import getTokens, removeStopwords, pairwiseSim

import sys
import os
from collections import Counter, OrderedDict
import itertools
import string

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

TAGS = ["heartbleed", "ssl", "ladygaga", "justinbieber"]
SCORE_TAGS = [("heartbleed", "ssl"), ("ladygaga", "justinbieber"), ("nba", "ncaa")]
TEST = ['ssl', 'heartbleed']

## plot the curve
## input: a dict of {# of tweets:# of unique tokens}
## output: a curve
def plotCurve(tokens, mytitle, myxlabel, myylabel):
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 20)])
    legends = []
    font = {'size': 12}
    plt.rc('font', **font)
    fig, ax = plt.subplots()
    for tag, token in tokens.iteritems():
        plt.plot(token.keys(), token.values())
        legends.append(tag)
    plt.legend(legends, 'upper right', shadow=True)
    plt.title(mytitle)
    plt.xlabel(myxlabel)
    plt.ylabel(myylabel)
    fig.savefig('curve.png', bbox_inches=0)

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

## given tweets
def getIncreasingScores(filepath, pair):
    print "computing scores of increasing tokens for %s..." % (filepath)
    num_tokens_steps = {0:0}
    # set the step for processing tweets
    steps = (i*100 for i in xrange(1, 61))
    # read lines from the file according to the step
    for i in steps:
        with open("%s/%s.txt" % (filepath, pair[0])) as f1:
            with open("%s/%s.txt" % (filepath, pair[1])) as f2:
                lines1 = (f1.next().lower().rstrip().translate(None, string.punctuation) for x in xrange(i))
                lines2 = (f2.next().lower().rstrip().translate(None, string.punctuation) for x in xrange(i))
                num_tokens_steps[i] = pairwiseSim(' '.join(lines1), ' '.join(lines2))
    # return sorted dict {# of tweets:score}
    return OrderedDict(sorted(num_tokens_steps.iteritems(), key=lambda t: t[0]))

## for all the tags
## compute the increasing curve of # of tokens v. # of tweets
## the generate the curve plot
def main(foldername):
    unique_tokens = {}
    for pair in SCORE_TAGS:
        #unique_tokens[tag] = getIncreasingNumOfTokens("%s/%s.txt" % (foldername, tag))
        unique_tokens["%s v %s" % (pair[0], pair[1])] = getIncreasingScores(foldername, pair)
    plotCurve(unique_tokens, "Curve of # of entities processed v. score", "# of entities processed", "similarity score")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Duuuuuuuuuugh!!!"
        print "Usage: python script.py foldername"
        sys.exit(0)
    main(sys.argv[1])
