# -*- coding:utf-8 -*-
from preprocess import *
from evaluate import *
from check import *
import time
import yaml

def loadSENTI(path):
    fo = open(path)
    global sentiDICT
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
    print "Length of sentiment lexion in %s is %s " %(fo.name,len(lexicon))
    return lexicon

    
oov= set()
def calPHRASEstrength(nonLINEAR,phrase,advDICT):
    if not phrase:  ## didnt extract a phrase
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
    if strength < -5:
        strength = -5
    if strength > 5:
        strength =5
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

def calALL(nonLINEAR,advDICTfilePATH,inputPATH,outputPATH):
    fo = open(inputPATH)
    fw = open(outputPATH,'w')
    advDICT = readFILEasDICT(advDICTfilePATH)
    list=[]
    for line in fo:
        line=line.strip()
        if line!='----------':
            if line =='SUM':
                list.append('s')
            else:
                list.append(str(calPHRASEstrength(nonLINEAR,line,advDICT)))
        else: 
            fw.write("|".join(list)+"\n")
            list=[]
    fw.write("|".join(list)+"\n")    # handler the last line
    fw.close()

def statistics(movie,phraseNUMBERseqs):
    errorLIST = []
    cnt = 0
    lineno = 0
    with open(phraseNUMBERseqs) as myFILE, open(movie) as fo:
        for line, y in izip(myFILE,fo):
            lineno+=1
            label = ""
            line=line.strip()
            strength1 = findSENTIdroppoint(line)
            strength2 = commonSENTI(line)
            
            if strength1 * strength2 > 0:
                strength = strength2    ## ?
            elif strength1 == 0:
                strength = strength2
            elif strength2 == 0:
                strength = strength1
            else:
                
                if strength1 >0 and strength2 < 0:
                    strength = strength1
                else:
                    strength = strength2

            if strength > 4:
                label = "力荐"
            elif 2<strength and strength<=4:
                label = "推荐"
            elif 0<=strength and strength<=2:
                label = "还行"
            elif -3<=strength and strength<0:
                label = "较差"
            elif -5<=strength and strength<-3:
                label = "很差"
                
            if label == y.split("----------")[0]:
                cnt+=1
            else:
                errorLIST.append(lineno)
                
    print cnt
    print "the correct percentage is %s" %(cnt/800.0)
    return errorLIST

if __name__ == '__main__':
    print "starts",time.asctime()

    with open("rank.conf") as f:
        settings=yaml.load(f)
##    preprocess(settings['preFILE'])
##    segANDpos(settings['preFILE'])

    reformPARSED(settings['parseFILE'],settings['parsedFILE'])

    sentiDICT = {}
    loadSENTI('./sentiment2.txt')   # ./mySTRENGTH.txt
    findPHRASE(settings['taggedFILE'],settings['parsedFILE'],settings['phraseFILE'])
    filterPHRASE(settings['phraseFILE'],settings['finalPHRASE'])
    nonLINEAR  = loadLEXICON('./nonlinear.txt')
    calALL(nonLINEAR,'advxxx.txt',settings['finalPHRASE'],settings['phraseNUMBERseqs'])
    errorLIST  = statistics('./movie.txt',settings['phraseNUMBERseqs'])
    writeERROR('preprocess-pos.txt',errorLIST)
    recordOOV(oov)
    print 'finished',time.asctime()




                
                
