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
        }
    return record

def print_csv_files(book, filename):
    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(filename + '.csv', 'wb') as f:
        header = ["author", "lex_rich", "sents_pp_mean", "sents_pp_std", "words_sent_mean",
                  "words_sent_std", "commas_sent_mean", "semis_sent_mean", "word_sparsity"]
        writer = csv.writer(f)
        writer.writerow(header)
        for chapter in book.chapters:
            if chapter.stat_features != None:
                data = [chapter.stat_features[key] for key in header]
                writer.writerow(data)

def main(args):
    samples=[]
    records=[]
    for x in text_format.getnames():
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
            print_csv_files(sample, filepath)
        else:
            with open(filepath) as statfile:
                record=pickle.load(statfile)
        samples.append(sample)
        records.append(record)

parser = argparse.ArgumentParser(description="Perform data mining on test set")
parser.add_argument('-f','--force',
                    dest='force',
                    action='store_true',
                    help='recalculate all stats')
args = parser.parse_args()
main(args)
