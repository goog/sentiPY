# -*- coding:utf-8 -*-
from preprocess import *
from evaluate import *
from check import *
import os
import time
from nlp import parser,StanfordNLP,parser1
import numpy as np
import pymongo
from eigenvector import ev
#from plumbum.cmd import cat
#from plumbum import local
from datetime import datetime, timedelta
from time import mktime
from NPfindOP import opinionSEARCH3
from featurePIPE import countSTREAM,showCOUNT
pwd = os.path.dirname(os.path.realpath(__file__))

#load the sentiment lexicon
def loadSENTI(path):
    fo = open(path)
    sentiDICT = {}
    for line in fo:
        line =line.strip()
        if line:
            li= line.split()
            if len(li)==2:
                try:
                    sentiDICT[li[0]]= float(li[1])
                except:
                    print "type error, not number",line
    print "Length of sentiment lexion in %s is %s " %(fo.name,len(sentiDICT))
    return sentiDICT

# load the non-linear sentiment lexicon
def loadLEXICON(path):
    with open(path) as fo:
        lexicon = {}
        for line in fo:
            line =line.strip()
            if line:
                li= line.split()
                try:
                    lexicon[' '.join(li[0:-1])]= float(li[-1])
                except:
                    print "type error, not number",line
    return lexicon

    
oov= set()  ## record the oov
def calPHRASEstrength(sentiDICT,nonLINEAR,phrase,advDICT):
    if not phrase:
        return 0
    li = phrase.split()
    if len(li) ==1:
        strength= sentiDICT.get(li[0])
        if strength is None:
            oov.add(li[0]);strength = 0
    elif nonLINEAR.get(' '.join(li)):
        strength = nonLINEAR.get(' '.join(li))
    elif len(li)==2:
        strength = sentiDICT.get(li[1])
        if strength is None:
            oov.add(li[1])
            strength = 0
        if li[0] == 'shift' and strength:
            strength = strength - 4 if strength>0 else strength + 4
        elif li[0]=="不太" and strength:
            strength = strength - 5 if strength>0 else strength + 5
        elif advDICT.get(li[0]):
            strength*= advDICT.get(li[0])
        

    elif len(li)==3:  
        strength= sentiDICT.get(li[2])
        if strength is None:
            oov.add(li[2])
            strength = 0
        if advDICT.get(li[1]):
            strength*=advDICT.get(li[1])
        ## DO SHIFT(4)
        if li[0] in ['shift','没','没有']:
            if strength>0:
                strength-=4
            elif strength<0:
                strength+=4
        else:
            if advDICT.get(li[0]):
                strength*= advDICT.get(li[0])
    
    else:
        length = len(li)
        strength= sentiDICT.get(li[length-1])
        if strength is None:
            oov.add(li[length-1])
            strength = 0
        for i in range(length-2,-1,-1):
            if advDICT.get(li[i]):
                strength*=advDICT.get(li[i])
##    if strength < 0:
##        strength = strength*1.3       
## if droppoint,comment two lines above
    return strength


def readFILEasDICT(path):
    dict={}
    fo = open(path)
    for line in fo:
        line=line.strip()
        if line:
            li=line.split()
            if len(li)==2:
                try:
                    dict[li[0]]=float(li[1])
                except:
                    print "type error, not number"
    print "the length of dictionary builded from file is %s" %(len(dict))
    return dict

## apply final phrases to calculate number sequences
def calALL(sentiDICT,nonLINEAR,advDICTfilePATH,finalPHs):
    advDICT = readFILEasDICT(advDICTfilePATH)
    list=[]
    if not finalPHs:    # phrase is empty
	return str(0.0)
    for line in finalPHs:
            if line =='SUM':
                list.append('s')
	    else:
                list.append(str(calPHRASEstrength(sentiDICT,nonLINEAR,line,advDICT)))
    return ("|".join(list))
           
## The combinated method to classify the polarity
def statistics(phraseNUMBERseqs):
    strength1 = findSENTIdroppoint(phraseNUMBERseqs)
    strength2 = commonSENTI(phraseNUMBERseqs)
    if strength1 * strength2 > 0:
        strength = strength2
    elif strength1 == 0:
        strength = strength2
    elif strength2 == 0:
        strength = strength1
    else:
        if strength1 >0 and strength2 < 0:
            strength = strength1
        else:
            strength = strength2
    return strength




## the example to process a text by the sentiment analysis proposed
class senti():
    def __init__(self):
        self.sentiDICT = loadSENTI(os.path.join(pwd,'data','sentiment2.txt'))
        self.nonLINEAR  = loadLEXICON(os.path.join(pwd,'data','nonlinear.txt'))
        self.nlp = StanfordNLP()
        ## load the lexicons
	self.dict = sentiment()
        self.nnSET = file2set(os.path.join(pwd,'data','sentiNN.txt'))
        self.vvSET=file2set(os.path.join(pwd,'data','sentiVV.txt'))
        self.adSET = file2set(os.path.join(pwd,'data','sentiAD.txt'))
        self.sumLIST = file2list(os.path.join(pwd,'data','summary.txt'))
        self.aspect = loadASPECTsenti(os.path.join(pwd,'data','aspectDICT.txt'))
        self.am = file2list(os.path.join(pwd,'data','ambiguity.txt'))
    def sentiFLY(self,line):
        li = []
        ## nature language processing
        seged,posed,parsed = parser1(self.nlp,line)
        ## opinion phrases and compute the sentiment strength
        seqs = []
        fph =  [] ## final phrases
        for pos,parse in zip(posed,parsed):
            phrases = findPHRASE(self.dict,self.nnSET,self.vvSET,self.adSET,self.sumLIST,
                                 self.aspect,self.am, pos,parse)
            finalPH = filterPHRASE(phrases)
            fph.append(" ,".join(finalPH))
            phraseNUMBERseqs = calALL(self.sentiDICT,self.nonLINEAR,os.path.join(pwd,'data','advxxx.txt'),finalPH)
            #print "phraseNUMBERseqs: ", phraseNUMBERseqs
            seqs.append(phraseNUMBERseqs)
        senti = statistics("|".join(seqs))
        seged = ' '.join(seged)
        posed = ' '.join(posed)
        parsed= ' '.join(parsed)
        li.extend([seged,posed,parsed,' ,'.join(fph),'|'.join(seqs),senti])
        return li


## backup one
def sentiFLY1(line):
    print 'current directory is ',os.getcwd()
    loadSENTI('./sentiment2.txt')
    ## nlp
    print "segment begins:"
    seged = seg(line)
    print "pos tagger begins:"
    posed = pos(seged)
    print "parser begins:"
    parsed = parser(seged)
    print "parser is over."

    print "seged",seged
    print "parsed",parsed

    ## find phrases and compute the sentiment polarity
    phrases = findPHRASE(posed,parsed)
    print ' '.join(phrases)
    finalPH = filterPHRASE(phrases)
    nonLINEAR  = loadLEXICON('./nonlinear.txt')
    phraseNUMBERseqs = calALL(nonLINEAR,'./advxxx.txt',finalPH)
    return statistics(phraseNUMBERseqs)

def dict2review(doc):
    try:
        time = doc['e_time']
        vip  = doc['u_grade']
        votes = doc['useful_counts']
        text = doc['opnion']
        length = len(text)

    except:
        time,vip,votes,length,text=None,None,None,None,None
    return time,vip,votes,length,text


''' mongo block'''

## connect to a mongo database
def dbCON(ip,port,dbname):
    ## connect to db
    client = pymongo.MongoClient(ip,port)
    db = client[dbname]
    return db

def starsSTAT(db,collection,productID):
    coll = db[collection]
    #qresult = coll.find({"pid":productID})
    #s5 = qresult.where('this.rating == 5').count()
    s5 = coll.find({"pid":productID,"rating":5}).count()
    s4 = coll.find({"pid":productID,"rating":4}).count()
    s3 = coll.find({"pid":productID,"rating":3}).count()
    s2 = coll.find({"pid":productID,"rating":2}).count()
    s1 = coll.find({"pid":productID,"rating":1}).count()
    return [s5,s4,s3,s2,s1]

def oneS(document):
    grades = {"注册会员":1,"铁牌会员":2,"铜牌会员":3,"银牌会员":4,"金牌会员":5,"钻石会员":6,"双钻石会员":7,"企业客户":8}
    timeSTR,vip,votes,length,text = dict2review(document)
    vip = vip.encode('utf8')
    vip = grades[vip]
    print "votes",votes
    print length
    print text
    text = text.encode("utf8")
    
    seged = seg(text)
    posed = pos(seged)
    npOP,fCNT = opinionSEARCH3(posed)
    
    ## time
    now = datetime.now()
    stime = time.strptime(timeSTR, "%Y-%m-%d %H:%M")
    dt = datetime.fromtimestamp(mktime(stime))
    timeduration = str(now - dt)
    days =  timeduration.split()[0]
    
    
    sentiment = sentiFLY(text)
    ## digitalized indicators
    print vip,votes,days,length,fCNT,sentiment
    return vip,votes,days,length,fCNT,sentiment

def fetchFstat():
    db = dbCON('192.168.0.155',27017,'jd')
    print db
    coll = db['mobile_evaluation']
    qresult = coll.find({"pid": "1022456996"})
    #starsSTAT(db,'mobile_evaluation',"1022456996")
    
    ##feature dictionary to store the feature statistic result
    fdict = {}
    for i in qresult:
        text = i['opnion'].encode("utf8")
        seged = seg(text)
        try:
            posed = pos(seged)
        except:
            print "oopsss"
        npop = opinionSEARCH3(posed)[0]  
        if npop:
            for j in npop:
                countSTREAM(j,fdict)
    showCOUNT(fdict)
    return fdict

from stars import senti2stars

def rating():
    db = dbCON('192.168.0.155',27017,'jd')
    print db
    coll = db['mobile_evaluation']
    qresult = coll.find({"pid": "1022456996"})
    #starsSTAT(db,'mobile_evaluation',"1022456996")
    
    ##feature dictionary to store the feature statistic result
    fdict = {1:0,2:0,3:0,4:0,5:0}
    for i in qresult:
        text = i['opnion'].encode("utf8")
        score = sentiFLY(text)
        grade = senti2stars(score)
        fdict[grade]+=1
    print fdict
    return fdict


def test():
    print "welcome to sentiment python world."        
if __name__=="__main__":
    '''db = dbCON('192.168.0.155',27017,'jd')
    print db
    coll = db['mobile_evaluation']
    qresult = coll.find({"pid": "1022456996"})
    starsSTAT(db,'mobile_evaluation',"1022456996")
    rating()'''
    ss = senti()
    print "the sentiment strength is :",ss.sentiFLY("新年快乐")
            
    
    
                         
