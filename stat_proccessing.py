import numpy as np

def proccess_book(book):
    data = filter(None, [proccess_chapter(x) for x in book.chapters])

def proccess_chapter(chapter):
    words = chapter.get_words()
    if len(words) > 100:
        #Get the lexical richness, and the average length per paragraph
        lex_rich = float(len(words)) / len(set(words))
        sents_per_pp = np.array([len(x.sentences) for x in chapter.paragraphs])
        
        #Get the average length per sentence, comma per sentence, and semicolon per sentence
        (ls, cs, ss) = get_frequencies(chapter)
        words_per_sent = np.array(ls)
        commas_per_sent = np.array(cs)
        semis_per_sent = np.array(ss)
        
        return (lex_rich, sents_per_pp.mean(), sents_per_pp.std(), words_per_sent.mean(),
                words_per_sent.std(), commas_per_sent.mean(), semis_per_sent.mean())
    return None
        
def get_frequencies(chapter):
    """ Compute lengths, comma counts, and semicolon counts for each paragraph in a chapter """
    ls, cs, ss = ([] for i in range(3))
    for p in chapter.paragraphs:
        (x,y,z) = proccess_paragraph(p)
        ls += x
        cs += y
        ss += z
    return (ls, cs, ss)

def count_p(p, words):
    """ Count the number of words that end with the char p """
    return sum(1 for w in words if w.text.endswith(p))
        
def proccess_paragraph(paragraph):
    """ Compute the lengths, comma count, and semicolon count for each sentence in a paragraph"""
    lengths = [len(x.words) for x in paragraph.sentences]
    commas = [count_p(',', x.words) for x in paragraph.sentences]
    semis = [count_p(';', x.words) for x in paragraph.sentences]
    return (lengths, commas, semis)

def proccess_sentence(sentence):
    pass

def proccess_word(word):
    pass



