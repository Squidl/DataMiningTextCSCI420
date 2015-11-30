from collections import OrderedDict

def findbest(freqdicts,n=10,filter=None,t=False):
    total=freqdict()
    for newdict in freqdicts:
        for key in newdict.keys():
            if filter is not None:
                if not filter(key):
                    continue
            total.plusplus(key,newdict[key])
        # assumed normalized
        # norm=normalize(newdict)
        # total.dictplusplus(newdict)
    return top_n(total,n=n).keys()

def normalize(tonorm,copy=False,cachetotal=None):
    if copy:
        tonorm=dict(tonorm)
    total=None
    if cachetotal is None:
        total=sum(tonorm.values())
    else:
        total=tonorm[cachetotal]
    for k in tonorm.keys():
        tonorm[k]=float(tonorm[k])/total
    return tonorm

def top_n(freq,n=10):
    return OrderedDict(sorted(freq.items(),key=lambda t: 0-t[1] )[:n])

class freqdict(dict):
    def __init__(self, *args, **kwargs):
        super(freqdict,self).__init__()
        self.default=0
        if "default" in kwargs:
            self.default=kwargs["default"]
    def __getitem__(self, key):
        if key in self:
            return super(freqdict,self).__getitem__(key)
        else:
            return self.default
    def plusplus(self, key, number=1):
        newval=float(self[key])+float(number)
        self[key]=newval
        return newval
    def dictplusplus(self, other):
        for k in other.keys():
            self.plusplus(k,other[k])

debug=False
if debug:
    newcount=freqdict()
    newcount.plusplus("goo",6)
    newcount.plusplus("goo",7)
    newcount.plusplus("ga",5)
    newcount.plusplus("gee",6)
    newcount.plusplus("ga",6)
    count=freqdict()
    count.plusplus("goo",6)
    count.plusplus("goo",7)
    count.plusplus("ga",5)
    count.plusplus("gee",6)
    count.plusplus("ga",6)
    #total=freqdict()
    #total.dictplusplus(newcount)
    #total.dictplusplus(count)
    print(count)
    print(newcount)
    #print(total)
    print(findbest([count,newcount],n=2))
