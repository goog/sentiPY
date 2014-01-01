import os
from plumbum.cmd import cat
from plumbum import local
import subprocess
import json
import jsonrpclib
from pprint import pprint
############################
#       online NLP         #
############################

java = local["java"]
def seg(text):
    seged = (java["-mx1g","-cp","/home/bigdata/segment/stanford-ner.jar:", 
            "edu.stanford.nlp.ie.NERServer", "-port","9191","-client"] << text)()
    seged = seged.split('\n',1)[1].strip()
    seged = seged.encode('utf8')
    return seged


class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def parser(string):
    nlp = StanfordNLP()
    result = nlp.parse(string)
    #print "the parsed return:",result
    words = result['sentences'][0]['words']
    print "the first sentence words:",words
    poses  = map(lambda x:(x[0]+"#"+x[1].get("PartOfSpeech")).encode("utf8"),words)
    print "poses:"," ".join(poses)
    deps = result['sentences'][0]['dependencies']
    deps = map(lambda x:x.encode('utf8'),deps)
    return " ".join(poses),"   ".join(deps)

if __name__ =="__main__":
    string  = "总体还不错 ！厂商做的很用心（个人觉得老人机中的机皇），快递也给力 一天就到了。就是护套，建议以后要是有人一次买两个，包装的时候护套能不能包不一样的颜色啊！"
#    print "segment:",seg(string)
    print parser(string)
    
