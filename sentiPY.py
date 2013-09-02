import numpy as np
import pymongo
from eigenvector import ev
import subprocess
from plumbum.cmd import cat
from plumbum import local
from datetime import datetime, timedelta
from time import mktime
import time
from NPfindOP import opinionSEARCH3



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

def dbFETCH():
    ## connect to db
    client = pymongo.MongoClient("192.168.0.155", 27017)
    db = client.jd
    document = db.mobile_evaluation.find_one()
    return document

def oneS(document):
    grades = {"注册会员":1,"铁牌会员":2,"铜牌会员":3,"银牌会员":4,"金牌会员":5,"钻石会员":6,"双钻石会员":7,"企业客户":8}
    timeSTR,vip,votes,length,text = dict2review(document)
    vip = vip.encode('utf8')
    vip = grades[vip]
    print "votes",votes
    print length
    print text
    text = text.encode("utf8")
    java = local["java"]
    seged = (cat << text |java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:",
                               "edu.stanford.nlp.ie.NERServer","-port","9191","-client"])()
    seged = seged.split('\n',1)[1].strip()
    
    ## time
    now = datetime.now()
    stime = time.strptime(timeSTR, "%Y-%m-%d %H:%M")
    dt = datetime.fromtimestamp(mktime(stime))
    timeduration = str(now - dt)
    days =  timeduration.split()[0]
    
    posed = (cat << seged |java["-mx700m","-cp","/home/drill/pos/stanford-postagger.jar:",
                               "edu.stanford.nlp.tagger.maxent.MaxentTaggerServer","-port","2020","-client"])()
    posed=posed.strip()
    posed = posed.encode('utf8')
    npOP,fCNT = opinionSEARCH3(posed)
    sentiment = 1
    ## vip need to digitalize
    print vip,votes,days,length,fCNT,sentiment
    return vip,votes,days,length,fCNT,sentiment
    
    

if __name__=="__main__":
    oneS(dbFETCH())            
            
    
    
                         
