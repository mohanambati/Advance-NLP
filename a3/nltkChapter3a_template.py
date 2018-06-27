from __future__ import division
import nltk, re

from urllib.request import urlopen

from nltk import word_tokenize

SimpleText='One day, his a horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def exercise6():
    print("part b")
    tokens = word_tokenize(SimpleText)
    part6b = [w for w in tokens if re.search('[A-Z][a-z]*', w)]#First letter being Capital followed by lower case letters
    print(part6b)
    print("part c")
    part6c = [w for w in tokens if re.search('p[aeiou]{,2}t', w)]#Lower case 'p' followed by a vowel followed by a t which can be repeated atmost
    print(part6c)
    print("part f")
    part6f = [w for w in tokens if re.search('\w+|[^\w\s]+', w)]
    print(part6f)



def exercise7():
    print("part a")
    tokens = word_tokenize(SimpleText)
    part7a = [w for w in tokens if re.search('^(a|an|the)$', w)]
    print(part7a)



def exercise21():
    unknown('https://www.cs.utexas.edu/~vl/notes/dijkstra.html')
    

def exercise25():
    print("For Word:")
    print("The converted word is:", pig_latin(input("Enter word to be converted to pig_latin:")))
    print("For text:")
    tokens = word_tokenize(SimpleText)
    for w in tokens:
        print(pig_latin(w), sep='', end=' ', flush=True)



def unknown(url):
    response = urlopen(url)
    raw = response.read().decode('utf8')
    tag_pattern = re.compile('<.*?>')
    cleaned = re.sub(tag_pattern, '', raw)#Cleaned HTML
    known = nltk.corpus.words.words('en')
    tokens_findall = [w for w in re.findall(r'[a-z]+', cleaned)]
    tokens_wordTokenize = set(word_tokenize(cleaned))
    wnl = nltk.WordNetLemmatizer()
    lem_findall_tokens = [wnl.lemmatize(t) for t in tokens_findall]
    lem_tokens_wordtokenize = [wnl.lemmatize(t) for t in tokens_wordTokenize]
    unknown_words_findall = [w for w in set(tokens_findall) if w not in set(known)]
    unknown_words_wordTokenize = [w for w in tokens_wordTokenize if w not in set(known)]
    unknown_words_lem_findall = [w for w in set(lem_findall_tokens) if w not in set(known)]
    unknown_words_lem_wordTokenize = [w for w in set(lem_tokens_wordtokenize) if w not in set(known)]
    print("Total number of Unknown words using re.findall() method:", len(unknown_words_findall))
    print("Total number of Unknown words using nltk.word_tokenize() method:", len(unknown_words_wordTokenize))
    print("Total number of Unknown words using re.findall() method after lemmatizing tokens:", len(unknown_words_lem_findall))
    print("Total number of Unknown words using nltk.word_tokenize() method after lemmatizing tokens:", len(unknown_words_lem_wordTokenize))


def pig_latin(word):
    regexp = r'[AEIOUaeiou]'
    suffix = 'ay'
    vowels = re.findall(regexp, word)
    final_word = 'final_word'
    if len(vowels) != 0:
        vowel = vowels[0]
        vowel_index = word.index(vowel)
        if vowel_index != 0:
            if (word[vowel_index] is 'u' and word[vowel_index-1] is 'q') or (word[vowel_index] is 'u' and word[vowel_index-1] is 'Q'):
                print("Yeah")
                w = word[0:vowel_index+1]
                rest = word[vowel_index+1:len(word)]
                final_word = rest + w + suffix
            else:
                w = word[0:vowel_index]
                rest = word[vowel_index:len(word)]
                final_word = rest + w + suffix
        else:
            final_word = word + suffix
    else:
        return word
    return final_word



def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(6)
    exercise(7)
    exercise(21)
    exercise(25)

if __name__ == "__main__":
    main()

