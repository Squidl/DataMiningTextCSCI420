from nltk.corpus import wordnet as wn

try:
    wn.synsets("test")
except:
    print("Problem with WordNet, make sure it is downloaded. (run 'nltk.download()' )")
    exit(1)

def proccess_book(bookdata):
    for x in bookdata.chapters:
        proccess_chapter(x)

def proccess_chapter(chapterdata):
    for x in chapterdata.paragraphs:
        proccess_paragraph(x)

def proccess_paragraph(paragraphdata):
    for x in paragraphdata.sentences:
        proccess_sentence(x)

printed=False
def proccess_sentence(sentencedata):
    sentencedata.wordbigrams=ngrams(2,sentencedata.words)
    for x in sentencedata.words:
        proccess_word(x)

def proccess_word(worddata):
    worddata.characterbigrams=ngrams(2,"^"+worddata.text+"$")
    try:
        
        worddata.synsets=wn.synsets(worddata.text)
    except:
        print("problem finding word:"+worddata.text)
        worddata.synsets=None


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
