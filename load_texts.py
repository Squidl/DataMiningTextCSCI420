import pickle
from os import listdir

def load_texts(name,auth):
    data=None
    with open(text["dir"]+"/"+name) as f:
        data=f.read()
    ind = data.find("*** START OF THIS PROJECT GUTENBERG")
    if ind !=-1:
        data=data[ind+4:]
        ind=data.find("***")
        data=data[ind+4:]
    ind = data.find("*** END OF THIS PROJECT")
    if ind != -1:
        data=data[:ind]
    data=data.decode('unicode_escape')
    print(repr(data[:100]))
    return (name,auth,data)

def isyes(inp):
    return inp[0]=="y" or inp[0]=="Y"

def peek(filename):
    data=None
    with open(text["dir"]+"/"+filename) as f:
        data=f.read()
    print("")
    print("*"*80)
    print(data[:200])
    print("*"*80)
    print("")

def add_files_inter():
    anynew=False
    for path in listdir(text["dir"]):
        if path in text["dat"]:
            continue
        anynew=True
        if isyes( raw_input("Would you like to load "+path+"?") ):
            peek(path)
            auth=raw_input("What is the author's name?")
            text["dat"][path]=auth
    if not anynew:
        print("No new files")

settings_path="source_settings"
text=None
cached={}
try:
    with open(settings_path) as settingsfile:
        text=pickle.load(settingsfile)
except:
    text={"dir":"texts",
          "dat":{}}
if __name__=="__main__":
    print("source")
    print("filename\t\tAuthor")
    for k in text["dat"].keys():
        print("%s\t\t%s"%(k,text["dat"][k]))
    if isyes( raw_input("Would you like to add files to source?") ):
        add_files_inter()
    if isyes( raw_input("Would you like to modify the files?") ):
        for k in text["dat"].keys():
            peek(k)
            newau=raw_input("Author for "+k+":")
            if newau.strip() != "":
                text["dat"][k]=newau
    with open(settings_path,'w') as settingsfile:
        pickle.dump(text,settingsfile)

def get(name,cache=True):
    if cache and name in cached:
        return cached[name]
    else:
        result=load_texts(name,text["dat"][name])
        cached[name]=result
        return result

def getauthors():
    return list(set([text["dat"][k] for k in text["dat"].keys()]))

def getnames(authors=None):
    if authors is not None:
        return [name for name in text["dat"].keys() if text["dat"][name] in authors]
    else:
        return text["dat"].keys()
