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
from nlp import seg,pos
from themain import sentiFLY
from featurePIPE import countSTREAM,showCOUNT



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


''' along with mongo block'''

## connect to a mongo database
def dbCON(ip,port,dbname):
    ## connect to db
    client = pymongo.MongoClient(ip,port)
    db = client[dbname]
    return db

def starsSTAT(db,collection,productID):
    coll = db[collection]
    qresult = coll.find({"pid":productID})
    print "the total number is:",qresult.count()
    print "the number of five stars:",qresult.where('this.rating == 5').count()
    s5 = qresult.where('this.rating == 5').count()
    print "the number of four stars:",qresult.where('this.rating == 4').count()
    s4 = qresult.where('this.rating == 4').count()
    print "the number of three stars:",qresult.where('this.rating == 3').count()
    s3 = qresult.where('this.rating == 3').count()
    print "the number of two stars:",qresult.where('this.rating == 2').count()
    s2 = qresult.where('this.rating == 2').count()
    print "the number of one stars:",qresult.where('this.rating == 1').count()
    s1 = qresult.where('this.rating == 1').count()
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
    posed = pos(text)
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
    
    

if __name__=="__main__":
    db = dbCON('192.168.0.155',27017,'jd')
    print db
    coll = db['mobile_evaluation']
    qresult = coll.find({"pid": "1022456996"})
    starsSTAT(db,'mobile_evaluation',"1022456996")
    
    ##feature dictionary to store the feature statistic result
    fdict = {}
    cnt = 0
    for i in qresult:
        text = i['opnion'].encode("utf8")
        if cnt == 1089:
            print text
        seged = seg(text)
        posed = pos(text)
        npop = opinionSEARCH3(posed)[0]  
        if npop:
            for j in npop:
                countSTREAM(j,fdict)
        cnt +=1
        print "current time:",cnt
    showCOUNT(fdict)
            
    
               
            
    
    
                         
