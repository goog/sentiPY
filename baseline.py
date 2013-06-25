# -*- coding:utf-8 -*-
from preprocess import *
from evaluate import *
from check import *
import time,yaml

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
    ### return none if oov
    if not phrase:
        return 0    #################  smth ????  should return none
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
    fw.close()

def statistics(phraseNUMBERseqs):
    errorLIST = []
    dict ={1:0,0:0,-1:0}
    with open(phraseNUMBERseqs) as myFILE:
        for num, line in enumerate(myFILE, 1):
            line=line.strip()
            strength1 = findSENTIdroppoint(line)
            #strength = commonSENTI(line)
            ''' mix two methods '''
            strength2 = commonSENTI(line)
            if strength1 * strength2 > 0:
                strength = strength2
            elif strength1 == 0:
                strength = strength2
            elif strength2 == 0:
                strength = strength1
            else:
                
                if strength1 >0 and strength2 < 0:   #######
                    strength = strength1
                elif strength1 < 0 and strength2 > 0:
                    strength = strength2
                else:
                    print "here"
                    strength = (strength1+strength2)/2
                #####strength = strength2
##            if strength > 0:
##                errorLIST.append(num)
            dict[calORIENTATION(strength)]+=1
    print dict
    print "my union method:"
    print "the correct percentage is %s" %(dict[1]/2000.0)
    return errorLIST


def statistics2(phraseNUMBERseqs):
    dict ={1:0,0:0,-1:0}
    with open(phraseNUMBERseqs) as myFILE:
        for num, line in enumerate(myFILE, 1):
            line=line.strip()
            eles = line.split('|')
            sum  = 0
            for i in eles:
                try:
                    value = float(i)
                except:
                    pass
                if value > 0:
                    sum+=1
                elif value < 0:
                    sum-=1
                          
            dict[calORIENTATION(sum)]+=1
    print '''  *****count stat:'''
    print dict
    print "the correct percentage is %s" %(dict[1]/2000.0)
    

if __name__ == '__main__':
    print "starts",time.asctime()
    
    with open("neg_weibo.conf") as f:
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
    errorLIST  = statistics(settings['phraseNUMBERseqs'])

    ###add new function to count the number of pos/neg
    statistics2(settings['phraseNUMBERseqs'])
    
    writeERROR('preprocess-neg.txt',errorLIST)
    recordOOV(oov)
    print 'finished',time.asctime()



            




                
                
