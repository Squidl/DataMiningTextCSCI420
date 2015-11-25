#!/usr/bin/python

import text_format
import text_proccessing
import stat_proccessing
from frequency_vector import findbest

import argparse
import os
import re
import pickle
import csv
from threading import Thread
from collections import OrderedDict


def stat_record(name,sample):
    record={
        "name":name,
        "author":sample.author,
        "chapters":[{"stats":chap.stat_features,
                     "words":chap.chapter_register["word_freq_dict"]
                     }
                          for chap
                          in sample.chapters
                          if chap.chapter_register["validwords"]>100]
        }
    return record

header_dict = OrderedDict([
    ("author","{%s}"%(", ".join(text_format.getauthors())) ),
    ("chapter_number","numeric"),
    ("lex_rich","numeric"),
    ("sents_pp_mean","numeric"),
    ("sents_pp_std","numeric"),
    ("words_sent_mean","numeric"),
    ("words_sent_std","numeric"),
    ("commas_sent_mean","numeric"),
    ("semis_sent_mean","numeric"),
    ("commas_word_mean","numeric"),
    ("semis_word_mean","numeric")
])

wordpattern = re.compile("^[A-Za-z]+$")
def is_valid_word(word):
    return True if wordpattern.match(word) else False

def print_csv_files(records, filename):
    #print(text_format.getauthors())
    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(filename + '.arff', 'wb') as f:
        f.write("@relation %s\n\n"%filename.split("/")[-1].split(".")[0])
        for k in header_dict.keys():
            f.write("@attribute %s %s\n"%(k,header_dict[k]))
        most_words=findbest([chapter["words"]
                          for record in records
                          for chapter in record["chapters"]],
                            filter=is_valid_word)
        for k in most_words:
            f.write("@attribute w_%s_freq numeric\n"%k)
        f.write("\n\n@data\n")
        writer = csv.writer(f)
        for record in records:
            for i in range(len(record["chapters"])):
                chapter=record["chapters"][i]
                if chapter != None:
                    chapter["stats"]["chapter_number"]=i
                    data = [chapter["stats"][key] for key in header_dict.keys()]
                    data += [chapter["words"][key] for key in most_words]
                    writer.writerow(data)

def paraiter(x,resultplace,force=False):
    filepath="stat/"+x
    record=None
    if ( not os.path.exists(filepath) ) or args.force:
        print("Loading file : {}.".format(x))
        sample=text_format.get(x)
        text_proccessing.proccess_book(sample)
        stat_proccessing.proccess_book(sample)
        record=stat_record(x,sample)
        with open(filepath,"w") as statfile:
            pickle.dump(record,statfile)
    else:
        with open(filepath) as statfile:
            record=pickle.load(statfile)
    print_csv_files([record], filepath)
    resultplace.append(record)

def main(args):
    texts=[]
    results=[]
    combinedFileName=None
    if args.output is not None:
        combinedFileName='stat/'+args.output
        if combinedFileName is not None and (os.path.exists(combinedFileName) ):
            print("Combined file already exists")
            exit(1)
    if args.texts is not None:
        texts=args.texts.split(",")
    else:
        authors=None
        if args.author is not None:
            authors=args.author.split(",")
        texts=text_format.getnames(authors=authors)
    threads=[]
    for x in texts:
        if args.async:
            newb=[]
            newthr=Thread(target=paraiter, args=(x, newb, args.force))
            newthr.start()
            threads.append(newthr)
            results.append(newb)
        else:
            newb=[]
            paraiter(x, newb, args.force)
            results.append(newb)
    for t in threads:
        t.join()
    fres=[result[0] for result in results if len(result)>0]
    if combinedFileName is not None:
        print_csv_files(fres,combinedFileName)

parser = argparse.ArgumentParser(description="Perform data mining on test set")
parser.add_argument('-f','--force',
                    dest='force',
                    action='store_true',
                    help='recalculate all stats')
parser.add_argument('--async',
                    dest='async',
                    action='store_true',
                    help='user multiple threads')
parser.add_argument('-t','--texts',
                    dest='texts',
                    action='store',
                    help='recalculate only for texts in comma seperated paths')
parser.add_argument('-a','--author',
                    dest='author',
                    action='store',
                    help='recalculate one author')
parser.add_argument('-o','--output',
                    dest='output',
                    action='store',
                    help='set combined output')
args = parser.parse_args()
main(args)
