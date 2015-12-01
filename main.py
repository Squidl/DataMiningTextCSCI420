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
from subprocess import call


minwords=100

wordpattern = re.compile("^[A-Za-z]+$")
def is_valid_word(word):
    return True if wordpattern.match(word) else False


def stat_record(name,sample):
    record={
        "name":name,
        "author":sample.author,
        "chapters":[{"stats":chap.stat_features,
                     "words":chap.chapter_register["word_freq_dict"],
                     "usage":chap.chapter_register["usage_freq_dict"],
                     "topic":chap.chapter_register["topic_freq_dict"],
                     "region":chap.chapter_register["region_freq_dict"],
                     "sense":chap.chapter_register["sense_dist_dict"],
                     "character_ngrams":chap.chapter_register["character_ngrams"],
                     "word_ngrams":chap.chapter_register["word_ngrams"]
                     }
                          for chap
                          in sample.chapters
                          if chap.chapter_register["validwords"]>minwords]
        }
    return record

header_dict = OrderedDict([
    ("author",{"type":"{%s}"%(", ".join(text_format.getauthors())),"set":"id","use":True}),
    ("chapter_number",{"type":"numeric","set":"id","use":False}),
    ("lex_rich",{"type":"numeric","set":"stat","use":True}),
    ("sents_pp_mean",{"type":"numeric","set":"stat","use":True}),
    ("sents_pp_std",{"type":"numeric","set":"stat","use":True}),
    ("words_sent_mean",{"type":"numeric","set":"stat","use":True}),
    ("words_sent_std",{"type":"numeric","set":"stat","use":True}),
    ("commas_sent_mean",{"type":"numeric","set":"stat","use":True}),
    ("semis_sent_mean",{"type":"numeric","set":"stat","use":True}),
    ("commas_word_mean",{"type":"numeric","set":"stat","use":True}),
    ("semis_word_mean",{"type":"numeric","set":"stat","use":True})
])


def print_csv_files(records, filename):
    #print(text_format.getauthors())
    if filename.endswith('.txt'):
        filename = filename[:-4]
    header=[x for x in header_dict.keys() if header_dict[x]["use"] and (usestat or header_dict[x]["set"]!="stat")]
    with open(filename + '.arff', 'wb') as f:
        f.write("@relation %s\n\n"%filename.split("/")[-1].split(".")[0])
        for k in header:
            f.write("@attribute %s %s\n"%(k,header_dict[k]["type"]))
        if wordfreq:
            most_words=findbest([chapter["words"]
                                 for record in records
                                 for chapter in record["chapters"]],
                                filter=is_valid_word)
            for k in most_words:
                f.write("@attribute wfreq_%s numeric\n"%k)
        if usagefreq:
            most_use=findbest([chapter["usage"]
                               for record in records
                               for chapter in record["chapters"]],
                              t=True)
            for k in most_use:
                f.write("@attribute ufreq_%s numeric\n"%(k.replace(".","_")))
        if topicfreq:
            most_topic=findbest([chapter["topic"]
                                 for record in records
                                 for chapter in record["chapters"]],
                                t=True)
            for k in most_topic:
                f.write("@attribute tfreq_%s numeric\n"%(k.replace(".","_")))
        if regionfreq:
            most_region=findbest([chapter["region"]
                                  for record in records
                                  for chapter in record["chapters"]],
                                 t=True)
            for k in most_region:
                f.write("@attribute rfreq_%s numeric\n"%(k.replace(".","_")))
        if sensefreq:
            for k in ["pos","neg","obj"]:
                f.write("@attribute sfreq_%s numeric\n"%k)
        most_ngrams={}
        if charngrams:
            for n in text_proccessing.character_ngrams:
                most_ngrams[n]=findbest([chap["character_ngrams"][n]
                                         for record in records
                                         for chap in record["chapters"]],
                                        t=True)
                for k in most_ngrams[n]:
                    f.write("@attribute c%sgram_%s numeric\n"%(str(n),"".join(k)))
        most_wngrams={}
        if wordngrams:
            for n in text_proccessing.word_ngrams:
                most_wngrams[n]=findbest([chap["word_ngrams"][n]
                                         for record in records
                                         for chap in record["chapters"]],
                                         t=True,
                                         filter=lambda x: not False in [is_valid_word(y) for y in x])
                for k in most_wngrams[n]:
                    f.write("@attribute c%sgram_%s numeric\n"%(str(n),"".join(k)))
        f.write("\n\n@data\n")
        writer = csv.writer(f)
        for record in records:
            for i in range(len(record["chapters"])):
                chapter=record["chapters"][i]
                if chapter != None:
                    chapter["stats"]["chapter_number"]=i
                    data = [chapter["stats"][key] for key in header]
                    if wordfreq:
                        data += [chapter["words"][key] for key in most_words]
                    if usagefreq:
                        data += [chapter["usage"][key] for key in most_use]
                    if topicfreq:
                        data += [chapter["topic"][key] for key in most_topic]
                    if regionfreq:
                        data += [chapter["region"][key] for key in most_region]
                    if sensefreq:
                        data += [chapter["sense"][key] for key in ["pos","neg","obj"]]
                    if charngrams:
                        for n in text_proccessing.character_ngrams:
                            data += [chapter["character_ngrams"][n][key] for key in most_ngrams[n]]
                    if wordngrams:
                        for n in text_proccessing.word_ngrams:
                            data += [chapter["word_ngrams"][n][key] for key in most_wngrams[n]]
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
        if args.weka:
            call(["weka",combinedFileName+".arff"])

parser = argparse.ArgumentParser(description="Perform data mining on test set")
parser.add_argument('--async',
                    dest='async',
                    action='store_true',
                    help='use multiple threads')
parser.add_argument('-f','--force',
                    dest='force',
                    action='store_true',
                    help='recalculate all stats')
parser.add_argument('-t','--texts',
                    dest='texts',
                    action='store',
                    help='recalculate only for texts in comma seperated paths')
parser.add_argument('-a','--author',
                    dest='author',
                    action='store',
                    help='recalculate only for authors in comma seperated list')
parser.add_argument('-o','--output',
                    dest='output',
                    action='store',
                    help='set combined output')
parser.add_argument('-w','--weka',
                    dest='weka',
                    action='store_true',
                    help='Chain opening combined output in weka. Must we used with -o.')
parser.add_argument('-s','--nostat',
                    dest='hidestat',
                    action='store_true',
                    help='Hides the flat stats.')
for x in ["wordfreq","usagefreq","regionfreq","topicfreq","sensefreq","charngrams","wordngrams"]:
    parser.add_argument("--"+x,
                        dest=x,
                        action="store_true",
                        help="calculate %s attributes"%x)
parser.add_argument("--allfreq",
                    dest="allfreq",
                    action="store_true",
                    help="calculate all frequencies")

args = parser.parse_args()
wordfreq=args.wordfreq
usagefreq=args.usagefreq
regionfreq=args.regionfreq
topicfreq=args.topicfreq
sensefreq=args.sensefreq
charngrams=args.charngrams
wordngrams=args.wordngrams
usestat=not args.hidestat
if(args.allfreq):
    wordfreq = True
    usagefreq = True
    regionfreq = True
    topicfreq = True
    sensefreq = True
    charngrams = True
    wordngrams = True
    usestat = True
main(args)
