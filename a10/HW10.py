'''
Title : CSCI 8450 Assignment: Chapter 4b
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 04 April 2018
'''
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup

from nltk.corpus import wordnet as wn

from timeit import Timer
import matplotlib.pyplot as plt
SimpleText = 'One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def sort_synset(input_list, base_synset):
    depth = {synset: wn.synset(synset).shortest_path_distance(wn.synset(base_synset)) for synset in input_list}
    return sorted(depth.items(), key=lambda x: x[1])

def exercise0():
    wn_synsets = ['minke_whale.n.01', 'orca.n.01', 'novel.n.01', 'tortoise.n.01']
    print(sort_synset(wn_synsets, 'right_whale.n.01'))

def recursive_catalan(n):
    result = 0
    if n <=1:
        return 1
    for i in range(n):
        result += recursive_catalan(i) * recursive_catalan(n-i-1)
    return result


lookup = {}

def dynamic_catalan(n):
    result = 0
    if n <= 1:
        if n not in lookup:
            lookup[n] = 1
        return 1
    for i in range(n):
        try:
            a = lookup[i]
        except KeyError:
            a = dynamic_catalan(i)
        try:
            b = lookup[n - i - 1]
        except KeyError:
            b =  dynamic_catalan(n - i - 1)

        result += a*b
    if n not in lookup:
        lookup[n] = result
    return result


def exercise26():
    # Example of timer usage:
    stop = 17
    plt.axis([0, stop, 0, 7])

    for i in range(stop):
        print("N value : ", i)
        recursion_time = Timer(lambda: recursive_catalan(i)).timeit(1)
        print("\tRecursion execution time : ", recursion_time)
        recursion = plt.scatter(i, recursion_time, color='r',  s=121*2, marker='^', alpha=.4)
        plt.pause(0.05)
        dynamic_time = Timer(lambda: dynamic_catalan(i)).timeit(1)
        dynamic = plt.scatter(i, dynamic_time, color='b', s=121/2, alpha=.4)
        plt.pause(0.05)
        print("\tDynamic execution time : ", dynamic_time)
        plt.legend((recursion, dynamic),
                   ('recursion time', 'dynamic time'),
                   scatterpoints=1,
                   loc='upper left',
                   ncol=3,
                   fontsize=8)
    plt.show()


def GetRawText(url = "https://www.cs.utexas.edu/~vl/notes/dijkstra.html"):
    # open url and decode the html page to a list
    html = urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html, "html.parser").get_text()
    return raw

text = GetRawText()
sentences = nltk.sent_tokenize(text)
words = [word.lower() for word in nltk.word_tokenize(text)]
fd = nltk.FreqDist(words)

def get_sentences_score(n):
    lookup = dict(fd)
    sentence_lookup = {}
    count = 0
    for sentence in sentences:
        words_in_sentence =  [word.lower() for word in nltk.word_tokenize(sentence)]
        sentence_lookup[sentence] = (sum([lookup[word] for word in words_in_sentence]), count)
        count += 1
    result = sorted(sentence_lookup.items(), key=lambda x: x[1][0])[::-1]
    highest_rank = result[0][1][0]
    result = [sent for sent in result if sent[1][0] == highest_rank]
    return sorted(result, key=lambda x: x[1][1])[:n]

def exercise32():
    print(get_sentences_score(5))



def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise" + str(exNum)]()
    print("")


def main():
    exercise(0)
    exercise(26)
    exercise(32)


if __name__ == "__main__":
    main()

