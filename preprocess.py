# -*- coding:utf-8 -*-
import os,sys,re
import subprocess
from check import *

pal = re.compile(ur'\(.+?\)')
pal2 = re.compile(ur'\uff08.+?\uff09')
quote = re.compile(ur'".+?"')
quote2 = re.compile(ur'\u201c.+?\u201d')
#suiran = re.compile(ur'\u867d\u7136.+?\u4f46.+?[,!\uff01\uff0c\u3002\uff1b]')

def rmBLANK(path,writeTO):
    fo = open(path)
    fw = open(writeTO,'w')
    for line in fo:
        line = line.strip()
        if line:
            fw.write(line+'\n')       
    fw.close()

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

def file2set(path):
    newSET = set()
    fo = open(path)
    for line in fo:
        line = line.strip()
        if line:
            newSET.add(line)
    return newSET

def preprocess(path):
    ## the method mainly to remove smth disrelated and interferential
    r=raw_input("type a directory name:")
    fw = open(path,'w')
    for root,dirs,files in os.walk(r):
        for f in files:
            path = os.path.join(root,f)
            fo = open(path)
            for line in fo:
                line=line.strip()
                if line:
                    #remove the content in () 
                    match = pal.findall(line)
                    if match:
                        for i in match:
                            if i=='(*^__^*)' or i=='(∩_∩)':
                                line = line.replace(i,'微笑 ')
                            else:
                                line = line.replace(i,' ')

                    match = quote.findall(line)
                    if match:
                        for i in match:
                            if i=='(*^__^*)' or i=='(∩_∩)':
                                line = line.replace(i,'微笑 ')
                            else:
                                line = line.replace(i,' ')
                            
                    m = pal2.findall(line.decode('utf8'))
                    if m:
                        for i in m:
                            line = line.replace(i.encode('utf8'),' ')

                    m = quote2.findall(line.decode('utf8')) ## remove chinese quotes
                    if m:
                        for i in m:
                            #print i
                            line = line.replace(i.encode('utf8'),' ')
                    ## remove intensional verb and something unsure
                    line_copy=line     
                    line_copy = line_copy.replace('。','\n').replace(',','\n').replace('，','\n')
                    clauses = line_copy.split('\n')
                    for i in clauses:
                        for j in ['怀疑','觉得','如果','假如']:
                            if i.find(j) !=-1:
                                line = line.replace(i,' ')
                    if line:
                        fw.write(line+'\n')            
            fw.write("----------\n")
        fw.close()
                    

def segANDpos(input):
    cmd="cp "+input+" ~/segmenter/"+input
    subprocess.call(cmd, shell=True)
    arg0=input[-7:-4]  
    subprocess.call("./segment.sh "+arg0, shell=True)
    print "segment finished."
    subprocess.call("./tagger.sh "+arg0, shell=True)
    print "pos tagger finished."
    
def parseLINE(line):
    p = re.compile( '#\w{1,3}')
    fw=open('/home/googcheng/parser/line.txt','w')
    fw.write(p.sub('',line))
    fw.close()
    subprocess.call("./parse.sh", shell=True)

def sentiment():
    dict_list=[]
    exclude = set()
    fop = open('exclude.txt')
    for line in fop:
        line= line.strip()
        if line:
            exclude.add(line)
            
    fo1 = open('./neg.txt')
    fo2 = open('./pos.txt')
    for line in fo1:
        line=line.strip()
        if line not in exclude:
            dict_list.append(line)

    for line in fo2:
        line=line.strip()
        if line not in exclude:
            dict_list.append(line)
    print "there is %s words in sentiment dictionary" % len({}.fromkeys(dict_list,1))
    return {}.fromkeys(dict_list,1)

def getLABEL(element):
    return element[element.find('#')+1:]

def getWORD(element):
    return element[:element.find('#')]

def doSMALLbig(seger,element):
    if seger=='小': 
        if getWORD(element) in ['单人床','县城','地方','柜门','液晶']:
            return '-小\n'
    elif seger=='大':
        if getWORD(element) in ['公司','单位','商场','城市','宾馆',
                                  '床','店','气','片','能力','酒店','钱','银行','阳台']:
            return '+大\n'
        elif getWORD(element) in ['声','理由','环境','当']:
            return '-大\n'

def findPHRASE(taggedFILE,phraseFILE):
    dict = sentiment()
    advSET = file2set('./sentiADV.txt') ##read sentiment words which act as advs
    nnSET = file2set('./sentiNN.txt')
    fo = open(taggedFILE)
    fw = open(phraseFILE,'w')
    for line in fo:
        line = line.strip()
        if line:
            #if line =='----------#NN':  ## NN
            #if line =='--#PU --#PU --#PU --#PU --#PU':   ## for ctb segment
            if line =='--#NN --#NN --#NN --#NN --#NN':
                fw.write('----------\n')
                continue
            list = line.split()
            lb = 0    #lowerbound, record the wrote position
            for i in range(len(list)):
                seger = getWORD(list[i]);label = getLABEL(list[i])
                if seger in ['整体','总之','总体','总而言之','总的来说','总结','整体性','总体性']:
                    fw.write('SUM\n');lb=i
                ## try this pattern  
##                if seger=='高':  ##for some special words both positive and negative, like 'miss'
##                    parseLINE(line)  ## consume much time because of the java CLI, improve 0.2%
##                    fo = open('/home/googcheng/parser/parsed.txt')
##                    target = "nsubj(高-"+str(i+1)
##                    for line in fo:
##                        line=line.strip()
##                        if line:
##                            if line.find(target)!=-1:
##                                print line
##                                position = line.split()[1].find('-')
##                                if line.split()[1][:position] in ['中间','温度','热量','风扇','配置',
##                                                                  '价格','发热量','左边','散热','价钱']:
##                                    fw.write('-高\n');lb=i  ##use const
##                                else:
##                                    fw.write('+高\n');lb=i
                ##  because there is not a No in lexicon
                if list[i]=='没有#VE':
                    try:
                        nextLABEL = getLABEL(list[i+1])
                        if nextLABEL=='NN' and (not dict.get(getWORD(list[i+1]))):
                            fw.write('-没有\n');lb=i
                    except:
                        print "the No,process failed.please check it:",line
                        
                if dict.get(seger):
                    if label=="VA":
                        if i>0:
                            p_label = getLABEL(list[i-1]) 
                            if p_label in ['DEV','DEG'] and i>1:
                                fw.write(''.join(list[i-2:i+1])+'\n');lb=i
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
                                        fw.write(''.join(list[i-3:i+1])+'\n');lb=i
                                    else:
                                        fw.write(''.join(list[i-1:i+1])+'\n');lb=i       

                                else:
                                    if ind<=lb:
                                        ind=lb+1 ## avoid repeated extraction
                                    fw.write(''.join(list[ind:i+1])+'\n');lb=i
                            ###  may other to do   
                            else:
                                fw.write(list[i]+'\n');lb=i
                        else:
                            fw.write(list[i]+'\n');lb=i
                    
                    if label=="NN":
                        if seger in nnSET:  ## skip the zero strength noun
                            continue
                        if i>0:
                            p_label = getLABEL(list[i-1])
                            if p_label in ['AD','JJ','VE','CD']:
                                # VE: 有/没有;CD:一点点
                                fw.write(''.join(list[i-1:i+1])+'\n');lb=i
                            elif p_label=='DT' and i>1:
                                fw.write(findADorVE(''.join(list[i-2:i+1])));lb=i
                            else:
                                fw.write(list[i]+'\n');lb=i
                        else:
                            fw.write(list[i]+'\n');lb=i
                            
                    # verbs ,forward/backward?
                    if label=="VV":
                        if i>0:
                            p_label = getLABEL(list[i-1])
                            if p_label in ['AD','PN','VV']:
                                fw.write(''.join(list[i-1:i+1])+'\n');lb=i
                            else:
                                fw.write(list[i]+'\n');lb=i
                        else:
                            fw.write(list[i]+'\n');lb=i
                                           
                    if label=='AD':
                        if i>0:
                            p_label = getLABEL(list[i-1])
                            if p_label=='NN' and getWORD(list[i-1]) in ['问题','价格','价位','效果',
                                                                       '速度','续航','散热','性能','外观','容量']:
                                fw.write(''.join(list[i-1:i+1])+'\n');lb=i
                            elif p_label=='AD':
                                ind = i-1
                                try:
                                    for j in range(i-2,-1,-1):
                                        if getLABEL(list[j])=='AD':
                                            ind=j
                                        else:
                                            break
                                except:
                                    pass
                                if seger in advSET:  ## enhanced lexicon
                                    if seger=='重' and getWORD(list[i-1]) in['再','往复']:
                                        continue
                                    else:
                                        if ind<=lb:
                                            ind=lb+1
                                        fw.write(''.join(list[ind:i+1])+'\n');lb=i
                            else:
                                fw.write(list[i]+'\n');lb=i
                        else:
                            fw.write(list[i]+'\n');lb=i
                            
                            
                    #interjection        
                    if label=="IJ":
                        fw.write(list[i]+'\n');lb=i
                    if label=="JJ":
                        try:
                            if getLABEL(list[i+1])=='NN':
                                if doSMALLbig(seger,list[i+1]):
                                    fw.write(doSMALLbig(seger,list[i+1]));lb=i
                            elif getLABEL(list[i+1])=='DEG' and getLABEL(list[i+2])=='NN':
                                if doSMALLbig(seger,list[i+2]):
                                    fw.write(doSMALLbig(seger,list[i+2]));lb=i+1
                            ## 长#JJ 时间#NN //notebook +;hotel -
                        except:
                            print "JJ currently,out of range"
                    if label=="CD":  # so small
                        fw.write(list[i]+'\n');lb=i

    fw.close()

def filterPHRASE(phraseFILE,filteredFILE):
    p = re.compile( '#\w{1,3}')
    rmword = re.compile( '\w{1,3}')
    dict = sentiment()
    fo = open(phraseFILE)
    fw = open(filteredFILE,'w')
    for line in fo:
        line = line.strip() # has this line,next line works
        if line:
            if line =='----------':
                fw.write('----------'+'\n')
            elif line == 'SUM':
                fw.write('SUM\n')
            elif line.startswith('+') or line.startswith('-'):
                fw.write(line+'\n')
            else:
                li= line.split('#')
                if len(li) == 3:
                    if li[2]=='VA' and (li[1].startswith('NN') or li[1].startswith('VV')) and (not dict.get(li[0])):
                        fw.write(li[1][2:]+'\n')
                    elif li[1].startswith('PU'):
                        fw.write(li[1][2:]+'\n')
                    else:
                        fw.write(p.sub('   ',line)+'\n')
                elif len(li) ==2:
                    fw.write(li[0]+'\n')
                    
                elif len(li) == 4:  ###  more things to do
                    if not li[1].startswith('VE') and rmword.sub('',li[1]) in ['什么','任何','啥']:
                        fw.write('没有   ' + rmword.sub('',li[2])+'\n')
                    else:
                        if li[1].startswith('VE'):
                            # VE:有/没有
                            fw.write(p.sub('   ',line)+'\n')
                            #print line,p.sub('   ',line)
                        elif li[1].startswith('AD'):
                            if li[2].startswith('DEV') :
                                fw.write(li[0]+'   '+rmword.sub('',li[2])+'\n')
                            else:
                                if li[0] in ['都','就','却','还是']:
                                    fw.write(rmword.sub('','   '.join(li[1:3]))+'\n')
                                else:
                                    fw.write(processADVS(rmword.sub('','   '.join(li[0:3]))))
                        else:
                            if li[1].startswith('LC'):
                                fw.write("不   "+rmword.sub('',li[2])+'\n')  #  add negative
                                #print line,"不   "+rmword.sub('',li[2])
                            else:
                                if li[2].startswith('DT'):
                                    fw.write(rmword.sub('','   '.join(li[1:3]))+'\n')
                                    #print line,rmword.sub('','   '.join(li[1:3]))
                                    
                                else:
                                    fw.write(rmword.sub('',li[2])+'\n')
                                    #print line,rmword.sub('',li[2])
                else:
                    if len(li)==5:
                        if li[2].startswith('VC'):
                            if li[0]=="不":
                                fw.write("shift   "+rmword.sub('','   '.join(li[2:4]))+'\n')
                            else:
                                fw.write(rmword.sub('','   '.join([li[0]]+li[2:4]))+'\n')
                        else:
                            fw.write(rmword.sub('','   '.join(li)+'\n'))
                            #print line,rmword.sub('','   '.join(li))
                    else:
                        #print len(li)
                        fw.write(rmword.sub('','   '.join(li))+'\n')
                                                
    fw.close()





                
                
