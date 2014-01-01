# -*- coding:utf-8 -*-

from suffix_tree import GeneralisedSuffixTree
def test():
    stree = GeneralisedSuffixTree(['mississippi'])
    for shared in stree.sharedSubstrings(2):
        for seq,start,stop in shared:
            print seq, '['+str(start)+':'+str(stop)+']',
            print stree.sequences[seq][start:stop],
            print stree.sequences[seq][:start]+'|'+stree.sequences[seq][start:stop]+'|'+stree.sequences[seq][stop:]


def getMAXchSTR(string):
    stree = GeneralisedSuffixTree([string])
    ## record the max length of shared substring and the substring
    maxlength = 0;register = ""
    for shared in stree.sharedSubstrings(15):  ## five chinese characters
        for seq,start,stop in shared:
            if (stop-start) > maxlength:
                maxlength = stop - start
                register  = stree.sequences[seq][start:stop]
    #print type(register),register.decode('utf8')
    return maxlength,register


if __name__=="__main__":
    print getMAXchSTR("非常好的的 非常好的的")
