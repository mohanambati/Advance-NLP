'''
Title : CSCI 8450 Assignment: Chapter 6
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 7 March 2018
'''
from __future__ import division
import nltk, re, pprint

from nltk.corpus import names
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet
from nltk.corpus import ppattach

def gender_features(word, step):
    feature_set = {'last_letter': word[-1]}
    if step >= 1:
        feature_set.update({'last4_letters': word.lower()[-4:]})
    if step >= 2:
        vcount = 0
        for letter in word.lower():
            vcount += word.lower().count(letter)
        feature_set['vowels'] = vcount
    if step >= 3:
        feature_set['first2_letters'] = word[:2]
    if step >= 4:
        feature_set['first_letter'] = word[0]

    return feature_set

def exercise2():
    for step in range(5):
        print("Step : ", step+1)
        featuresets_male = [(gender_features(n, step), gender) for (n, gender) in
                            [(name, 'male') for name in names.words('male.txt')]]
        featuresets_female = [(gender_features(n, step), gender) for (n, gender) in
                              [(name, 'female') for name in names.words('female.txt')]]
        train_set = featuresets_male[0:250] + featuresets_female[0:250]
        dev_set = featuresets_male[250:500] + featuresets_female[250:500]
        test_set = featuresets_male[500:] + featuresets_female[500:]

        nb_classifier = nltk.NaiveBayesClassifier.train(train_set)
        dt_classifier = nltk.DecisionTreeClassifier.train(train_set)
        mk_classifier = nltk.MaxentClassifier.train(train_set)
        print("Naive Bays Classifier : ")
        print("\t Accuracy of dev_set is : ", nltk.classify.accuracy(nb_classifier, dev_set))
        print("Decision Tree Classifier : ")
        print("\t Accuracy of dev_set is : ", nltk.classify.accuracy(dt_classifier, dev_set))
        print("Maxent Classifier : ")
        print("\t Accuracy of dev_set is : ", nltk.classify.accuracy(mk_classifier, dev_set))

    print("Final accuracy of classifiers : ")
    print("Naive Bays Classifier : ", nltk.classify.accuracy(nb_classifier, test_set))
    print("Decision Tree Classifier : ", nltk.classify.accuracy(dt_classifier, test_set))
    print("Maxent Classifier : ", nltk.classify.accuracy(mk_classifier, test_set))

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
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
    print("Accuracy : ", nltk.classify.accuracy(classifier, test_set))
    most_informative_featur = classifier.show_most_informative_features(30)
    if most_informative_featur:
        print(most_informative_featur)


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
    print("Accuracy : ",nltk.classify.accuracy(dialog_tagger.getClassifier(), restDialog_tagger.getRefined()))
    print(dialog_tagger.getClassifier().show_most_informative_features(5))

def document_features_ex0(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        if word in document_words:
            synsets = wordnet.synsets(word)
            if synsets:
                features['lemma({})'.format(word)] = synsets[0].lemmas()[0].name()
                features['contains({})'.format(word)] = "KNOWN"
            else:
                features['lemma({})'.format(word)] = features['contains({})'.format(word)] = "UNK"
        else:
            features['lemma({})'.format(word)] = features['contains({})'.format(word)] = "UNK"
    return features

def exercise0():
    documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    featuresets = [(document_features_ex0(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("Accuracy : ",nltk.classify.accuracy(classifier, test_set))
    print("Most Informative Features : ")
    print(classifier.most_informative_features(5))


nattach = [inst for inst in ppattach.attachments('training') if inst.attachment == 'N']


def features(noun1, noun2, verb):
    feature_set = {}
    feature_set['noun1_suffix'] = noun1[-1:].lower()
    feature_set['noun2_suffix'] = noun2[-1:].lower()
    feature_set['noun1_prefix'] = noun1[0:3].lower()
    feature_set['noun2_prefix'] = noun2[0:3].lower()
    feature_set['verb'] = verb.lower()
    if feature_set['noun1_suffix'] == feature_set['noun2_suffix']:
        feature_set['special1'] = True
    else:
        feature_set['special1'] = False

    return feature_set


def exercise9():
    print('Extra Credit')
    featuresets = [(features(attach.noun1, attach.noun2, attach.verb), attach.prep) for attach in nattach]
    train_set, test_set = featuresets[100:], featuresets[:100]
    clasifier = nltk.NaiveBayesClassifier.train(train_set)
    print("Accuracy : ", nltk.classify.accuracy(clasifier, test_set))
    print("Most Informative Features : ")
    print(clasifier.most_informative_features(5))


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(2)
    exercise(4)
    exercise(7)
    exercise(0)
    exercise(9)


if __name__ == "__main__":
    main()

