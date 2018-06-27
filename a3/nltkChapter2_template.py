import nltk, re, pprint

from nltk.book import *

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn


def exercise2():
    print("not implemented")


def exercise5():
    print("not implemented")


def exercise9():
    print("not implemented")


def exercise11():
    print("not implemented")


def exercise13():
    print("not implemented")


def exercise18():
    print("not implemented")


def exercise27():
    print("not implemented")


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(2)
    exercise(5)
    exercise(9)
    exercise(11)
    exercise(13)
    exercise(18)
    exercise(27)


if __name__ == "__main__":
    main()

