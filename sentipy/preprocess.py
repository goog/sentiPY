# -*- coding:utf-8 -*-
import os,sys,re
import opencc
import subprocess
from check import *
from itertools import izip
pwd = os.path.dirname(os.path.realpath(__file__))

par = re.compile(ur'\(.+?\)')
par2 = re.compile(ur'\uff08.+?\uff09')
quote = re.compile(ur'".+?"')
quote2 = re.compile(ur'\u201c.+?\u201d')
period = re.compile(ur'\u3002{2,}')
han = re.compile(ur'[\u4e00-\u9fa5]+')
tag = re.compile('#\w{1,3}')
rmword = re.compile('\w{1,3}')

def extractADV(path):
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

def file2set(path):
    newSET = set()
    fo = open(path)
    for line in fo:
        line = line.strip()
        if line:
            newSET.add(line)
    return newSET

def file2list(path):
    li = []
    with open(path) as fo:
        for line in fo:
            line = line.strip()
            if line:
                li.append(line)
    return li

def preprocess(path):
    r=raw_input("type a directory name:")
    fw = open(path,'w')
    ivLIST = file2list('./iv.txt')
    for root,dirs,files in os.walk(r):
        for f in files:
            path = os.path.join(root,f)
            fo = open(path)
            for line in fo:
                line=line.strip()
                cc = opencc.OpenCC('t2s',opencc_path='/usr/bin/opencc')
                line  = cc.convert(line.decode('utf8')).encode('utf8')
                if line:
                    #remove the content in () 
                    match = par.findall(line)
                    if match:
                        for i in match:
                            if i=='(*^__^*)' or i=='(∩_∩)':
                                line = line.replace(i,' 微笑 ')
                            else:
                                line = line.replace(i,' ')

                    line = applyPAT(quote,line,isCH=None,sub=' ')
                    line = applyPAT(par2,line,1)
                    line = applyPAT(quote2,line,1)
                    line = applyPAT(period,line,1,' 无语 ')
                    
                    ## remove intensional verb and something unsure
                    lineCOPY = line    
                    lineCOPY = lineCOPY.replace('。','\n').replace(',','\n').replace('，','\n')
                    clauses = lineCOPY.split('\n') 
                    for i in clauses:
                        for j in ivLIST:
                            if i.find(j) !=-1:
                                line = line.replace(i,' ')
                    if line:
                        if line.startswith('宾馆反馈'):
                            continue
                        fw.write(line+'\n')            
            fw.write("----------\n")
        fw.close()

def sentiment():
    dict_list=[]
    exclude = file2set(os.path.join(pwd,'data','stopword.txt'))      
    fo1 = open(os.path.join(pwd,'data','neg.txt'))
    fo2 = open(os.path.join(pwd,'data','pos.txt'))
    for line in fo1:
        line=line.strip()
        if line:
            dict_list.append(line)

    for line in fo2:
        line=line.strip()
        if line:
            dict_list.append(line)
    #print "prior length:",len(dict_list)
    for i in exclude:
        try:
            dict_list.remove(i)
        except:
            pass
    return dict.fromkeys(dict_list,1)

def getLABEL(element):
    return element[element.find('#')+1:]

def getWORD(element):
    return element[:element.find('#')]

def searchLIST(li,ty,string):
    for i in li:
        if i.startswith(ty) and i.find(string)!= -1:
            return i

def doNO(ylist,string,i,phraseLIST,dict):
    key = string.split('#')[0]
    ele = searchLIST(ylist,'dobj',key+"-"+str(i+1))
    if ele is None:
        ele = searchLIST(ylist,'nsubj',key+"-"+str(i+1))
    if ele:
        m = han.findall(ele.decode('utf8'))
        if m:
            pair = [h.encode('utf8') for h in m]
            if len(pair)==2:
                pair.remove(key)
                if not dict.get(pair[0]):
                    phraseLIST.append('没有');lb=i
                else:
                    ## dobj all right; nsubj ? 
                    return ele.split(',')[1][:-1]

'''
    params:
        line: posed  string
        y   : parsed string

'''

def findPHRASE(dict, nnSET, vvSET, adSET, sumLIST, aspect, am, line, y): 
    phraseLIST = []
    phraseLIST2 = []
    farSENTI = [] ##do queue
    farSENTI2 = []   ## for not
    line = line.strip()
    y = y.strip()
    if line:
        list = line.split()
        ylist = y.split('   ')
        lb = 0    #lowerbound, record the wrote position
        for i in range(len(list)):
            seger = getWORD(list[i]);label = getLABEL(list[i])
            if seger in sumLIST:
                phraseLIST.append('SUM');lb=i
                
            elif list[i]=='没有#VE' or list[i]=='没#VE':
                ret = doNO(ylist,list[i],i,phraseLIST,dict)
                if ret:
                    farSENTI.append(ret)
                        
            elif dict.get(seger):
                if label=="VA":
                    if i>0:
                        p_label = getLABEL(list[i-1]) 
                        if p_label in ['DEV','DEG'] and i>1:
                            phraseLIST.append(''.join(list[i-2:i+1]));lb=i
                        elif p_label=='AD':
                            ind = i-1
                            try:
                                for j in range(i-2,-1,-1):
                                    if getLABEL(list[j])=='AD':
                                        ind=j
                                    else:
                                        break
                            except:
                                print "out of range."
                            if ind==i-1 and i>2:
                                if getLABEL(list[i-2])=='VC' and getLABEL(list[i-3])=='AD':
                                    phraseLIST.append(''.join(list[i-3:i+1]));lb=i
                                else:
                                    phraseLIST.append(''.join(list[i-1:i+1]));lb=i       

                            else:
                                if ind<=lb:
                                    ind=lb+1 ## avoid repeated extraction
                                phraseLIST.append(''.join(list[ind:i+1]));lb=i  
                        else:
                            phraseLIST.append(list[i]+'-'+str(i+1));lb=i
                    else:
                        phraseLIST.append(list[0]+'-1');lb=i
                
                if label=="NN":
                    if seger in nnSET:  ## skip the zero strength noun
                        continue
                    if i>0:
                        p_label = getLABEL(list[i-1])
                        if p_label in ['AD','JJ','VE','CD']:
                            # VE: 有/没有;CD:一点点
                            if lb != i-1:  ## most use of lb
                                phraseLIST.append(''.join(list[i-1:i+1]));lb=i
                        elif p_label=='DT' and i>1:
                            phraseLIST.append(findADorVE(''.join(list[i-2:i+1])));lb=i
                        else:
                            phraseLIST.append(list[i]+'-'+str(i+1));lb=i
                    else:
                        phraseLIST.append(list[0]+'-1');lb=i
                        
                if label=="VV":
                    if seger in vvSET:
                        continue
                    if i>0:
                        p_label = getLABEL(list[i-1])
                        if p_label in ['AD','PN']:
                            phraseLIST.append(''.join(list[i-1:i+1]));lb=i
                        else:
                            phraseLIST.append(list[i]+'-'+str(i+1));lb=i
                    else:
                        phraseLIST.append(list[0]+'-1');lb=i
                                       
                if label=='AD':
                    if seger in adSET:
                        continue
                    if i>0:
                        p_label = getLABEL(list[i-1])
                        if p_label=='AD':
                            ind = i-1
                            try:
                                for j in range(i-2,-1,-1):
                                    if getLABEL(list[j])=='AD':
                                        ind=j
                                    else:
                                        break
                            except:
                                pass
                            ''' some fragments '''
                            if seger=='重' and getWORD(list[i-1]) in['再','往复']:
                                continue
                            else:
                                if ind<=lb:
                                    ind=lb+1
                                phraseLIST.append(''.join(list[ind:i+1]));lb=i
                        else:
                            phraseLIST.append(list[i]+'-'+str(i+1));lb=i
                    else:
                        phraseLIST.append(list[i]+'-'+str(i+1));lb=i        
                #interjection        
                if label=="IJ":
                    phraseLIST.append(list[i]);lb=i
                if label=="JJ":
                    if seger in am:  ## handler  ambiguity
                        jjj = searchLIST(ylist,'amod',seger+"-"+str(i+1))
                        if jjj:
                            m = han.findall(jjj.decode('utf8'))
                            if m:
                                pair = [h.encode('utf8') for h in m]
                                if len(pair)==2 and (not dict.get(pair[0])):
                                    if aspect.get(' '.join(pair)):
                                        phraseLIST.append(aspect.get(' '.join(pair)));lb=i
                                    else:
                                        ### default
                                        phraseLIST.append(list[i])
                    else:
                        phraseLIST.append(list[i]);lb=i
                        
                    
                if label=="CD":
                    phraseLIST.append(list[i]);lb=i
            else:
                if label=='VV':
                    ### to do .......
                    try:
                        if ''.join(list[i-3:i])=='不#AD会#VV再#AD':
                            phraseLIST.append('-4');lb=i  ### add a const
                    except:
                        pass
                if seger=='不':
                    ele  = searchLIST(ylist,'neg',"不-"+str(i+1))
                    if ele:
                        ele2 = ele.split(',')[0][4:]
                        farSENTI2.append(ele2)
                  
        for p in phraseLIST:
            if tag.sub('',p) in farSENTI:
                phraseLIST2.append('shift   '+p.split('-')[0])
            elif tag.sub('',p) in farSENTI2:
                phraseLIST2.append('shift   '+p.split('-')[0])
            else:
                if p.startswith('-'):
                    phraseLIST2.append(p)
                else:
                    phraseLIST2.append(p.split('-')[0])
    return phraseLIST2
    

def findPHRASE1(taggedFILE,phraseFILE):
    dict = sentiment()
    #advSET = file2set('./sentiADV.txt') ##read sentiment words which act as advs
    with open(taggedFILE) as fo1,open(phraseFILE,'w') as fw: 
        for line in fo1:
            phraseLIST = [];
            line = line.strip()

            if line:  ##  a line from taggedFILE
                #if line =='----------#NN':  ## NN
                #if line =='--#PU --#PU --#PU --#PU --#PU':   ## for ctb segment
                if line =='--#NN --#NN --#NN --#NN --#NN':
                    fw.write('----------\n')
                    continue
                list = line.split()
                
                  #lowerbound, record the wrote position
                for i in range(len(list)):
                    seger = getWORD(list[i]);
                    
                    if dict.get(seger):
                        fw.write(list[i]+'\n')
    fw.close()

def filterPHRASE(phraseLIST):
    dict = sentiment()
    finalPH = []
    for line in phraseLIST:
        if line == 'SUM':
            finalPH.append('SUM')
        elif line.startswith('+') or line.startswith('-'):  ## for const sentiment
            finalPH.append(line)
        else:
            li= line.split('#')
            if len(li)==1:
                finalPH.append(li[0]) 
            elif len(li) ==2:
                finalPH.append(li[0])
            elif len(li) == 3:
                if li[2]=='VA' and (li[1].startswith('NN') or li[1].startswith('VV')) and (not dict.get(li[0])):
                    finalPH.append(li[1][2:])
                elif li[1].startswith('PU'):
                    finalPH.append(li[1][2:])
                else:
                    finalPH.append(tag.sub('   ',line))  
            elif len(li) == 4:
                if li[1].startswith('VE'):   ## VE:有/没有
                    if li[0] in ['没','没有']:
                        li.pop(1)
                        finalPH.append(rmword.sub('','   '.join(li)))
                        #print line,rmword.sub('','   '.join(li))
                    else:
                        pass  ## skip it
                elif li[1].startswith('AD'):
                    if li[2].startswith('DEV') :
                        finalPH.append(li[0]+'   '+li[2][3:])
                        #print line,li[0]+'   '+rmword.sub('',li[2])
                    else:
                        if li[0] in ['都','就','却','还是']:
                            finalPH.append(rmword.sub('','   '.join(li[1:3])))
                        else:
                            finalPH.append(processADVS(rmword.sub('','   '.join(li))))
                else:
                    if li[2].startswith('DT'):
                        finalPH.append(rmword.sub('','   '.join(li[1:3])))
                        #print line,rmword.sub('','   '.join(li[1:3]))          
                    else:
                        finalPH.append(rmword.sub('',li[2]))
                        #print line,rmword.sub('',li[2])
            else:
                if len(li)==5:
                    if li[2].startswith('VC'):
                        if li[0]=="不":
                            finalPH.append("shift   "+rmword.sub('','   '.join(li[2:])))
                            #print line,"shift   "+rmword.sub('','   '.join(li[2:]))
                        else:
                            finalPH.append(rmword.sub('','   '.join([li[0]]+li[2:4])))
                    else:
                        finalPH.append(rmword.sub('','   '.join(li)))
                        #print line,rmword.sub('','   '.join(li))
                else:
                    finalPH.append(rmword.sub('','   '.join(li)))
    return finalPH

if __name__ == '__main__':
    preprocess("preprocess-neg.txt")
##    extractADV('phrase2.txt')
    #findPHRASE('neg_tagged.txt','neg_parsed_format.txt','neg_phrase.txt')





                
                
