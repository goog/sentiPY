# -*- coding:utf-8 -*-
import re
import os
from shutil import copyfile
from preprocess import *
from suffixTEST import getMAXchSTR
'''tools'''


## load each line as a single key 
def file2dic(path):
    with open(path) as fo:
        dictionary = {}
        for line in fo:
            line =line.strip()
            if line:
                dictionary[line] = 1
    print "the length of the dictionary is %s " %(len(dictionary))
    return dictionary
            

def checkoutPHRASE(path):
    ## path to the final phrase,return empty phrase line number
    emptyLIST=[]
    fo =open(path)
    flag=0
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------":
                lineNO+=1
                if flag==1:
                    emptyLIST.append(lineNO)
                flag=1
            else:
                flag=0
    print "the length of empty phrase reviews is:",len(emptyLIST)
    return emptyLIST


def reviewNOphrase():
    list  = checkoutPHRASE('phraseRANK.txt')  # analyze the final phrase
    fo = open('./pos_tagged.txt')
    fw = open('reviewNOphrase.txt','w')
    buf = ""
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="---------#NR -#PU":  ## change with segmenter
                lineNO+=1
                if lineNO in list:
                    fw.write(buf+'*_*\n')
                buf=''
            else:
                buf+=' '+line
    fw.close()


def writeERROR(path,list):
    fo = open(path)
    fw = open('errorLINES.txt','w')
    buf = ""
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------":
                lineNO+=1
                if lineNO in list:
                    fw.write(str(lineNO)+':'+buf+'*_*\n')
                buf=''
            else:
                buf+=line
    fw.close()

    fo = open('neg_tagged.txt')
    fw = open('errorTAG.txt','w')
    buf = ""
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="--#NN --#NN --#NN --#NN --#NN":
                lineNO+=1
                if lineNO in list:
                    fw.write(str(lineNO)+':'+buf+'*_*\n')
                buf=''
            else:
                buf+=line
    fw.close()

    fo = open('neg_phrase.txt')
    fw = open('errorphrase.txt','w')
    buf = ""
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------":
                lineNO+=1
                if lineNO in list:
                    fw.write(str(lineNO)+':'+buf+'*_*\n')
                buf=''
            else:
                buf+=line+' '
    fw.close()
    
    

def countPHRASE(path):
    len1=0;len2=0;len3=0;lenx=0
    fo = open(path)
    for line in fo:
        line=line.strip()
        if line:
            num =len(line.split())
            if num==1:
                len1+=1
            elif num==2:
                len2+=1
            elif num==3:
                len3+=1
            else:
                lenx+=1
    print "the number of length 1 2 3 and more than three in a phrase is %s %s %s %s" %(len1,len2,len3,lenx)

def findLABELS(path):
    fo = open(path)  # "./pos_phrase.txt"
    a= set()
    for line in fo:
        line = line.strip()
        index = line.find('#')
        if index!=-1:
            a.add(line[index+1:])
    print a

def file2count(path):
    ## read a file ,output  k,v
    fo =open(path)
    dict = {}
    for line in fo:
        line = line.strip()
        if line:
            if dict.get(line):
                dict[line]+=1
            else:
                dict[line]=1
    for i in dict.keys():
        print i,dict[i]
    
def checkLABELED(path1,path2):
    dict1={}
    dict2={}
    fo1 = open(path1)  #'./1.txt'
    fo2 = open(path2)  #'./2.txt'
    fw=open('./senti.txt','a')
    for line in fo1:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                    dict1[kv[0]]=kv[1]
                except:
                    print kv[0],"value not float."    
    print "dict1 length is %s" %len(dict1)


    for line in fo2:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                    dict2[kv[0]]=kv[1]
                except:
                    print kv[0]
    print "dict2 length is %s" %len(dict2)

    a = set(dict1.keys())
    b = set(dict2.keys())
    c = a|b
    print "the total length is %s" %len(c)
    flag=0
    for i in c:
        if i=="自我":
            flag=1
        if flag:
        
            try:
                
                if dict1.get(i)==dict2.get(i):
                    fw.write(i+"   "+dict1.get(i)+"\n")
                else:
                    if dict1.get(i) and dict2.get(i):
                        if abs(int(dict1.get(i))-int(dict2.get(i)))<=1:
                            avg= (int(dict1.get(i))+int(dict2.get(i)))/2.0
                            fw.write(i+"   "+str(avg)+"\n")
                        else:
                            print i,"   ",dict1.get(i),"   ",dict2.get(i)
                            r=raw_input("type a value:")
                            fw.write(i+"   "+r+"\n")
                            
                            
                    else:
                        print i,"   ",dict1.get(i),"   ",dict2.get(i)
                        r=raw_input("type a value:")
                        fw.write(i+"   "+r+"\n")
            except:
                print i
    fw.close()


def adjust(path1,path2):
    dict1={}
    dict2={}
    fo1 = open(path1)  #'./1.txt'
    fo2 = open(path2)  #'./2.txt'
    fw=open('./senti2.txt','w')
    for line in fo1:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                    dict1[kv[0]]=kv[1]
                except:
                    print kv[0],"value not float."    
    print "dict1 length is %s" %len(dict1)


    for line in fo2:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                    dict2[kv[0]]=kv[1]
                except:
                    print kv[0]
    print "dict2 length is %s" %len(dict2)

    
    for i in dict1.keys():
            
        if dict1.get(i)==dict2.get(i):
            continue
        else:
            if dict1.get(i) and dict2.get(i):
                if abs(float(dict1.get(i))-float(dict2.get(i)))<=1:
                    avg= (float(dict1.get(i))+float(dict2.get(i)))/2.0
                    dict1[i]=str(avg)
                else:
                    print i,"   ",dict1.get(i),"   ",dict2.get(i)
                    r=raw_input("type a value:")
                    dict1[i]=r
                    
    for i in dict1.keys():
        fw.write(i+"   "+dict1.get(i)+"\n")
    fw.close()

import re
hanLAB = re.compile(ur'[\u4e00-\u9fa5]+   -?[\d.]+')
def splitLABEL(path,path1):
    fo = open(path)
    fw = open(path1,'w')
    for line in fo:
        line=line.strip()
        li = hanLAB.findall(line.decode('utf8'))
        if li:
            print len(li)
            for j in li:
                fw.write(j.encode('utf8')+"\n")
    fw.close()
                
        

def doOOV():
    fo1 = open('./oov.txt')
    fo2 = open('./oov1.txt')
    a =set()
    b= set()
    for line in fo1:
        line=line.strip()
        if line:
            a.add(line.split()[0])

    #print len(a)


    for line in fo2:
        line=line.strip()
        if line:
            b.add(line)

    print  len(b-a)        
    for i in (b -a):
        print i

def processADVSS(path):
    ## ./advss.txt
    dict = {}
    fo=open(path)
    fw=open('./finalADVSS.txt','w')
    for line in fo:
        line=line.strip()
        if line:
            li=line.split()
            if li[0] in ['也','都','就','却','还是']:
                #remove non-intensitive 
                fw.write(' '.join(li[1:])+'\n')
            else:
                fw.write(line+'\n')
            if dict.get(li[0]):
                dict[li[0]]+=1
            else:
                dict[li[0]]=1
##    for i in dict.keys():
##        print i,dict[i]
        
    fw.close()

def recordOOV(oov):
    fw = open('oov.txt','w')
    for i in oov:
        fw.write(i+'   \n')
    fw.close()
    print "the length of OOV is %s" %(len(oov))


def processADVS(line):
    li=line.split()
    if len(li)==3:
        if ''.join(li[:2])=='不太':
            return '不太 '+li[2]+'\n'  ## minus -5
    return line+'\n'


palAD= re.compile(ur'[\u4e00-\u9fa5]+#AD.*')
palVE= re.compile(ur'[\u4e00-\u9fa5]+#VE.*')
def findADorVE(phrase):
    li = phrase.split('#PU')
    if len(li)==2:
        phrase = li[1]
    m = palAD.search(phrase.decode('utf8'))
    m2=palVE.search(phrase.decode('utf8'))
    if m:
        phrase = m.group().encode('utf8')
    elif m2:
        phrase = m2.group().encode('utf8')
    return phrase



def checkOOV(path1,path2):
    dict1={}
    fo1 = open(path1)  #'./sentiment_yb.txt'
    fo2 = open(path2)  #'./oov.txt'
    fw=open('./oov2.txt','w')
    for line in fo1:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                    dict1[kv[0]]=kv[1]
                except:
                    print kv[0],kv[1]
                
    print "dict1 length is %s" %len(dict1)


    for line in fo2:
        line=line.strip()
        if line:
            if not dict1.get(line):
                print "%s isn't in sentiment_yb" %line
            else:
                print line,':',dict1.get(line)
            r=raw_input("type a value:")
            if r=='':
                continue
            else:
                fw.write(line+"   "+r+"\n")
    fw.close()

def rmOOVinLEXICON(path):
    fo =open(path)
    fw= open('./oovRESERVE.txt','w')
    li=[]
    for line in fo:
        line=line.strip()
        if line:
            print line
            r=raw_input("remove it? [y/n]:")
            if r=='y' or r=='Y' or r=='':
                li.append(line)
            else:
                fw.write(line+'\n')
    print 'there is %s words to be removed!' %len(li)
    fw.close()

    with open('pos.txt') as f, open('pos_rm.txt',"w") as working:
        for line in f:
            line=line.strip()
            if line:
                if line in li:
                    continue
                else:
                    working.write(line+'\n')
    os.rename('pos_rm.txt','pos.txt')

    with open('neg.txt') as f, open('neg_rm.txt',"w") as working:
        for line in f:
            line=line.strip()
            if line:
                if line in li:
                    continue
                else:
                    working.write(line+'\n')
    os.rename('neg_rm.txt','neg.txt')


def fixedLEN(path):
    fo =open(path)
    fw= open('./cedict1.txt','w')
    for line in fo:
        line=line.strip()
        if line:
            if len(line)==9 or len(line)==12:
                fw.write(line+'\n')
    fw.close()

def applyPAT(pat,line,isCH=None,sub=' '):
    if isCH:
        m = pat.findall(line.decode('utf8'))
        if m:
            for i in m:
                line = line.replace(i.encode('utf8'),sub)
    else:
        m = pat.findall(line)
        if m:
            for i in m:
                line = line.replace(i,sub)
    return line

def loadASPECTsenti(path):
    dic = {}
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line:
                li = line.split()
                if len(li)==3:
                    if dic.get(' '.join(li[0:2])):
                        continue
                    else:
                        dic[' '.join(li[0:2])]=li[2]
    return dic

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# split more than 80 tokens
def splitLONG(line,manual=False):
    '''
    param: i, segmented line
    return the smaller length sentence list
    '''
    sentenceLI= []
    list1=line.split('，')
    for j in list1:
        j = j.strip()
        if j:
            if len(j.split())<81:
                sentenceLI.append(j)
            else:
                jlist = j.split(',')
                for k in jlist:
                    k = k.strip()
                    if k:
                        if len(k.split())<81:
                            sentenceLI.append(k)
                        else:
                            if not manual:
                                print "this too long sentence can't be split by delimiter"
                                if getMAXchSTR(k)[0]:  ## repeat detect, also used for spam
                                    key = getMAXchSTR(k)[1]   ## the key is utf8
                                    sentenceLI.append(key)
                                else:
                                ##chunk the long sentence to the fixed sentences
                                    ge = chunks(k.split(),80)
                                    for i in ge:
                                        sentenceLI.append(' '.join(i))
                            else:
                                print "this sentence can't be split:\n",k
                                r=raw_input("input man-made sentence:")
                                list2 = r.split('\\n')
                                for l in list2:
                                    sentenceLI.append(l)
    return sentenceLI
                        
## post-process the seged file
###define a regx
sen = re.compile(ur'\u3002|\uff0e|\uff01|\uff1f|\?|!|\.')
def getSENTENCE(path):
    ## sentence length :80 tokens
    with open(path) as f,open('sentences.txt','w') as fw:
        for line in f:
            line=line.strip()
            if line:
                if line=='-- -- -- -- --':
                    fw.write(line+'\n')
                else:
                    li = sen.split(line.decode('utf8')) #### split the seged file
                    for i in li:
                        i = i.strip().encode('utf8')
                        if i:
                            if len(i.split())< 81:
                                fw.write(i+'\n')
                            else:
                                list2 = splitLONG(i)
                                for s in list2:
                                    if s:
                                        fw.write(s+'\n')
    fw.close()
    copyfile('sentences.txt',path+'.backup')  
    os.rename('sentences.txt',path)


## post-process the seged file  , ##todo : remove above method                      
def splitSegmented(path,path2):
    ## sentence length :80 tokens
    with open(path) as f,open(path2,'w') as fw:
        for line in f:
            line=line.strip()
            if line:
                if line=='-- -- -- -- --':
                    fw.write(line+'\n')
                else:
                    li = sen.split(line.decode('utf8')) #### split the seged file
                    for i in li:
                        i = i.strip().encode('utf8')
                        if i:
                            if len(i.split())< 81:
                                fw.write(i+'\n')
                            else:
                                list2 = splitLONG(i)
                                for s in list2:
                                    if s:
                                        fw.write(s+'\n')
    fw.close()

def statSENTENCES(path):
    cnt = 0
    maxl = 1
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line:
                if line!='-- -- -- -- --':
                    length = len(line.split())
                    if length > maxl:
                        maxl = length
                    if length >80:
                        print line
                        cnt+=1
    print cnt,maxl
    
def statPARSED(path):
    cnt = 0
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line=='':
                cnt+=1
    print cnt

def reformPARSED(path,path2):
    with open(path) as f,open(path2,'w') as fw:
        li = []
        for line in f:
            line=line.strip()
            if line:
                li.append(line)
            else:
                fw.write('   '.join(li)+'\n')
                li = []
    fw.close()


def checkDICT(path,path2):
    a = file2set(path)
    print len(a)

    b = file2set(path2)
    print len(b)
    with open(path2) as fo:
        for line in fo:
            line=line.strip()
            if line and (line not in a):
                print line

def diffTWOfile(path1,path2):
    a = set()
    b= set()
    with open(path1) as org,open(path2) as dec:
        for line in org:
            if line:
                if line.strip().split()[0] in a:
                    print line.strip().split()[0]
                a.add(line.strip().split()[0])

        for line in dec:
            if line:
                b.add(line.strip().split()[0])
    print len(a),len(b)
    c= a-b
    for i in c:
        print i
    
                    
if __name__ == '__main__':
##    processADVSS('./advss.txt')
##    print findADorVE('几乎#AD没有#VE什么#DT合口味#NN')
    #checkOOV('./sentiment_yb.txt','./oov.txt')
    #rmOOVinLEXICON('./oov.txt')
    #fixedLEN('./cedict.txt')
    reviewNOphrase()
    #print loadASPECTsenti('./aspectDICT.txt')
##    getSENTENCE('./neg_seged.txt')
    statSENTENCES('./pos_seged.txt')
##    statPARSED('./pos_parsed.txt')
##    reformPARSED('pos_parsed.txt','pos_parsed_format.txt')
    #checkDICT('positive.txt','NTUSD_positive_simplified.txt')
    #adjust('sentiment.txt','lexicon2.txt')
    #splitLABEL("senti2.txt","senti3.txt")
    #diffTWOfile("sentiment2.txt","mySTRENGTH.txt")
    pass
