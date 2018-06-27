'''
Title : CSCI 8450 Assignment: Chapter 3a
Written by : Mohan Sai Ambati
Date : 31 Jan 2018
Description:
This file contains solutions of exercises 6(b,c,f),7(a),21 and 25 from section 3.12 in http://www.nltk.org/book/ch03.html
'''
from __future__ import division
import nltk, re
from urllib import request
from nltk import word_tokenize
from bs4 import BeautifulSoup

SimpleText = 'One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def exercise6():
    regular_ex = {'part b': '[A-Z][a-z]*',
                  'part c': 'p[aeiou]{,2}t',
                  'part f': '\w+|[^\w\s]+'}
    for part in regular_ex:
        print(part+' :')
        result = nltk.re_show(regular_ex[part], SimpleText, '{', '}')
        if result:
            print(result)
        print()

def exercise7():
    reg_ex = {"part a" : "\\b[Aa][n]?\\b|\\b[Tt][h][e]\\b" }
    result =  nltk.re_show(reg_ex["part a"], SimpleText, '{', '}')
    if result:
        print(result)

def unknown(url):
    # open url and decode the html page to a list
    html = request.urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html, "html.parser").get_text()

    # Filter HTML data using regular expression. get only word which has atleast one lower case letter in it.
    regex_words = re.findall(r'[A-Za-z]+', raw)
    regex_words = set(word for word in regex_words if not word.isupper())

    # using word_tokenize to filter the data
    tokens = set(word_tokenize(raw))

    #diffrence of re.findall and word_tokenize
    print("Words in re.findall() and not in word_tokenize() : ", regex_words - tokens)
    print("\n Words in word_tokenize() and not in re.findall() : ", tokens - regex_words)

    # Lemmatize regex_words
    print("Lemmatizing words ..")
    wordlemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_words = set(wordlemmatizer.lemmatize(word) for word in regex_words)

    # Get words form nltk.corpus.words
    print("Collecting words from corpus ..")
    corpus_words = set(word for word in nltk.corpus.words.words())

    # fidn all the words not present in corpus.words.words
    return list(lemmatized_words - corpus_words), list(regex_words - corpus_words)

def exercise21():
    unknown_lemmetized_words, unknown_regex_words = unknown("https://www.cs.utexas.edu/~vl/notes/dijkstra.html")
    print('\n Unknown words (unknown_lemmetized_words, unknown_refindall()_words) : ', (len(unknown_lemmetized_words),len(unknown_regex_words)))
    print("\n Extra unknown words in re.findall() :", set(unknown_regex_words) - set(unknown_lemmetized_words))

def pig_latin(text):
    pig_latin_text = []
    consonant_clusters = ['scr', 'spl', 'spr', 'str', 'squ', 'shr', 'sch', 'thr', 'pl', 'pr', 'ph', 'bl', 'br', 'tr', 'dr', 'cl',
                          'cr', 'ch', 'ck', 'gl', 'gr', 'fl', 'fr', 'th', 'sh', 'sk', 'sc', 'sl', 'sm', 'sn', 'sp', 'st',
                          'sw', 'tw', 'dw', 'qu', 'gw']
    vowles = ['a', 'e', 'i', 'o', 'u']
    words = word_tokenize(text)
    for word in words:
        w = re.findall(r'[A-Za-z]+',word)
        flag = False
        if w:
            for letter in w[0]:
                if letter in vowles:
                    flag = True
                    break
            if w[0][:3].lower() in consonant_clusters:
                pig_latin_text.append(word.replace(w[0], w[0][3:] + w[0][:3] + 'ay'))
            elif w[0][:2].lower() in consonant_clusters:
                pig_latin_text.append(word.replace(w[0], w[0][2:] + w[0][:2] + 'ay'))
            elif w[0][0].lower() in vowles:
                pig_latin_text.append(word.replace(w[0], w[0] + 'ay'))
            elif flag:
                for letter in range(0, len(w[0])):
                    if w[0][letter] in vowles:
                        pig_latin_text.append(word.replace(w[0],w[0][letter:] + w[0][:letter] + 'ay'))
                        break
            else:
                pig_latin_text.append(word.replace(w[0], w[0] + 'ay'))
        else:
            pig_latin_text.append(word)
    assert len(words), len(pig_latin_text)
    return " ".join(pig_latin_text)

def exercise25():
    print("Piglatin conversion for Simple text: ", pig_latin(SimpleText))
    stop = False
    print("\n******************** Piglatin conversion for given text/word (enter X to exit)  ********************")
    while not stop:
        user_input = input("Please enter your input: ")
        if user_input.lower() == 'x':
            stop = True
        else:
            print('piglatin of given word/text : ',pig_latin(user_input))

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise" + str(exNum)]()
    print("")

def main():
    exercise(6)
    exercise(7)
    exercise(21)
    exercise(25)


if __name__ == "__main__":
    main()

