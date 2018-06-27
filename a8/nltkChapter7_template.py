from __future__ import division
import nltk, re, pprint

from urllib.request import urlopen

from nltk.book import *

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc


def exercise1():
    print('not implemented')


def exercise2():
    print('not implemented')


def exercise3():
    print('not implemented')


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(2)
    exercise(3)


if __name__ == "__main__":
    main()

