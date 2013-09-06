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
    #seged = (cat << text |java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:",
    #                           "edu.stanford.nlp.ie.NERServer","-port","9191","-client"])()
    seged = (java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:", 
            "edu.stanford.nlp.ie.NERServer", "-port","9191","-client"] << text)()
    seged = seged.split('\n',1)[1].strip()
    seged = seged.encode('utf8')
    return seged

def pos(seged):
    posed = (cat << seged |java["-mx700m","-cp","/home/drill/pos/stanford-postagger.jar:",
                               "edu.stanford.nlp.tagger.maxent.MaxentTaggerServer","-port","2020","-client"])()
    posed=posed.strip()
    posed = posed.encode('utf8')
    return posed

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def parser(string):
    nlp = StanfordNLP()
    result = nlp.parse(string)
    deps = result['sentences'][0]['dependencies']
    deps = map(lambda x:x.encode('utf8'),deps)
    return "   ".join(deps)


if __name__ =="__main__":
    print seg("我是中国人")
##    string  = "我 是 中国 人"
##    print parser(string)
    
