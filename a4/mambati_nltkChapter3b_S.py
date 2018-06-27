
'''
Title : CSCI 8450 Assignment: Chapter 4
Written by : Mohan Sai Ambati
Date : 14 Feb 2018
Description:
This file contains solutions of exercises 29, 30, 40 in http://www.nltk.org/book/ch03.html
'''

from __future__ import division
import nltk
from nltk.book import *
from nltk.corpus import brown


SimpleText = 'One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def count_wh_words(text):
    wh_words = ['what', 'where', 'when', 'which', 'who', 'whom', 'whose', 'why']
    count = 0
    for word in text:
        if word.lower() in wh_words:
            count += 1
    return count

def exercise1():
    print("wh words in text2 : ", count_wh_words(text2))
    print("wh words in text7 : ", count_wh_words(text7))


def ARI_for_brown_corpus(ARI):
    for section in brown.categories():
        temp1 = [len(word) for word in brown.words(categories=section)]
        temp2 = [len(sent) for sent in brown.sents(categories=section)]
        ARI[section] = 4.71 * (sum(temp1) / len(temp1)) + 0.5 * (sum(temp2)/len(temp2)) - 21.43
    print("ARI result : \n")
    return ARI

def exercise29():
    print("Computing ARI for all sections in brown corpus .....")
    for section, ari in ARI_for_brown_corpus({'Section': 'ARI'}).items():
        print("{:>20} | {}".format(section, ari))


def exercise30():
    words = nltk.word_tokenize(SimpleText)
    porter = nltk.PorterStemmer()
    porter = [porter.stem(word) for word in words]
    lancaster = nltk.LancasterStemmer()
    lancaster = [lancaster.stem(word) for word in words]
    print("words in lancaster not in porter : ", set(lancaster) - set(porter))
    print("words in porter not in lancaster : ", set(porter) - set(lancaster))


def reading_difficulty_score(text, flag = False):
    temp1 = [len(word) for word in nltk.word_tokenize(text)]
    temp2 = []
    tokenize = nltk.sent_tokenize(text)
    if flag:
        print("Sentenses tokenized after using punkt : ", tokenize)
    for sent in tokenize:
        temp2.append(len(nltk.word_tokenize(sent)))
    return (4.71 * (sum(temp1) / len(temp1)) + 0.5 * (sum(temp2) / len(temp2)) - 21.43)

def exercise40():
    print("Computing the reading difficulty scores ...")
    rural = nltk.corpus.abc.raw('rural.txt')
    print("Reading difficulty of rural.txt : ", reading_difficulty_score(rural, False))
    science = nltk.corpus.abc.raw('science.txt')
    print("Reading difficulty of science.txt : ", reading_difficulty_score(science, False))


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise" + str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(29)
    exercise(30)
    exercise(40)


if __name__ == "__main__":
    main()

