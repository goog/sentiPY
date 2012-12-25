# -*- coding:utf-8 -*-
import os,sys,re
import subprocess


def rmBLANK(path,writeTO):
    fo = open(path)
    fw = open(writeTO,'w')
    for line in fo:
        line = line.strip()
        if line:
            fw.write(line+'\n')       
    fw.close()

def readFILEasSET(path):
    newSET = set()
    fo = open(path)
    for line in fo:
        line = line.strip()
        if line:
            newSET.add(line)
    return newSET

pal = re.compile(ur'\(.+?\)')
pal2 = re.compile(ur'\uff08.+?\uff09')
quote = re.compile(ur'".+?"')
quote2 = re.compile(ur'\u201c.+?\u201d')
#suiran = re.compile(ur'\u867d\u7136.+?\u4f46.+?[,!\uff01\uff0c\u3002\uff1b]')
#chinese notation must unicode in reg
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
    
    

def parse():
    pass

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

 
## the vital method
def findPHRASE(taggedFILE,posedFILE):
    dict = sentiment()
    advSET = readFILEasSET('./sentiADV.txt') ## read advs which have sentiment
    fo = open(taggedFILE)
    fw = open(posedFILE,'w')
    for line in fo:
        line = line.strip()
        if line:
            if line =='----------#NR':
                fw.write('----------\n')
                continue
            list = line.split()       #list elements are Word#POS
            for i in range(len(list)):
                index = list[i].find('#');seger = list[i][:index];
                label = getLABEL(list[i])
                if seger in ['整体','总之','总体','总而言之','总的来说','总结','整体性','总体性']:
                    fw.write('SUM\n')
                if dict.get(seger):   #current word in sentiment lexicon
                    #label_dict[label]=label_dict[label]+1
                    if label=="VA":
                        if i>0:
                            p_label = getLABEL(list[i-1])
                            #consider '的' 
                            if p_label in ['DEV','DEG'] and i>1:
                                fw.write(''.join(list[i-2:i+1])+'\n')
                            elif p_label=='AD':
                                if i==1:
                                    fw.write(''.join(list[0:2])+'\n')
                                else:
                                    ind = i-1
                                    for j in range(i-2,-1,-1):
                                        if getLABEL(list[j])=='AD':
                                            ind=j
                                        else:
                                            break
                                    if ind==i-1 and i>2:
                                        if getLABEL(list[i-2])=='VC' and getLABEL(list[i-3])=='AD':
                                            fw.write(''.join(list[i-3:i+1])+'\n')
                                        else:
                                            fw.write(''.join(list[i-1:i+1])+'\n')
                                            

                                    else:
                                        fw.write(''.join(list[ind:i+1])+'\n')
                            ###  may other to do   
                            else:
                                fw.write(list[i]+'\n')
                        else:
                            fw.write(list[i]+'\n')
                    
                    # nouns
                    if label=="NN":
                        if i>0:
                            p_label = list[i-1][list[i-1].find('#')+1:]
                            if p_label in ['AD','JJ','VE','CD']:
                                # VE: 有/没有;CD:一点点
                                fw.write(''.join(list[i-1:i+1])+'\n')
                            elif p_label=='DT' and i>1:
                                #print ''.join(list[i-2:i+1])
                                fw.write(''.join(list[i-2:i+1])+'\n')
                            else:
                                fw.write(list[i]+'\n')
                        else:
                            fw.write(list[i]+'\n')
                            
                    # verbs ,forward/backward
                    if label=="VV":
                        if i>0:
                            p_label = list[i-1][list[i-1].find('#')+1:]
                            if p_label in ['AD','PN','VV']:  #PN means I(subjective);算#VV可以#VV;没#VV得说#VV
                                fw.write(''.join(list[i-1:i+1])+'\n')
                            else:
                                fw.write(list[i]+'\n')
                        else:
                            fw.write(list[i]+'\n')
                            
                    if label=='AD' and i>0:
                        index = list[i-1].find('#');p_label = getLABEL(list[i-1])
                        if p_label=='NN' and list[i-1][:index] in ['问题','价格','价位','效果','速度','续航','散热','性能','外观','容量']:
                            #print ''.join(list[i-1:i+1])
                            fw.write(''.join(list[i-1:i+1])+'\n')
                        elif p_label=='AD':
                            ind = i-1
                            for j in range(i-2,-1,-1):
                                if getLABEL(list[j])=='AD':
                                    ind=j
                                else:
                                    break
                            if seger in advSET:
                                if seger=='重' and list[i-1][:index] in['再','往复']:
                                    continue
                                else:
                                    fw.write(''.join(list[ind:i+1])+'\n')
                                    #print ''.join(list[ind:i+1])
                        else:
                            fw.write(''.join(list[i])+'\n')
                            
                    #interjection        
                    if label=="IJ":
                        fw.write(list[i]+'\n')
                    if label=="JJ":
                        if seger not in ['大']:
                            fw.write(list[i]+'\n')
                    if label=="CD":
                        fw.write(list[i]+'\n')

    fw.close()
    #print label_dict


def filterPHRASE(phraseFILE,filteredFILE):
    cnt5 = 0
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
                    #  solve 有些#AD 不#AD 合理#VA
                    if not li[1].startswith('VE') and rmword.sub('',li[1]) in ['什么','任何','啥']:
                        fw.write('没有   ' + rmword.sub('',li[2])+'\n')
                        #print '没有   ' + rmword.sub('',li[2])
                    else:
                        if li[1].startswith('VE'):
                            # VE:有/没有 ,
                            fw.write(p.sub('   ',line)+'\n')
                            #print line,p.sub('   ',line)
                        elif li[1].startswith('AD'):
                            if li[2].startswith('DEV') :
                                fw.write(li[0]+'   '+rmword.sub('',li[2])+'\n')
                                #print line,li[0]+'   '+rmword.sub('',li[2])
                            else:
                                ## ad attention
##确实#AD不#AD低#VA 低
##都#AD挺#AD烫#VA 烫
##极#AD不#AD舒服#VA 舒服
                                fw.write(rmword.sub('','   '.join(li[0:3]))+'\n')
                                ##todo liner and nonlinear
                                ###print line,rmword.sub('','   '.join(li[0:3]))
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
                        ##cnt5+=1
                        if li[2].startswith('VC'):
                            if li[0]=="不":
                                fw.write("shift   "+rmword.sub('','   '.join(li[2:4]))+'\n')
                            else:
##本#AD是#VC很#AD时尚#VA
##实在#AD是#VC太#AD麻烦#VA
##的确#AD是#VC比较#AD大#VA
                                fw.write(rmword.sub('','   '.join(li[2:4]))+'\n')
                                
                                
                    else:
                        fw.write(rmword.sub('','   '.join(li[2:4]))+'\n')
                                                
    fw.close()




                
                
