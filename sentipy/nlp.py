import os,sys
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

def parser(nlp,text):
    result = nlp.parse(text)
    #print "the parsed return:",result
    posed = []
    parsed = []
    try:
        for sen in result['sentences']:
            words = sen['words']
            poses  = map(lambda x:(x[0]+"#"+x[1].get("PartOfSpeech")).encode("utf8"),words)
            deps = sen['dependencies']
            deps = map(lambda x:x.encode('utf8'),deps)
            posed.append(" ".join(poses))
            parsed.append("   ".join(deps))

    except:
	print "there is an error in sentences ."
	posed = []
	parsed = []
    return posed,parsed


def parser1(nlp,text):
    result = nlp.parse(text)
    #print "the parsed return:",result
    seged = []
    posed = []
    parsed= []
    try:
        for sen in result['sentences']:
            segs = []
            words = sen['words']
	    for i in words:
		print "seged word type:",type(i[0])
		segs.append(i[0].encode('utf8'))
            
            poses= map(lambda x:(x[0]+"#"+x[1].get("PartOfSpeech")).encode("utf8"),words)
	    deps = sen['dependencies']
            deps = map(lambda x:x.encode('utf8'),deps)
            seged.append(" ".join(segs))
	    posed.append(" ".join(poses))
            parsed.append("   ".join(deps))
	    
    except:
        print "there is an error in sentences ."
	seged = []
        posed = []
        parsed = []
    return seged,posed,parsed

if __name__ =="__main__":
    string  = "总体还不错 ！厂商做的很用心（个人觉得老人机中的机皇），快递也给力 一天就到了。就是护套，建议以后要是有人一次买两个，包装的时候护套能不能包不一样的颜色啊！"
    nlp = StanfordNLP()
    print parser1(nlp,string) 
