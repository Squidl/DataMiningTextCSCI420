import text_format
import text_proccessing
import stat_proccessing

import argparse
import os
import pickle

def stat_record(name,sample):
    record={
        "name":name
        }
    return record

def main(args):
    samples=[]
    records=[]
    for x in text_format.getnames():
        sample=None
        record=None
        filepath="stat/"+x
        if ( not os.path.exists(filepath) ) or args.force:
            sample=text_format.get(x)
            text_proccessing.proccess_book(sample)
            stat_proccessing.proccess_book(sample)
            record=stat_record(x,sample)
            with open(filepath,"w") as statfile:
                pickle.dump(record,statfile)
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
