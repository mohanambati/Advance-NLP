from __future__ import division
import csv, nltk, random

all_words = []
word_features= None
def clean_data(row):
    temp = []
    for word in row:
        if ',' in word:
            temp += word.split(',')
        else:
            temp.append(word)
    cleaned_data = [word for word in temp if word.isalpha()]
    for word in temp.copy():
        if word.isalpha():
            temp.remove(word)
    all_words.extend(temp)
    temp = [" ".join(cleaned_data)]+temp
    return temp

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def document_classifier(cleaned_data):
    documents = [(document[1:200],document[0]) for document in cleaned_data]
    print("suffeling documents .... ")
    random.shuffle(documents)
    print("adding features to documents ... ")
    global word_features
    word_features = list(dict(nltk.FreqDist(w for w in all_words)).keys())[:170]
    print("creating feature sets ....")
    featuresets = [(document_features(d), c) for (d, c) in documents]
    print("Dividing data into 3 parts ....")
    train_set, test_set, result_set = featuresets[:1000], featuresets[1000:2000], featuresets[2000:2010]
    print("training classifiers .....")
    nb_classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("Accuracy of naive bays : ",nltk.classify.accuracy(nb_classifier, test_set))

    print("\nClassifying documents that are not in training set ... ")
    for (d,c) in result_set:
        print("\t\tPrediction : ", nb_classifier.classify(d), "\tActual : ", c)

def main():
    with open('input.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        print("Cleaning data .... ")
        cleaned_date = [clean_data(row) for row in spamreader]
        document_classifier(cleaned_date)


if __name__ == "__main__" :
    main()