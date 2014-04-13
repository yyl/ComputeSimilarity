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
from collections import Counter
import itertools
import string

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

TAGS = ["heartbleed", "ssl", "ladygaga", "justinbieber"]
TEST = ['ssl']

def getIncreasingNumOfTokens(filepath):
    num_tokens_steps = {0:0}
    steps = (i*100 for i in xrange(20))
    # read lines from the file according to the step
    for i in steps:
        with open(filepath) as ftweet:
            lines = [ftweet.next().lower().translate(None, string.punctuation) for x in xrange(i)]
            num_tokens_steps[i] = len(Counter(removeStopwords(getTokens(''.join(lines)))))
    return num_tokens_steps

## for all the tags
## compute the increasing curve of # of tokens v. # of tweets
## the generate the curve plot
def main(foldername):
    unique_tokens = {}
    for tag in TAGS:
        unique_tokens[tag] = getIncreasingNumOfTokens("%s/%s.txt" % (foldername, tag))
    print unique_tokens

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Duuuuuuuuuugh!!!"
        print "Usage: python script.py foldername"
        sys.exit(0)
    main(sys.argv[1])
