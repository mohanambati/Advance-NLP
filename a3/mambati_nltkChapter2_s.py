'''
Title : CSCI 8450 Assignment: Chapter 2
Written by : Mohan Sai Ambati
Date : 7 Feb 2018
Description:
This file contains solutions of exercises 2,5,9,11,13,18 and 27 in http://www.nltk.org/book/ch02.html
'''

import nltk, re
from nltk.corpus import stopwords
from nltk.book import *

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet

relationships = {}

def exercise2():
    persuasion = gutenberg.words("austen-persuasion.txt")
    print("word tokens : ", len(persuasion))
    print("word types : ", len(set(persuasion)))


def add_relation(pair, relation):
    if relation in relationships:
        if pair not in relationships[relation]:
            relationships[relation].append(pair)
    else:
        relationships[relation] = [pair]


def relationship_finder(pairs):
    for pair in pairs:
        word1 = None
        synonyms = wordnet.synsets(pair[0])
        for synonym in synonyms:
            if pair[1] in "".join([member.name() for member in synonym.member_meronyms()]):
                add_relation(pair, 'member_meronyms')
            elif pair[1] in "".join([member.name() for member in synonym.part_meronyms()]):
                add_relation(pair, 'part_meronyms')
            elif pair[1] in "".join([member.name() for member in synonym.substance_meronyms()]):
                add_relation(pair, 'substance_meronyms')
            elif pair[1] in "".join([member.name() for member in synonym.member_holonyms()]):
                add_relation(pair, 'member_holonyms')
            elif pair[1] in "".join([member.name() for member in synonym.part_holonyms()]):
                add_relation(pair, 'part_holonyms')
            elif pair[1] in "".join([member.name() for member in synonym.substance_holonyms()]):
                add_relation(pair, 'substance_holonyms')

    return relationships

def exercise5():
    noun_pairs = [('house', 'library'), ('university', 'college'), ('school', 'staff'),
                  ('tree', 'wood'), ('tree', 'forest'), ('foot', 'leg'), ('feather', 'bird'), ('ice', 'glacier'),
                  ('melanin', 'skin'), ('river', 'water')]
    print("The noun pairs selected are : ")
    print(noun_pairs)
    print("Finding relations for given noun pairs...")
    output = relationship_finder(noun_pairs)
    for relation in output:
        print('{:>20} : {}'.format(relation, output[relation]))

    print("total relations identified : ", len([z for x in output for z in output[x]]))


# construct a dictory to check the context of every word.
text = list(nltk.corpus.genesis.words('english-kjv.txt'))+list(nltk.corpus.genesis.words('english-web.txt'))
my_english_dictonary = nltk.ConditionalFreqDist(nltk.bigrams(text))

#search the context of the word in contructed dictonary.
def search_dictonary(word):
    try:
        return list(my_english_dictonary[word])
    except ValueError:
        return None

def exercise9():
    text1_vocab = sorted(set(text1))
    text7_vocab = sorted(set(text7))

    print(" \nVocabulary of text1 : ", text1_vocab)
    print(" Vocabulary of text7 : ", text7_vocab)

    print("Vocabulary Size (text1, text7) : ", (len(text1_vocab), len(text7_vocab)))

    text1_richness = len(text1_vocab) / len(text1)
    text7_richness = len(text7_vocab) / len(text7)

    print(" \nText richness of text1 : ", text1_richness)
    print(" Text richness of text7 : ", text7_richness)

    stopwrds = stopwords.words('english')
    print("\nContent fraction of text 1 : ", len([w for w in text1_vocab if w.lower() not in stopwrds]) / len(text1))
    print("Content fraction of text 7 : ", len([w for w in text7_vocab if w.lower() not in stopwrds]) / len(text7))

    print("\n Collocations used in text1 : ")
    text1_collocations = text1.collocations()
    if text1_collocations:
        print(text1_collocations)

    print("\n Collocations used in text7 : ")
    text7_collocations = text7.collocations()
    if text7_collocations:
        print(text7.collocations())

    fd_text1 = FreqDist([word for word in text1 if (word.lower()).islower()]).most_common(5)
    fd_text7 = FreqDist([word for word in text7 if (word.lower()).islower()]).most_common(5)

    print("\nTop 5 common words used in text1 : ", fd_text1)
    print("Top 5 common words used in text7 : ", fd_text7)

    # take all the owrds with atleast length 9
    text1_words = set(word for word in set(text1) if len(word) >= 9)
    text7_words = set(word for word in set(text7) if len(word) >= 9)

    # take common words in two texts.
    commonwords = text1_words & text7_words

    # construct bigrams for both the texts to identify the context.
    text1_bigrams = set(bigram for bigram in set(nltk.bigrams(text1)) if
                        bigram[0] in commonwords and len(bigram[1]) >= 3 and re.search('([A-Z a-z])+', bigram[1]))
    text7_bigrams = set(bigram for bigram in set(nltk.bigrams(text7)) if
                        bigram[0] in commonwords and len(bigram[1]) >= 3 and re.search('([A-Z a-z])+', bigram[1]))

    context_dic = {}
    final_words = {}

    # find same words used in diffrent context in two texts.
    for word in commonwords:
        word_ussage_text1 = set(bigram[1] for bigram in text1_bigrams if bigram[0] == word)
        word_ussage_text7 = set(bigram[1] for bigram in text7_bigrams if bigram[0] == word)

        if word_ussage_text1 and word_ussage_text7 and not (word_ussage_text1 & word_ussage_text7):
            if word not in context_dic:
                context_dic[word] = (word_ussage_text1, word_ussage_text7)

    # filter words that are used in diffrent context from the constucted dictonary.
    for word in context_dic:
        if not (set(search_dictonary(word)) & (context_dic[word][0] | context_dic[word][0])):
            if word not in final_words:
                final_words[word] = context_dic[word]

    print("\nFilterd words after processing founnd "+str(len(final_words))+" words are used with diffrent bigrams than dictonary  : ", final_words)

    # words find after manually analyzing final_words.
    diffrent_context_words = ['condemned', 'Intermediate', 'sketching', 'promotion']
    print(" After further analysis, the words that are used in diffrent contexts are : ", diffrent_context_words)

    for word in diffrent_context_words:
        text1.concordance(word)
        text7.concordance(word)


def exercise11():
    modal_list = {'pronouns': ['i', 'me', 'mine', 'you', 'yours', 'his', 'her', 'hers', 'we', 'they', 'them'],
                  'adverbs': ['up', 'so', 'out', 'just', 'now', 'how', 'then', 'more', 'also', 'here'],
                  'most_common_words': ['be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not',
                                        'on'],
                  }

    genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
    cfd = nltk.ConditionalFreqDist(
        (genre, word.lower())
        for genre in genres
        for word in brown.words(categories=genre)
    )

    for modal in modal_list:
        print("\nModal used : ", modal)
        cfd.tabulate(conditions=genres, samples=modal_list[modal])


def exercise13():
    print('caliculating all noun syncsets ......')
    noun_synonyms = wordnet.all_synsets('n')
    total = 0
    no_hyponyms = 0
    print('Counting noun sets with no hyponyms ...... ')
    for synonym in noun_synonyms:
        if not synonym.hyponyms():
            no_hyponyms += 1
        total += 1
    print("Total noun synsets : ", total)
    print("noun synsets with no hyponyms : ", no_hyponyms)
    print("Percentage of noun synsets with no hyponyms : ", (no_hyponyms / total) * 100)


def exercise18():
    stopwrds = stopwords.words('english')
    print(("Computing bigrams ...."))
    bigrams = list(nltk.bigrams([word for genre in brown.categories() for word in brown.words(categories=genre)]))
    bigrams = [bigram for bigram in bigrams if bigram[0] not in stopwrds and bigram[1] not in stopwrds and (bigram[0].lower()).islower() and (bigram[1].lower()).islower()]
    print("Computing frequency distributions ....")
    fd = nltk.FreqDist(bigrams)
    print("Most common 50 bigrams : ", fd.most_common(50))
    print("Most common 5 bigrams : ", fd.most_common(5))

def polysemy(word_class):
    print("Computing average polysemy of word class("+word_class+") .........")
    polysemy_count = 0
    all_lemma_names = set(wordnet.all_lemma_names(word_class, lang="eng"))
    for name in all_lemma_names:
        polysemy_count += len(wordnet.synsets(name,word_class))
    return polysemy_count/len(all_lemma_names)

def polysemy_meth2(word_class):
    print("Computing average polysemy of word class("+word_class+") .........")
    polysemy_count = 0
    all_lemma_names = set(wordnet.all_lemma_names(word_class))
    for name in all_lemma_names:
        polysemy_count += len(wordnet.synsets(name,word_class))
    return polysemy_count/len(all_lemma_names)

def exercise27():
    word_class = {"nouns": 'n',
                  "verbs": 'v',
                  "adjectives": 'a',
                  "adverbs": 'r'}
    for e in word_class:
        """There are 2 ways of implementing this, both ways are defined above.
        I am using polysemy() instead of polysemy_meth2() because it has less execution time.
        """
        average_polysemy = polysemy(word_class[e])
        print("The average polysemy of " + e + " : ", average_polysemy)



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

