from preprocess import *
from evaluate import *

def readPHRASE(path):
    fo = open(path)
    fw=open('./maybeADV.txt','w')
    li=[]
    for line in fo:
        line=line.strip()
        if line:
            words=line.split()
            if len(words)==2:
                li.append(words[0])
    a =set(li)
    print "the maybe adv has %s" %len(a)
    for i in a:
        fw.write(i+'\n')
    fw.close()


def countPHRASE(path):
    len1=0
    len2=0
    len3=0
    lenx=0
    fo = open(path)
    for line in fo:
        line=line.strip()
        if line:
            num =len(line.split())
            if num==1:
                len1+=1
            elif num==2:
                len2+=1
            elif num==3:
                len3+=1
            else:
                lenx+=1
    print "the number of length 1 2 3 and more than three in a phrase is %s %s %s %s" %(len1,len2,len3,lenx)


def loadSENTI(path):
    fo = open(path)  #'./sentiment.txt'           
    global senti_dict
    for line in fo:
        line =line.strip()
        if line:
            li= line.split()
            if len(li)==2:
                try:
                    senti_dict[li[0]]= float(li[1])
                except:
                    print "type error, not number"
    print "the length of sentiment lexion is ",len(senti_dict)
    
oov=set()
def calPHRASEstrength(phrase,advDICT): 
    if not phrase:    ## it occurs
        return 0
    li = phrase.split()
    if len(li) ==1:
        value = senti_dict.get(li[0])
        if not value:
            oov.add(li[0])
        return  0 if value is None else value
    elif len(li)==2:
        sentiSTR= senti_dict.get(li[1])
        if sentiSTR is None:
            oov.add(li[1])
            sentiSTR = 0
        if advDICT.get(li[0]):
            ### try to shift
            strength= advDICT.get(li[0])*sentiSTR
        else:
            strength = sentiSTR
        return strength
    else:  ###  len 3  
        strength= senti_dict.get(li[2])
        if strength is None:
            oov.add(li[2])
            strength = 0
        if advDICT.get(li[1]):
            strength*=advDICT.get(li[1])
        ## DO SHIFT
        if li[0] in ['shift','没','没有']:
            if strength>0:
                strength-=4
            else:
                strength+=4
        else:
            if advDICT.get(li[0]):
                strength*= advDICT.get(li[0])
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


def calALL(advDICTfilePATH,inputPATH,outputPATH):
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
                list.append(str(calPHRASEstrength(line,advDICT)))
        else:
            #if list:  ### a lot lines is empty 
            fw.write("|".join(list)+"\n")
            list=[]  
    fw.close()


def statistics(phraseNUMBERseqs):
    #'./phraseINline2.txt'
    errorLIST = []
    dict ={1:0,0:0,-1:0}
    with open(phraseNUMBERseqs) as myFILE:
        for num, line in enumerate(myFILE, 1):
            line=line.strip()
            strength = findSENTIdroppoint(line)
            if strength > 0:
                errorLIST.append(num)
            dict[calORIENTATION(strength)]+=1
    print errorLIST
    print dict
    print "the correct percentage is %s" %(dict[-1]/2000.0)


taggedFIILE='./pos_tagged.txt'
phraseFILE='./pos_phrase.txt'
finalPHRASE='./phrase.txt'
phraseNUMBERseqs='./phraseINline.txt'

#### precess block
#preprocess("preprocess-neg.txt")
#segANDpos("preprocess-neg.txt")


## load sentiment strength 
senti_dict = {}
loadSENTI('./sentiment.txt')
#loadSENTI('./senti.txt')


findPHRASE(taggedFIILE,phraseFILE)
filterPHRASE(phraseFILE,finalPHRASE)
calALL('advxxx.txt',finalPHRASE,phraseNUMBERseqs)
statistics(phraseNUMBERseqs)


#for i in oov:
#    print i
print "the length of OOV:",len(oov)





            
    
            




                
                
