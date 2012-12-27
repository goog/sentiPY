# -*- coding:utf-8 -*-
import re
'''tools'''

def checkoutPHRASE(path):
    ## path to the final phrase
    emptyLIST=[]
    fo =open(path)
    flag=0
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------":
                lineNO+=1
                if flag==1:
                    emptyLIST.append(lineNO)
                flag=1
            else:
                flag=0
    print "the length of empty phrase reviews is:",len(emptyLIST)
    return emptyLIST


def reviewNOphrase():
    list  = checkoutPHRASE('phrase2.txt')  #to analyze the final phrase
    #print list
    fo = open('./neg_tagged.txt')
    fw = open('reviewNOphrase.txt','w')
    buf = ""
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------#NR":
                lineNO+=1
                if lineNO in list:
                    fw.write(buf+'\n')
                buf=''
            else:
                buf+=line
    fw.close()

def findLABELS(path):
    fo = open(path)  # "./pos_phrase.txt"
    a= set()
    for line in fo:
        line = line.strip()
        index = line.find('#')
        if index!=-1:
            a.add(line[index+1:])
    print a            


def doOOV():
    fo1 = open('./oov.txt')
    fo2 = open('./oov1.txt')
    a =set()
    b= set()
    for line in fo1:
        line=line.strip()
        if line:
            a.add(line.split()[0])

    #print len(a)


    for line in fo2:
        line=line.strip()
        if line:
            b.add(line)

    print  len(b-a)        
    for i in (b -a):
        print i

def processADVSS(path):
    ## ./advss.txt
    dict = {}
    fo=open(path)
    fw=open('./finalADVSS.txt','w')
    for line in fo:
        line=line.strip()
        if line:
            li=line.split()
            if li[0] in ['也','都','就','却','还是']:
                #remove non-intensitive 
                fw.write(' '.join(li[1:])+'\n')
            else:
                fw.write(line+'\n')
            if dict.get(li[0]):
                dict[li[0]]+=1
            else:
                dict[li[0]]=1
##    for i in dict.keys():
##        print i,dict[i]
        
    fw.close()


def processADVS(line):
    ## 不 太 好
    li=line.split()
    if len(li)==3:
        if ''.join(li[:2])=='不太':
            return '不太 '+li[2]+'\n'  ## minus -5
    return line+'\n'


palAD= re.compile(ur'[\u4e00-\u9fa5]+#AD.*')
palVE= re.compile(ur'[\u4e00-\u9fa5]+#VE.*')
def findADorVE(phrase):
    li = phrase.split('#PU')
    if len(li)==2:
        phrase = li[1]
    m = palAD.search(phrase.decode('utf8'))
    m2=palVE.search(phrase.decode('utf8'))
    if m:
        phrase = m.group().encode('utf8')
    elif m2:
        phrase = m2.group().encode('utf8')
    return phrase+'\n'
        
    
    
    

if __name__ == '__main__':
    processADVSS('./advss.txt')
    print findADorVE('几乎#AD没有#VE什么#DT合口味#NN')
    ##几乎#AD没有#VE什么#DT合口味#NN
    
            
            
            

