import os
from plumbum.cmd import cat
from plumbum import local
import subprocess
############################
#       online NLP         #
############################

java = local["java"]
def seg(text):
    seged = (cat << text |java["-mx700m","-cp","/home/drill/segment/stanford-ner.jar:",
                               "edu.stanford.nlp.ie.NERServer","-port","9191","-client"])()
    seged = seged.split('\n',1)[1].strip()
    seged = seged.encode('utf8')
    return seged

def pos(seged):
    posed = (cat << seged |java["-mx700m","-cp","/home/drill/pos/stanford-postagger.jar:",
                               "edu.stanford.nlp.tagger.maxent.MaxentTaggerServer","-port","2020","-client"])()
    posed=posed.strip()
    posed = posed.encode('utf8')
    return posed


## this is a temporary solution
def parser(string):
    os.popen("echo "+string+" > ~/parser/stanfordtemp.txt")
    os.popen("~/parser/do.sh ~/parser/stanfordtemp.txt > ~/parser/output.txt")
    fo = open('/home/drill/parser/output.txt')
    li = []
    for line in fo:
        line = line.strip()
        if line:
            li.append(line)
    return "   ".join(li)


if __name__ =="__main__":
    string  = "我 是 中国 人"
    output = parser(string)
    print output
    print seg("我是中国人")
    print pos("我 是 中国 人")
    
