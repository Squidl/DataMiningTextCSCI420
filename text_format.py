import load_texts

class book:
    def __init__(self,author,data):
        self.author=author
        self.chapters=[chapter(x) for x in data.split("\n\n\n")]

class chapter:
    def __init__(self,data):
        self.paragraphs=[paragraph(x) for x in data.split("\n\n")]

class paragraph:
    def __init__(self,data):
        self.sentences=[sentence(x) for x in data.split(".")]

class sentence:
    def __init__(self,data):
        self.words=[word(x) for x in data.split(" ")]

class word:
    def __init__(self,data):
        self.text=data
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
