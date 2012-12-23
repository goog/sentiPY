import os,sys
import re

p = re.compile( '#\w{1,3}')
rmword = re.compile( '\w{1,3}')
dict_list=[]
fo1 = open('./neg.txt')
fo2 = open('./pos.txt')
for line in fo1:
    line=line.strip()
    dict_list.append(line)

for line in fo2:
    line=line.strip()
    dict_list.append(line)
dict = {}.fromkeys(dict_list,1)
print "there is %s words in sentiment dictionary" % len(dict)




fo = open("./pos_phrase.txt")
fw = open('./phrase.txt','w')
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
                
            else:
                #print line
                if len(li) == 4:
                    if not li[1].startswith('VE') and rmword.sub('',li[1]) in ['什么','任何','啥'] :
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
                                fw.write(rmword.sub('',li[2])+'\n')
                                #print line,rmword.sub('',li[2])
                                
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
                        
                        
                        
                        
                
   
fw.close()



                
                
