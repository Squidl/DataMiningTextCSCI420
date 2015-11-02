
def proccess_book(bookdata):
    for x in bookdata.chapters:
        proccess_chapter(x)

def proccess_chapter(chapterdata):
    for x in chapterdata.paragraphs:
        proccess_paragraph(x)

def proccess_paragraph(paragraphdata):
    for x in paragraphdata.sentences:
        proccess_sentence(x)

def proccess_sentence(sentencedata):
    for x in sentencedata.words:
        proccess_word(x)

def proccess_word(worddata):
    pass
