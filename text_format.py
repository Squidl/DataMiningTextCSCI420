from nltk import data as nltk_data, word_tokenize
import string

import load_texts

sent_detector = nltk_data.load('tokenizers/punkt/english.pickle')

class book:
    def __init__(self,author,data):
        self.author=author
        self.chapters=[chapter(x) for x in data.split("\n\n\n")]

class chapter:
    def __init__(self,data):
        self.paragraphs=[paragraph(x) for x in data.split("\n\n")]
        
    def get_words(self):
        words = [paragraph.get_words() for paragraph in self.paragraphs]
        return [item for sublist in words for item in sublist]

class paragraph:
    def __init__(self,data):
        self.sentences=[sentence(x) for x in sent_detector.tokenize(data)]
        
    def get_words(self):
        words = [sentence.get_words() for sentence in self.sentences]
        return [item for sublist in words for item in sublist]

class sentence:
    def __init__(self,data):
        self.words=[word(x) for x in word_tokenize(data)]

    def get_words(self):
        words = [string.lower(word.text) for word in self.words]
        return filter(lambda x : not x in string.punctuation, words)

class word:
    def __init__(self,data):
        self.text=data.strip()
    def __str__(self):
        return self.text
    def __repr__(self):
        return self.__str__()
cached={}

def get(name,cache=True):
    if name in cached:
        return cached[name]
    else:
        raw=load_texts.get(name,cache=cache)
        dat=book(raw[1],raw[2])
        cached[name]=dat
        return dat

def getnames():
    return load_texts.getnames()
