import nltk
from nltk.corpus import wordnet as wn

from frequency_vector import freqdict, normalize

try:
    wn.synsets("test")
except:
    print("Problem with WordNet, make sure it is downloaded. (run 'nltk.download()' )")
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
    for x in chapter.paragraphs:
        proccess_paragraph(x,chapter_register)
    normalize(chapter_register["word_freq_dict"])
    normalize(chapter_register["region_freq_dict"])
    normalize(chapter_register["topic_freq_dict"])
    normalize(chapter_register["usage_freq_dict"])
    chapter.chapter_register=chapter_register
    #words = chapter.get_words()
    #if len(words) > 500:
    #    pos_freq = {
    #        "NN" : 0,
    #        "NNP" : 0,
    #        "DT" : 0,
    #        "IN" : 0,
    #        "JJ" : 0,
    #        "NNS" : 0
    #    }
    #    for pos in nltk.pos_tag(words):
    #        if pos[1] in pos_freq:
    #            pos_freq[pos[1]] += 1
    #    pos_freq = [(float(pos_freq[pos])/len(words)) for pos in pos_freq.keys()]
    #    chapter.text_features = {"pos_freq" : pos_freq}

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
        except BaseException as e:
            print(e)
            print("problem finding word:"+x)        
    #sentencedata.wordbigrams=ngrams(2,sentencedata.words)
    #sentencedata.synsets=[]
    #sentencedata.characterbigrams=[]
    #for x in sentencedata.words:
    #    sentencedata.characterbigrams.append(ngrams(2,"^"+x+"$"))
    #    try:
    #        sentencedata.synsets.append(wn.synsets(x))
    #    except BaseException as e:
    #        print(e)
    #        print("problem finding word:"+x)
    #        sentencedata.synsets.append(None)

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
