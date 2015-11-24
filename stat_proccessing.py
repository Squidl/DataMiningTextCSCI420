import numpy as np
import nltk

def proccess_book(book):
    for chapter in book.chapters:
        proccess_chapter(chapter, book.author)    

def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def proccess_chapter(chapter, author):
    words = chapter.get_words()
    if len(words) > 500:
        #Get the lexical richness, and the average length per paragraph
        lex_rich = float(len(words)) / len(set(words))
        sents_per_pp = np.array([len(x.sentences) for x in chapter.paragraphs])
        #Get the average length per sentence, comma per sentence, and semicolon per sentence
        (ls, cs, ss) = get_frequencies(chapter)
        words_per_sent = np.array(ls)
        commas_per_sent = np.array(cs)
        semis_per_sent = np.array(ss)
        
        top_ten = nltk.FreqDist(words).most_common(10)
        top_ten_frequencies = [float(freq * 100) / len(words) for (word,freq) in top_ten]
        
        chapter.stat_features = {
            "author" : author,
            "lex_rich": lex_rich,
            "sents_pp_mean": sents_per_pp.mean(),
            "sents_pp_std" : sents_per_pp.std(),
            "words_sent_mean" : words_per_sent.mean(),
            "words_sent_std" : words_per_sent.std(),
            "commas_sent_mean" : commas_per_sent.mean(),
            "semis_sent_mean" : semis_per_sent.mean(),
            "commas_word_mean" : float(commas_per_sent.sum())/words_per_sent.sum(),
            "semis_word_mean" : float(semis_per_sent.sum())/words_per_sent.sum(),
            "word_sparsity" : top_ten_frequencies
        }
        
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
    return sum(1 for w in words if w.endswith(p))
        
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



