'''
Title : CSCI 8450 Assignment: Chapter 5a
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 21 Feb 2018
'''

from __future__ import division
import nltk
from nltk.corpus import brown

SimpleText = 'One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def exercise1():
    train_data = brown.tagged_sents(categories='news')
    test_data = brown.tagged_sents(categories='lore')
    unigram_tagger_model = nltk.UnigramTagger(train_data)
    print("Evaluate on all of the sentences from the Brown corpus with the category lore : ",unigram_tagger_model.evaluate(test_data))
    print("Evaluate on all of the sentences from the Brown corpus with the category news : ", unigram_tagger_model.evaluate(train_data))
    print("Output of tagger on the 200th sentence of the lore category of the Brown Corpus : ", unigram_tagger_model.tag(brown.sents(categories='lore')[199]))


brown_words = {}
brown_dict = {}
def findtags():
    for genre in brown.categories():
        word_tags = []
        for (word, tag) in nltk.corpus.brown.tagged_words(categories=genre):
            word = word.lower()
            word_tags.append((tag, word))
            if genre not in brown_words:
                brown_words[genre] = [word]
            else:
                brown_words[genre].append(word)
        cfd = nltk.ConditionalFreqDist(word_tags)
        brown_dict[genre] = dict((tag, (cfd[tag],cfd[tag].most_common(len(set(cfd[tag])))))for tag in cfd.conditions())

    return brown_dict


def trigrams(genre):
    return list(nltk.ngrams(brown_words[genre], n=3))

def exercise2():
    tagdict = findtags()
    sep_genres = ['humor', 'romance', 'government']
    print("Part 1")
    words_JJ = set()
    for genre in tagdict:
        temp = set(tagdict[genre]['JJ'][0])
        words_JJ.update(temp)
        if genre in sep_genres:
            print(genre)
            temp = sorted(temp)
            print("\tAlphabetically sorted list of words tagged with \"JJ\" : ", temp)
            print("\tDistinct words tagged with \"JJ\" : ", len(temp))
            print("\tFirst five words tagged with \"JJ\" : ", list(temp)[:5])

    words_JJ = sorted(words_JJ)
    print()
    print("(In total Brown Corpus) Alphabetically sorted list of words tagged with \"JJ\" : ", words_JJ)
    print("(In total Brown Corpus) Distinct words tagged with \"JJ\" : ", len(words_JJ))
    print("(In total Brown Corpus) First five words tagged with \"JJ\" : ", list(words_JJ)[:5])


    print("Part 2")

    words = set()
    for genre in tagdict:
        temp = set()
        for tag in tagdict[genre]:
            if tag.startswith('NNS') or tag.startswith('VBZ'):
                temp |= set(tagdict[genre][tag][0])

        temp = sorted(temp)
        words.update(temp)
        if genre in sep_genres:
            print(genre)
            print("\tAlphabetically sorted list of words tagged with \"Plural nouns or singular verbs\" : ", temp)
            print("\tDistinct words tagged with \"Plural nouns or singular verbs\" : ", len(temp))
            print("\tFirst ten words tagged with \"Plural nouns or singular verbs\" : ", sorted(list(temp))[:10])

    words = sorted(words)
    print()
    print("(In total Brown Corpus) Alphabetically sorted list of words tagged with \"Plural nouns or singular verbs\" : ", words)
    print("(In total Brown Corpus) Distinct words tagged with \"Plural nouns or singular verbs\" : ", len(words))
    print("(In total Brown Corpus) First ten words tagged with \"Plural nouns or singular verbs\" : ", sorted(list(words))[:10])

    print("Part 3")

    word_phrases = []
    for genre in tagdict:
        temp = [" ".join([w1.lower(), w2.lower(), w3.lower()]) for tagged_sent in brown.tagged_sents(categories=genre)
            for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(tagged_sent)
                if t1.startswith('IN') and t2.startswith('AT') and t3.startswith('NN')]
        word_phrases.extend(temp)

        if genre in sep_genres:
            print(genre)
            print("\tMost common 3 phrases in this genre is : ", sorted(list(nltk.FreqDist(temp).most_common(3))))
    print("(In total Brown Corpus)  Most common word phrases in entire brown corpus is : ",
          nltk.FreqDist(word_phrases).most_common(3))


    print("Part 4")
    a = ['himself', 'his', 'him', 'he', "he's", "he'd", "he'll"]
    b = ['herself', 'her', 'hers', 'she', "she's", "she'd", "she'll"]

    m = f = 0
    for genre in tagdict:
        tm = tf = 0
        for tag in tagdict[genre]:
            if tag.startswith('PP'):
                for lis in tagdict[genre][tag][1]:
                    if lis[0] in a:
                        tm += lis[1]
                    elif lis[0] in b:
                        tf += lis[1]
        if genre in sep_genres:
            print(genre)
            print("\tmasculine ratio in this genre is : ", tm / tf)
        m += tm
        f += tf

    print("(In total Brown Corpus) ratio of masculine pronous over brown corpus is : ", m / f)


def exercise3():
    cfd = nltk.ConditionalFreqDist(
        (word.lower(), tag)
        for genre in brown.categories()
        for (word, tag) in brown.tagged_words(categories=genre)
    )
    result = {'part1':{},
              'part2' : {}
              }
    print("Part 1")
    for word in sorted(cfd.conditions()):
        tags = set(cfd[word])
        if len(tags) == 5:
            if word not in result['part1']:
                result['part1'][word] = tags

    print("Number of words which has exactly 5 possible tags : ", len(result['part1']))
    print("words which has exactly 5 possible tags : ", result['part1'])

    print("Part 2")

    possible_tags = ['CS', 'WPS', 'DT', 'QL', 'NIL']
    distinct_word = 'that'

    print(" the distinct word is : ", distinct_word)
    for sentence in brown.tagged_sents():
        for tuple in sentence:
            if tuple[0] == distinct_word and len(possible_tags) > 0:
                if tuple[1] == possible_tags[0]:
                    print("Sentence : ", " ".join([w for (w, t) in sentence]))
                    if len(possible_tags) > 0:
                        possible_tags.remove(possible_tags[0])



def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise" + str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(2)
    exercise(3)


if __name__ == "__main__":
    main()

