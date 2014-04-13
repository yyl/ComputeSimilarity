'''
A set of utility functions
'''

import os

## to decode incoming tweet
def decode_to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

# a generator that returns every filepath in the given folder one by one
def walker(fpath):
    for dirname, dirnames, filenames in os.walk(fpath):
        # print path to all filenames.
        for filename in filenames:
            if filename.endswith('.txt'):
                yield os.path.join(dirname, filename)
