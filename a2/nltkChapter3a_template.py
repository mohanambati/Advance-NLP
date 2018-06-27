from __future__ import division
import nltk, re, pprint

from urllib.request import urlopen

from nltk.book import *

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def exercise6():
    print("part b")
    print("not implemented")
    print("part c")
    print("not implemented")
    print("part f")
    print("not implemented")


def exercise7():
    print("part a")
    print("not implemented")


def exercise21():
    print("not implemented")
    

def exercise25():
    print("not implemented")


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(6)
    exercise(7)
    exercise(21)
    exercise(25)


if __name__ == "__main__":
    main()

