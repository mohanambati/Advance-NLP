'''
CSCI 8450
Assignment on Chapter 5a in “Natural Language Processing with Python
Author: Sai Tarun, Battula
Colloborator: Mohan Sai, Ambati

'''
from __future__ import division
import nltk, operator
from nltk.book import FreqDist
import pprint
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def ngrams(words, n):
    for i in range(0, len(words), n):
        yield words[i:i+n]

def exercise1():
    print("Part a")
    answer = {}
    plural_nouns = [w.lower() for (w, t) in brown.tagged_words() if t.startswith('NNS')]#Find the Plural Nouns
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_singular_nouns = [lemmatizer.lemmatize(w) for w in set(plural_nouns)]
    singular_nouns = [w.lower() for (w, t) in brown.tagged_words() if t.startswith('NN') if w in lemmatized_singular_nouns]
    fdist_pnouns = (FreqDist(plural_nouns))
    fdist_lsnouns = (FreqDist(singular_nouns))
    for (singular_word, singular_count) in fdist_lsnouns.most_common(100):
        for (word, count) in fdist_pnouns.most_common(100):
            if (singular_word == lemmatizer.lemmatize(word) and count > singular_count):
                answer[word]=count
                #print("Singular form:%s,Plural Form:%s,Count_Singular:%s,Count_Plural:%s"%(singular_word, word, singular_count, count))
    print(sorted(answer.items(), key=operator.itemgetter(1), reverse=True)[0:5])
    print("Part b")
    tags = [t for (w, t) in brown.tagged_words()]
    fdist_tags = (FreqDist(tags))
    print(fdist_tags.most_common(5))
    print("Part c")
    for genre in ['humor', 'romance', 'government']:
        print("The genre is:", genre)
        preceeding_tags = []
        four_grams = list(ngrams(brown.tagged_words(categories=genre), 4))
        for my_list in four_grams:
            if len(my_list) == 4 and my_list[3][1].startswith('NN'):
                preceeding_tags.append(my_list[0][1]+" "+my_list[1][1]+" "+my_list[2][1])
        print("The most common tags which preceed NN are:")
        fdist_mctags = (FreqDist(preceeding_tags))
        print(fdist_mctags.most_common(5))


def exercise2():
    print("Part a")
    t0 = nltk.DefaultTagger('NN')
    t1 = nltk.UnigramTagger(brown.tagged_sents(categories='news'), backoff=t0)
    t2 = nltk.BigramTagger(brown.tagged_sents(categories='news'), backoff=t1)
    t3 = nltk.TrigramTagger(brown.tagged_sents(categories='news'), backoff=t2)
    lore_tagged_sents = brown.tagged_sents(categories='lore')  # All the tagged sentences from Brown Corpus with category lore
    print(t3.evaluate(lore_tagged_sents))
    print("Part b")
    print(t3.tag(brown.sents(categories='lore')[199]))



def exercise3():
    news_tagged_sents = brown.tagged_sents(categories='news')  # All the sentences from Brown Corpus with category news
    lore_tagged_sents = brown.tagged_sents(
        categories='lore')  # All the tagged sentences from Brown Corpus with category lore
    trigram_tagger = nltk.TrigramTagger(
        news_tagged_sents)
    print(trigram_tagger.evaluate(lore_tagged_sents))


def exercise4():
    words = [n for n in wn.all_lemma_names()]
    more_than_one = []
    for word in words:

        tags = []
        for synset in wn.synsets(word):
            dot_location = synset.name().find('.')
            if synset.name()[0:dot_location] == word:
                tags.append(synset.name()[dot_location+1:dot_location+2])
        if len((set(tags))) > 1:
            more_than_one.append(word)


    print("More than one tagged words:",len(more_than_one))
    print("Total:", len(words))
    print("Percentage is:", (len(more_than_one)/len(words))*100)





def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(2)
    exercise(3)
    #exercise(4)


if __name__ == "__main__":
    main()

