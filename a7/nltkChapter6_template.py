from __future__ import division
import nltk, re, pprint

from urllib.request import urlopen

from nltk.book import *

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc


def exercise2():
    print('not implemented')


def exercise4():
    print('not implemented')


def exercise7():
    print('not implemented')


def exercise0():
    print('not implemented')


def exercise9():
    print('Extra Credit')
    print('not implemented')


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(2)
    exercise(4)
    exercise(7)
    exercise(0)
    exercise(9)


if __name__ == "__main__":
    main()

