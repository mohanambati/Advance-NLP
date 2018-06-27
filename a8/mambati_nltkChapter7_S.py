'''
Title : CSCI 8450 Assignment: Chapter 7
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 14 March 2018
'''
from __future__ import division
import nltk, re, pprint
from nltk.corpus import conll2000
from nltk import word_tokenize, pos_tag

# pseduo method that does sample IO and IOB tagging for explanation.
def get_tags(tree):
    io_tags = []
    iob_tags = []
    start = True
    for t in tree.leaves():
        if "NN" in t[1]:
            io_tags.append((t[0], t[1], "I-NP"))
            if start:
                iob_tags.append((t[0], t[1], "B-NP"))
                start = False
            else:
                iob_tags.append((t[0], t[1], "I-NP"))
        else:
            start = True
            iob_tags.append((t[0], t[1], "O"))
            io_tags.append((t[0], t[1], "O"))

    return iob_tags, io_tags

def exercise1():
    sentence = "John J. Smith travelled to Omaha."
    tree = pos_tag((word_tokenize(sentence)))
    cp = nltk.RegexpParser("NP: {<DT>?<JJ>*<NN.*>}")
    result = cp.parse(tree)
    iob_tags, io_tags = get_tags(result)
    print("IO tagging : ", io_tags)
    print("IOB tagging : ", iob_tags)
    print("""
    If you consider IO tagging, there are 3 continous chuncks ('John', 'NNP', 'I-NP'), ('J.', 'NNP', 'I-NP'), ('Smith', 'NNP', 'I-NP'), there is no information wheather to consider them seperately or as an single one, There is chance of loosing data.
    But If you consider IOB tagging, we have a begin tag for each chunk, so it will specify the start of every chunk and all the words with 'I-NP' is part of that chunk until we find next begin tag. So, there is no chance of loosing any data {('John', 'NNP', 'B-NP'), ('J.', 'NNP', 'I-NP'), ('Smith', 'NNP', 'I-NP')}.
    """)


def exercise2():
    sentenceSample = [("Many", "JJ"), ("little", "JJ"), ("dogs", "NNS"), ("barked", "VBD"), ("at", "IN"), ("cats", "NNS")]
    grammar = """NP: {(<DT>*<CD>*)?<JJ>*<NNS>}
                     {<DT>?<JJ>*<NN>} 
               """
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentenceSample)
    print("Parsed simple sentence : ",result)


def exercise3():
    print('Part a : ')
    grammar = """NP: {(<DT>*<CD>*)?<JJ>*<NNS>}
                     {<DT>?<JJ>*<NN>} 
               """
    cp = nltk.RegexpParser(grammar)
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])[:100]
    print(cp.evaluate(test_sents))

    print('Part b : ')
    cp = nltk.RegexpParser("")  # baseline parser
    print(cp.evaluate(test_sents))

    print('Part c : ')
    grammar = """NP : {<[RCDJNP].*>*<NNS>} 
                      {<[CDJNP].*>*<NNS>}
                      {(<DT>*<CD>*)?<JJ>*<NNS>}
                      {<DT>?<JJ>*<NN>}
                      """

    cp = nltk.RegexpParser(grammar)
    print(cp.evaluate(test_sents))

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(2)
    exercise(3)


if __name__ == "__main__":
    main()

