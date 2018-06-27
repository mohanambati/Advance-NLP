import nltk, re, pprint

from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.book import *
from nltk import memoize

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc

from timeit import Timer

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def exercise0():
    print('not implemented')


def recursive_catalan(n):
    print('not implemented')

def dynamic_catalan(n):
    print('not implemented')

def exercise26():
    # Example of timer usage:
    # print(Timer(lambda: recursive_catalan(n)).timeit(1))
    print('not implemented')

 	
    

def exercise32():
    print('not implemented')


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(0)
    exercise(26)
    exercise(32)


if __name__ == "__main__":
    main()

