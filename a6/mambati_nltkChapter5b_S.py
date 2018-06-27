'''
Title : CSCI 8450 Assignment: Chapter 5b
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 28 Feb 2018
'''

from __future__ import division
import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def ngarms(text, n):
    return list(nltk.ngrams(text, n))

def exercise1():
    print("Part a")
    print('Identifing plural words ....')
    words = set(brown.words())
    wordlemmatizer = nltk.WordNetLemmatizer()
    plural = nltk.FreqDist([w.lower() for (w, t) in brown.tagged_words() if t.startswith('NNS')])
    print('Identifing singular words ....')
    singular = nltk.FreqDist([w.lower() for (w, t) in brown.tagged_words() if t.startswith('NN') and not t.startswith('NNS')])
    print('lemmatizing plural words and finding the featured words....')
    temp = [word for word in plural if (wordlemmatizer.lemmatize(word) in singular and plural[word] > singular[wordlemmatizer.lemmatize(word)]) or (wordlemmatizer.lemmatize(word) not in singular and wordlemmatizer.lemmatize(word) in words)]
    print('Finding the frequencey of the featured words....')
    a = nltk.FreqDist([word.lower() for (word, tag) in brown.tagged_words() if word in temp])
    print("Five Nouns more common in their plural form are : ")
    print(a.most_common(5))

    print("Part b")
    tags = nltk.FreqDist([tag for (word, tag) in brown.tagged_words()])
    least_used_tags = tags.most_common(5)
    print("five most frequent tags in order of decreasing frequency : ")
    print(least_used_tags)

    print("Part c")
    genre = ['humor', 'romance', 'government']
    print("Most common 3 tags that precedes 'NN' is : ")
    for gen in genre:
        print(gen)
        print(nltk.FreqDist([seq for seq in [tup for tup in ngarms([tag for (word, tag) in brown.tagged_words(categories=gen)],4)] if seq[3].startswith('NN')]).most_common(1))



def exercise2():
    print("Part a")
    t0 = nltk.DefaultTagger('NN')
    t1 = nltk.UnigramTagger(brown.tagged_sents(categories='news'), backoff=t0)
    t2 = nltk.BigramTagger(brown.tagged_sents(categories='news'), backoff=t1)
    t3 = nltk.TrigramTagger(brown.tagged_sents(categories='news'), backoff=t2)
    lore_tagged_sents = brown.tagged_sents(categories='lore')  # All the tagged sentences from Brown Corpus with category lore
    print("Evaluate on all of the sentences from the Brown corpus with the category lore : ",t3.evaluate(lore_tagged_sents))
    print("Evaluate on all of the sentences from the Brown corpus with the category news : ",
          t3.evaluate(brown.tagged_sents(categories='news')))

    print("Part b")
    print("Output of tagger on the 200th sentence of the lore category of the Brown Corpus : ",t3.tag(brown.sents(categories='lore')[199]))


def exercise3():
    news_tagged_sents = brown.tagged_sents(categories='news')  # All the sentences from Brown Corpus with category news
    lore_tagged_sents = brown.tagged_sents(categories='lore')  # All the tagged sentences from Brown Corpus with category lore
    trigram_tagger = nltk.TrigramTagger(news_tagged_sents)
    print("Evaluate on all of the sentences from the Brown corpus with the category lore (without backoff) : ",trigram_tagger.evaluate(lore_tagged_sents))


def exercise4():
    wordclasses = ['n', 'v', 'a', 'r']
    temp = {}
    result = {}
    for word_class in wordclasses:
        temp[word_class] = set(wordnet.all_lemma_names(word_class, lang="eng"))
    for i in range(len(wordclasses)):
        for word in temp[wordclasses[i]] :
            for j in range(len(wordclasses)):
                if word in temp[wordclasses[j]]:
                    if word not in result:
                        result[word] = set(wordclasses[j])
                    else:
                        result[word].update(wordclasses[j])

    count = 0
    for word in result:
        if len(result[word]) > 1:
            count += 1
    print("More than one tagged words:", count)
    print("Total:", len(result))
    print("Percentage is:",(count/len(result))*100)





def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(2)
    exercise(3)
    exercise(4)


if __name__ == "__main__":
    main()

