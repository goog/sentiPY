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

def countPHRASE(path):
    len1=0;len2=0;len3=0;lenx=0
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

def findLABELS(path):
    fo = open(path)  # "./pos_phrase.txt"
    a= set()
    for line in fo:
        line = line.strip()
        index = line.find('#')
        if index!=-1:
            a.add(line[index+1:])
    print a

def file2count(path):
    ## read a file ,output  k,v
    fo =open(path)
    dict = {}
    for line in fo:
        line = line.strip()
        if line:
            if dict.get(line):
                dict[line]+=1
            else:
                dict[line]=1
    for i in dict.keys():
        print i,dict[i]
    
def checkLABELED(path1,path2):
    dict1={}
    dict2={}
    fo1 = open(path1)  #'./1.txt'
    fo2 = open(path2)  #'./2.txt'
    fw=open('./senti.txt','a')
    for line in fo1:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                except:
                    print kv[0]
                dict1[kv[0]]=kv[1]
    print "dict1 length is %s" %len(dict1)


    for line in fo2:
        line=line.strip()
        if line:
            kv=line.split()
            if len(kv)==2:
                try:
                    test = float(kv[1])
                except:
                    print kv[0]
                    
                dict2[kv[0]]=kv[1]
    print "dict2 length is %s" %len(dict2)

    a = set(dict1.keys())
    b = set(dict2.keys())
    c = a|b
    print "the total length is %s" %len(c)
    flag=0
    for i in c:
        if i=="自我":
            flag=1
        if flag:
        
            try:
                
                if dict1.get(i)==dict2.get(i):
                    fw.write(i+"   "+dict1.get(i)+"\n")
                else:
                    if dict1.get(i) and dict2.get(i):
                        if abs(int(dict1.get(i))-int(dict2.get(i)))<=1:
                            avg= (int(dict1.get(i))+int(dict2.get(i)))/2.0
                            fw.write(i+"   "+str(avg)+"\n")
                        else:
                            print i,"   ",dict1.get(i),"   ",dict2.get(i)
                            r=raw_input("type a value:")
                            fw.write(i+"   "+r+"\n")
                            
                            
                    else:
                        print i,"   ",dict1.get(i),"   ",dict2.get(i)
                        r=raw_input("type a value:")
                        fw.write(i+"   "+r+"\n")
            except:
                print i
    fw.close()


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

def recordOOV(oov):
    fw = open('oov.txt','w')
    for i in oov:
        fw.write(i+'   \n')
    fw.close()
    print "the length of OOV is %s" %(len(oov))


def processADVS(line):
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
            
            
            

