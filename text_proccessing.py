import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

from frequency_vector import freqdict, normalize

test=None
try:
    test=wn.synsets("test")
except:
    print("Problem with WordNet, make sure it is downloaded. (run 'nltk.download()' )")
    exit(1)
try:
    swn.senti_synsets("test")
except BaseException as e:
    print("Problem with SentiWordNet, make sure it is downloaded. (run 'nltk.download()' )")
    exit(1)

def proccess_book(bookdata):
    for x in bookdata.chapters:
        proccess_chapter(x)

def proccess_chapter(chapter):
    chapter_register={}
    chapter_register["validwords"]=0
    chapter_register["word_freq_dict"]=freqdict()
    chapter_register["region_freq_dict"]=freqdict()
    chapter_register["topic_freq_dict"]=freqdict()
    chapter_register["usage_freq_dict"]=freqdict()
    chapter_register["sense_dist_dict"]=freqdict()
    for x in chapter.paragraphs:
        proccess_paragraph(x,chapter_register)
    normalize(chapter_register["word_freq_dict"])
    normalize(chapter_register["region_freq_dict"])
    normalize(chapter_register["topic_freq_dict"])
    normalize(chapter_register["usage_freq_dict"])
    normalize(chapter_register["sense_dist_dict"],cachetotal="total")
    chapter.chapter_register=chapter_register

def proccess_paragraph(paragraphdata,chapter_register):
    for x in paragraphdata.sentences:
        proccess_sentence(x,chapter_register)


def proccess_sentence(sentencedata,chapter_register):
    for x in sentencedata.words:
        words=chapter_register["word_freq_dict"]
        words.plusplus(x,1)
        try:
            sets=wn.synsets(x)
            if len(sets)<=0:
                break
            chapter_register["validwords"]=chapter_register["validwords"]+1
            usage=chapter_register["usage_freq_dict"]
            usages = [inner for outer in sets for inner in outer.usage_domains()]
            for use in usages:
                usage.plusplus(use._name,float(1)/len(usages))
            topic=chapter_register["topic_freq_dict"]
            topics = [inner for outer in sets for inner in outer.topic_domains()]
            for top in topics:
                topic.plusplus(top._name,float(1)/len(topics))
            region=chapter_register["region_freq_dict"]
            regions = [inner for outer in sets for inner in outer.region_domains()]
            for reg in regions:
                region.plusplus(reg._name,float(1)/len(regions))
            sense=chapter_register["sense_dist_dict"]
            sentis = [swn.senti_synset(synset._name) for synset in sets]
            if None in sentis:
                continue
            for sen in sentis:
                sense.plusplus("pos",float(sen.pos_score())/len(sentis))
                sense.plusplus("neg",float(sen.neg_score())/len(sentis))
                sense.plusplus("obj",float(sen.obj_score())/len(sentis))
            sense.plusplus("total",1)
        except BaseException as e:
            print(e)
            print("problem finding word:"+x)

def ngrams(n,seq):
    grams=dictreducer()
    for i in range(len(seq)+1-n):
        grams.append(tuple(seq[i:i+n]))
    return grams

class dictreducer(dict):
    def __init__(self,red=lambda x,y:x+y):
        self.red=red
    def append(self,x):
        if x in self:
            self[x]=self[x]+1
        else:
            self[x]=1
    def __add__(self,other):
        res=dictreducer()
        for x in self.keys():
            res[x]=self[x]
        for x in other.keys():
            if x in res:
                res[x]=self.red(res[x],other[x])
            else:
                res[x]=other[x]
        return res
