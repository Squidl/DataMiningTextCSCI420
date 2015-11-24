#!/usr/bin/python

import text_format
import text_proccessing
import stat_proccessing

import argparse
import os
import pickle
import csv

def stat_record(name,sample):
    record={
        "name":name,
        "author":sample.author,
        "chapters":[chap.stat_features for chap in sample.chapters]
        }
    return record

combinedInitialized = False
combinedFileName = None

def print_csv_files(record, filename):
    global combinedInitialized
    #print(text_format.getauthors())
    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(filename + '.csv', 'wb') as f:
        header = ["author", "lex_rich", "sents_pp_mean", "sents_pp_std", "words_sent_mean",
                  "words_sent_std", "commas_sent_mean", "semis_sent_mean"]
        header2 = ["w_spars_{}".format(i+1) for i in range(0, 10)]
        writer = csv.writer(f)
        writer.writerow(header + header2)
        totalFile=None
        if combinedFileName is not None:
            totalFile = open(combinedFileName, 'a')
            writer2 = csv.writer(totalFile)
            if not combinedInitialized:
                writer2.writerow(header + header2)
                combinedInitialized = True
        for chapter in record["chapters"]:
            if chapter != None:
                data = [chapter[key] for key in header]
                data += chapter["word_sparsity"]
                writer.writerow(data)
                if combinedFileName is not None:
                    writer2.writerow(data)
        if totalFile is not None:
            totalFile.close()

def main(args):
    records=[]
    texts=[]
    if combinedFileName is not None and (os.path.exists(combinedFileName) ):
        print("Combined file already exists")
        exit(1)
    if args.texts is not None:
        texts=args.text.split(",")
    else:
        authors=None
        if args.author is not None:
            authors=args.author.split(",")
        texts=text_format.getnames(authors=authors)
    for x in texts:
        sample=None
        record=None
        filepath="stat/"+x
        if ( not os.path.exists(filepath) ) or args.force:
            print("Loading file : {}.".format(x))
            sample=text_format.get(x)
            print(len(sample.chapters))
            stat_proccessing.proccess_book(sample)
            text_proccessing.proccess_book(sample)
            record=stat_record(x,sample)
            with open(filepath,"w") as statfile:
                pickle.dump(record,statfile)
        else:
            with open(filepath) as statfile:
                record=pickle.load(statfile)
        records.append(record)
        print_csv_files(record, filepath)

parser = argparse.ArgumentParser(description="Perform data mining on test set")
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
                    help='recalculate one author')
parser.add_argument('-o','--output',
                    dest='output',
                    action='store',
                    help='set combined output')
args = parser.parse_args()
if args.output is not None:
    combinedFileName='stat/'+args.output
main(args)
