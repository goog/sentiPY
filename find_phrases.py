import os,sys
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

#labels = ['VA', 'AD', 'NN', 'VV', 'SP', 'CD', 'P', 'IJ', 'JJ', 'CS', 'NR', 'PN']
#label_dict = {}.fromkeys(labels,0)
#{'VA': 4937, 'AD': 437, 'NN': 1299, 'SP': 1, 'CD': 13, 'P': 1, 'IJ': 26,
#'VV': 1866, 'CS': 1, 'JJ': 255, 'PN': 1, 'NR': 7}


fo = open("./pos_tagged.txt")
fw = open('./pos_phrase.txt','w')
for line in fo:
    line = line.strip() # has this line,next line works
    if line =='----------#NR':
        fw.write('----------'+'\n')
        continue
    list = line.split()
    #list elements are Word#POS
    for i in range(len(list)):
        index = list[i].find('#');seger = list[i][:index];label = list[i][index+1:]
        #word in sentiment lexicon
        if seger=="总体":
            fw.write('SUM\n')
        if dict.get(seger):
            #label_dict[label]=label_dict[label]+1
            #Adjective e.g. 还是#AD不错#VA
            if label=="VA":
                if i>0:
                    p_label = list[i-1][list[i-1].find('#')+1:]
                    #consider '的' 
                    if p_label in ['DEV','DEG'] and i>1:
                        fw.write(''.join(list[i-2:i+1])+'\n')
                    else:
                        # this pattern is very important
                        fw.write(''.join(list[i-1:i+1])+'\n')
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
                    index = list[i-1].find('#');p_label = list[i-1][index+1:]
                    if p_label=='NN' and list[i-1][:index] in ['问题','价格','价位','效果','速度','续航','散热','性能','外观','容量']:
                        fw.write(''.join(list[i-1:i+1])+'\n')
            #感叹词        
            if label=="IJ":
                fw.write(list[i]+'\n')
            if label=="JJ":
                fw.write(list[i]+'\n')
            if label=="CD":
                fw.write(list[i]+'\n')
            

   
fw.close()
#print label_dict 


                
                
