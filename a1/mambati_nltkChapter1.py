'''
Title : CSCI 8450 Assignment: Chapter 1
Written by : Mohan Sai Ambati
Date : 24 Jan 2018
Description:
This file contains solutions of exercises 4,5,6,7,17,22 from section 8 in http://www.nltk.org/book/ch01.html
'''
from nltk.book import *
from nltk.corpus import brown
import re

def exercise4():
    print('Tokens/words in text 2: ', len(text2))
    print('Distinct tokens/words in text 2: ', len(set(text2)))
    words = []
    for word in text2:
        m = re.search('([A-Z a-z])+', word)
        if m:
            words.append(m[0])
    print('Actual english Words in text 2 : ', len(words))
    print('Distinct english words in text 2 : ', len(set(words)))
    return

def lexical_diversity(text):
    return len(set(text))/len(text)

def exercise5():
    words = ['humor', 'romance', 'fiction']
    lexical_vals = []
    titles = ['Genre', 'Lexical Diversity']

    for word in words:
        lexical_vals.append(lexical_diversity(brown.words(categories=word)))

    print('{:<8}|{:<8}'.format(*titles))
    for item in zip(words, lexical_vals):
        print('{0}|{1}'.format('-' * 8, '-' * 20))
        print ('{:<8}|{:<8}'.format(*item))
    print('The genre with maximum lexical diversity : ', words[lexical_vals.index(max(lexical_vals))])
    return

def exercise6():
    words = ['Elinor', 'Marianne', 'Edward', 'Willoughby']
    text2.dispersion_plot(words)
    return

def exercise7():
    collocations = text5.collocations()
    if collocations:
        print(collocations)
    return

def exercise17():
    # trail and error method for identifying sentence.
    move_front = move_back = True
    i = j = text9.index('sunset')
    while move_back or move_front:
        if text9[i] == '.':
            move_back = False
        if move_back: i -= 1
        if text9[j] == '.':
            move_front = False
        if move_front: j += 1
    i += 1
    j += 1
    print('The slice is : ', str(i) + ':' + str(j))
    print('Sliced sentence : ')
    print(" ".join(text9[i:j]))

    print("After further refinement.")
    # filter sentence
    sentence = text9[i:j]
    for k in range(1, len(sentence)):
        if sentence[k - 1].isupper() and sentence[k].isupper():
            i += 1
    print('The slice is : ', str(i) + ':' + str(j))
    print('Sliced sentence : ')
    print(" ".join(text9[i:j]))
    return

def exercise18():
    sent1_8 = []
    for i in range(1, 9):
        sent1_8 += globals()['sent' + str(i)]
    print('Vocabulary size : ', len(set(sent1_8)), 'Vocabulary : ', sorted(set(sent1_8)))
    return

def exercise22():
    four_letter_words = [word for word in text5 if len(word) == 4]
    frequency_distribution = FreqDist(four_letter_words)
    print('Words with decreasing order of frequency : ',
          frequency_distribution.most_common(len(set(four_letter_words))))
    titles = ['Word', 'Frequency', 'Count of word in text']
    print("Five most frequent words of length four : ")
    print('{:<8}|{:<8}|{:<8}'.format(*titles))
    for word in frequency_distribution.most_common(5):
        print('{0}|{1}|{2}'.format('-' * 8, '-' * 9, '-' * 20))
        print('{:<8}|{:<9}|{:<8}'.format(word[0], word[1], text5.count(word[0])))
    return

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")

def main():
    exercise(4)
    exercise(5)
    exercise(6)
    exercise(7)
    exercise(17)
    exercise(18)
    exercise(22)

if __name__ == "__main__":
    main()

