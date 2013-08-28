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
    timeSTR,vip,votes,length,text = dict2review(document)
    print "votes",votes
    print length
    print text
    text = text.encode("utf8")
    java = local["java"]
    seged = (cat << text |java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:",
                               "edu.stanford.nlp.ie.NERServer","-port","9191","-client"])()
    seged = seged.split('\n',1)[1].strip()
    print seged
    ## time:
    now = datetime.now()
    stime = time.strptime(timeSTR, "%Y-%m-%d %H:%M")
    dt = datetime.fromtimestamp(mktime(stime))
    print now - dt,type(now - dt)
    timeduration = str(now - dt)
    days =  timeduration.split()[0]
    parsed = (cat << seged |java["-mx700m","-cp","/home/drill/pos/stanford-postagger.jar:",
                               "edu.stanford.nlp.tagger.maxent.MaxentTaggerServer","-port","2020","-client"])()
    parsed=parsed.strip()
    parsed = parsed.encode('utf8')
    npOP,fCNT = opinionSEARCH3(parsed)
    print fCNT
    sentiment = 1
    ## vip need to digitalize
    print vip,votes,days,length,fCNT,sentiment
    return vip,votes,days,length,fCNT,sentiment
    
    

if __name__=="__main__":
    oneS(dbFETCH())            
            
    
    
                         
