import text_format
import text_proccessing
import stat_proccessing

import argparse
import os
import pickle

def stat_record(name,sample):
    record={
        "name":name,
        "author":sample.author,
        }
    return record

def main(args):
    records=[]
    for x in text_format.getnames(author=args.author):
        basefilepath="stat/"+x
        if ( not os.path.exists(basefilepath) ) or args.force:
            sample=text_format.get(x)
            for i in range(len(sample.chapters)):
                chap=sample.chapters[i]
                text_proccessing.proccess_chapter(chap)
                record=stat_proccessing.proccess_chapter(chap)
                filepath=("-Ch"+str(i)+".").join(basefilepath.split("."))
                with open(filepath,"w") as statfile:
                    pickle.dump(record,statfile)
                records.append(record)
        else:
            counter=0
            while True:
                record=None
                try:
                    with open(("-Ch"+str(counter)+".").join(basefilepath.split("."))) as statfile:
                        record=pickle.load(statfile)
                    records.append(record)
                except:
                    break
                counter=counter+1

parser = argparse.ArgumentParser(description="Perform data mining on test set")
parser.add_argument('-f','--force',
                    dest='force',
                    action='store_true',
                    help='recalculate all stats')
parser.add_argument('-a','--author',
                    dest='author',
                    action='store',
                    help='recalculate one author')
args = parser.parse_args()
main(args)
