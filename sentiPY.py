import re
import numpy as np
import pymongo
from eigenvector import ev
import subprocess
from plumbum.cmd import grep, cat
from plumbum import local



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



def main():
##    ## connect to db
##    client = pymongo.MongoClient("192.168.0.155", 27017)
##    db = client.jd
##    document = db.mobile_evaluation.find_one()
##    time,vip,votes,length,text = dict2review(document)
##    print "time",time
##    print length
##    print text
    text = "我们都是中国人"
    java = local["java"]
    seged = (cat << text |java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:","edu.stanford.nlp.ie.NERServer","-port","9191","-client"])()
    print seged
    

if __name__=="__main__":
    main()
        
    
            
            
            
    
    
                         
