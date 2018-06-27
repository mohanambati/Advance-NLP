'''
CSCI 8450
Assignment on Chapter 6 in “Natural Language Processing with Python
Author: Sai Tarun, Battula
Colloborator: Mohan Sai, Ambati

'''
from __future__ import division
import nltk, re,pprint
import random



from nltk.corpus import names, movie_reviews
from nltk.corpus import wordnet as wn
from nltk.corpus import ppattach


all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]



def gender_features(name):
    features = {}
    #Feature 1: The first letter of a word
    features["first_letter"] = name[0].lower()
    # Feature 2: The last letter of a word
    features["last_letter"] = name[-1].lower()

    #Feature 3: The possible count of individual letters
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    #Feature 4: Checking for likliness of Male or Female based on Vowel:Consonant Ratio
    consonant_count = 0
    vowel_count =0
    for letter in list(name):
        if letter.lower() in ['a', 'e', 'i', 'o', 'u']:
            vowel_count = vowel_count + 1
        else:
            consonant_count = consonant_count + 1
    if ((vowel_count/consonant_count) < 0.5):
        features["likely_male"] = False
    else:
        features["likely_female"] = True
    #Feature 5:Marking last two letters of name as suffix
    features["last_two_letters"] = name[-2:].lower()
    # Feature 6:Marking first two letters of name as Prefix
    features["prefix"] = name[:2].lower()
    return features

def exercise2():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(labeled_names)
    featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
    train_set = featuresets[1000:]
    devtest_set = featuresets[500:1000]
    test_set = featuresets[:500]
    naive_classifier = nltk.NaiveBayesClassifier.train(test_set)
    print("Naive Bayes Classifier:", nltk.classify.accuracy(naive_classifier, devtest_set))
    dtree_classifier = nltk.DecisionTreeClassifier.train(test_set)
    print("Decision Tree Classifier:", nltk.classify.accuracy(dtree_classifier, devtest_set))
    Maxent_classifier = nltk.MaxentClassifier.train(test_set)
    print("Maxent_classifier:",nltk.classify.accuracy(Maxent_classifier, devtest_set))
    print("Naive Bayes Classifier on training set:", nltk.classify.accuracy(naive_classifier, train_set))
    print("Decision Tree Classifier on training set:", nltk.classify.accuracy(dtree_classifier, train_set))
    print("Maxent_classifier on training set:", nltk.classify.accuracy(Maxent_classifier, train_set))


def document_features(document):
    global word_features
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


def exercise4():

    documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    featuresets = [(document_features(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(30))


def dac_features(post, i, history):
    features = {}
    features["suffix(1)"] = post.text[-1:].lower()
    features["suffix(2)"] = post.text[-2:].lower()
    features["suffix(3)"] = post.text[-3:].lower()
    features["prefix(1)"] = post.text[0:1].lower()
    features["prefix(2)"] = post.text[0:2].lower()
    features["prefix(3)"] = post.text[0:3].lower()
    if i == 0 or len(history) == 0:
        features["prev-post"] = "START"
        features["prev-class"] = "START"
    else:
        features["prev-post"] = history[i - 1].text.lower()
        features["prev-class"] = history.get('class')[i - 1]
    return features


class ConsecutiveDialogTagger():
    def __init__(self, posts):
        train_set = []
        self.refined_set = []
        i = 0
        for post in posts:
            history = []
            featureset = dac_features(post, i, history)
            i = i + 1
            train_set.append((featureset, post.get('class')))
            self.refined_set.append((featureset, post.get('class')))
            history.append(post)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def getClassifier(self):
        return self.classifier

    def getRefined(self):
        return self.refined_set


def exercise7():
    train_set = nltk.corpus.nps_chat.xml_posts()[0:7000]
    test_set = nltk.corpus.nps_chat.xml_posts()[7000:]
    dialog_tagger = ConsecutiveDialogTagger(train_set)
    restDialog_tagger = ConsecutiveDialogTagger(test_set)
    print(nltk.classify.accuracy(dialog_tagger.getClassifier(), restDialog_tagger.getRefined()))
    print(dialog_tagger.getClassifier().show_most_informative_features(5))



def augumented_document_features(document):
    global word_features
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
        if word in document_words:
            synsets = wn.synsets(word)
            if synsets:
                features['lemma_name'] = synsets[0].lemmas()[0].name()
            else:
                features['lemma_name'] = 'UNKNOWN'
            features['word_in_wnet'] = 'KNOWN'
        else:
            features['word_in_wnet'] = 'UNKNOWN'
    return features


def exercise0():
    documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    featuresets = [(augumented_document_features(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    #print(classifier.show_most_informative_features(30))


def ppattach_features(noun1, noun2, verb):
    features = {}
    features['noun1_suffix'] = noun1[-1:].lower()
    features['noun2_suffix'] = noun2[-1:].lower()
    features['noun1_prefix'] = noun1[0:3].lower()
    features['noun2_prefix'] = noun2[0:3].lower()
    features['verb'] = verb.lower()


    return features


def exercise9():
    print('Extra Credit')
    featuresets = [(ppattach_features(ppobject.noun1, ppobject.noun2, ppobject.verb), ppobject.prep) for ppobject in ppattach.attachments('training') if ppobject.attachment == 'N']
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.most_informative_features(5))


def dummy_print():
    [print(ppobject.noun1,ppobject.prep, ppobject.noun2, ppobject.verb) for ppobject in ppattach.attachments('training') if ppobject.attachment == 'N']


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(2)
    exercise(4)
    exercise(7)
    exercise(0)
    #dummy_print()
    exercise(9)


if __name__ == "__main__":
    main()

