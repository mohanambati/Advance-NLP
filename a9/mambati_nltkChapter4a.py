'''
Title : CSCI 8450 Assignment: Chapter 4a
Written by : Mohan Sai Ambati in collabration with Sai Tarun Battula
Date : 28 March 2018
'''

import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup


SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def GetRawText(url = "https://www.cs.utexas.edu/~vl/notes/dijkstra.html"):
    # open url and decode the html page to a list
    html = urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html, "html.parser").get_text()
    return raw

def novel10(text):
    return sorted([word for word in set(text[int(0.9*len(text)):int(len(text))]) if word not in set(text[0:int(0.9*len(text))])])

def exercise14():
    # tokonize the words in raw text
    tokenizedwords = [word.lower() for word in nltk.word_tokenize(GetRawText())]
    #sort and preint last 10% words in tokenized words.
    print( "first 10 tokens in last 10% of text is : ", novel10(tokenizedwords)[:10])

def AutomatedReadabilityIndex(text):
    temp1 = [len(word) for word in nltk.word_tokenize(text)]
    temp2 = []
    tokenize = nltk.sent_tokenize(text)
    for sent in tokenize:
        temp2.append(len(nltk.word_tokenize(sent)))
    return ((4.71 * (sum(temp1) / len(temp1))) + (0.5 * (sum(temp2) / len(temp2))) - 21.43)

def shorten(text, n):
    tokens = [word.lower() for word in nltk.word_tokenize(text)]
    fd = nltk.FreqDist(tokens)
    ommit_words = fd.most_common(n)
    #print(""+str(n)+" most frequent words ommited are : ", ommit_words)
    ommit_words = [word for (word,count) in ommit_words]
    return ' '.join([word for word in tokens if word not in ommit_words])


def exercise17():
    testvalues_n = [20, 35, 50, 65]
    Snippet = 'to begin with I would like to thank the College of Natural Sciences for the most honouring Invitation to address its newest flock of Bachelors on this most festive day. I shall do my best.'
    print("AutomatedReadabilityIndex of TestText is:", AutomatedReadabilityIndex(GetRawText()))
    print("\nPart A \n")
    for nvalue in testvalues_n:
        shorten_text = shorten(GetRawText(), nvalue)
        print("n = {}".format(nvalue))
        print("\tAutomatedReadabilityIndex of shorten text is : %s"%(AutomatedReadabilityIndex(shorten_text)))
        print("\tFew lines of shorten text is : \n", shorten_text[:300])
    print("\nPart B \n")
    print("The input text is : \n",Snippet)
    shorten_text = shorten(Snippet, 20)
    print("\nn = 20")
    print("\tOutput on snippet by removing 20 most frequent words is:", shorten_text)
    print("\tAutomatedReadabilityIndex of shorten text is : %s" % (AutomatedReadabilityIndex(shorten_text)))
    input1 = [word.lower() for word in nltk.word_tokenize(Snippet)]
    output = [word.lower() for word in nltk.word_tokenize(shorten_text)]
    print("**** Report ****")
    print("Total words in input snippet is : ", len(input1))
    print("Total words in output is : ", len(output))
    print("Total words removed : ", len(input1) - len(output))
    print("words removed are : ", [word for word in set(input1) if word not in set(output)])

### Tire data structure
class Tire:
    def __init__(self):
        self.root = dict()

    def insert(self, word):
        current_dict = self.root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        return

    def printTire(self):
        print(self.root)

    def getTire(self):
        return self.root

### Global varible
global buffer
buffer = []

### this function computes uniques string in every word using recurssion.
def compute_unique(word, tire):
    if not word:
        return
    buffer.append(word[0])
    if len(tire[word[0]]) == 1:
        return
    else:
        compute_unique(word[1:], tire[word[0]])

def exercise30():
    #create Tire object
    tire = Tire()
    #tokenize given text
    tokens = [word.lower() for word in nltk.word_tokenize(SimpleText)]
    # insert all unique words in Tire
    for word in set(tokens):
        tire.insert(word)
    print("The constructed tire data structure is : ")
    tire.printTire()
    # output variable for shortern text
    shorten_text = []
    #computer uniqueness for each word
    for word in tokens:
        global buffer
        compute_unique(word, tire.getTire())
        shorten_text.append(''.join(buffer))
        buffer = []
    #print the output
    shorten_text = ' '.join(shorten_text)
    compression = len(shorten_text)/len(SimpleText)
    print("Input text : ", SimpleText)
    print("Compression : ", compression)
    print("Output text : ", shorten_text)



def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(14)
    exercise(17)
    exercise(30)


if __name__ == "__main__":
    main()

