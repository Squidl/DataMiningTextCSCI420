
def proccess_book(bookdata):
    for x in bookdata.chapters:
        proccess_chapters(x)

def proccess_chapter(chapterdata):
    for x in chapterdata.paragraph:
        proccess_paragraph(x)

def proccess_paragraph(paragraphdata):
    for x in paragraphdata.sentences:
        proccess_sentence(x)

def proccess_sentence(sentencedata):
    for x in sentencedata.chapters:
        proccess_word(x)

def process_word(worddata):
    pass
