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

def print_csv_files(record, filename):
    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(filename + '.csv', 'wb') as f:
        header = ["author", "lex_rich", "sents_pp_mean", "sents_pp_std", "words_sent_mean",
                  "words_sent_std", "commas_sent_mean", "semis_sent_mean", "word_sparsity"]
        writer = csv.writer(f)
        writer.writerow(header)
        for chapter in record["chapters"]:
            if chapter != None:
                data = [chapter[key] for key in header]
                writer.writerow(data)

def main(args):
    records=[]
    texts=[]
    if args.texts is not None:
        texts=args.text.split(",")
    else:
        text_format.getnames(authors=args.author.split(","))
    for x in texts:
        sample=None
        record=None
        filepath="stat/"+x
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
args = parser.parse_args()
main(args)
