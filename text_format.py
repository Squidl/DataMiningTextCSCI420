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

texts=[]
for x in load_texts.raw:
    texts.append(book(x[1],x[2]))

