#!/usr/bin/python

import text_format
import text_proccessing
import stat_proccessing

import argparse
import os
import pickle
import csv
from threading import Thread
from collections import OrderedDict


def stat_record(name,sample):
    record={
        "name":name,
        "author":sample.author,
        "chapters":[chap.stat_features for chap in sample.chapters]
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
    ("semis_sent_mean","numeric")
])

def print_csv_files(records, filename):
    #print(text_format.getauthors())
    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(filename + '.arff', 'wb') as f:
        f.write("@relation %s\n\n"%filename.split("/")[-1].split(".")[0])
        for k in header_dict.keys():
            f.write("@attribute %s %s\n"%(k,header_dict[k]))
        f.write("\n\n@data\n")
        header = header_dict.keys()
        #header2 = ["w_spars_{}".format(i+1) for i in range(0, 10)]
        writer = csv.writer(f)
        #writer.writerow(header + header2)
        for record in records:
            for i in range(len(record["chapters"])):
                chapter=record["chapters"][i]
                if chapter != None:
                    chapter["chapter_number"]=i
                    data = [chapter[key] for key in header]
                    #data += chapter["word_sparsity"]
                    writer.writerow(data)

def paraiter(x,resultplace,force=False):
    filepath="stat/"+x
    record=None
    if ( not os.path.exists(filepath) ) or args.force:
        print("Loading file : {}.".format(x))
        sample=text_format.get(x)
        print(len(sample.chapters))
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
        sample=None
        record=None
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
