import networkx as nx
import matplotlib.pyplot as plt
### create the graph

DG=nx.DiGraph()
fo = open('./ngd.txt')
dict = {}
for line in fo:
    line=line.strip()
    parts=line.split('---')
    dict[parts[0]]=parts[1]
print len(dict)
###fo.seek(0)
# file cursor goes to the begin

## load sentiment lexicon
###### 
with open('./sentiment2.txt') as fo1:
    lexicon = {}
    for line in fo1:
        line = line.strip()
        if line:
            kv= line.split()
            if len(kv)==2:
                lexicon[kv[0]]=kv[1]

def loadSENTI(path):
    fo = open(path)
    sentiDICT = {}
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
    return sentiDICT


'''
    the construction of the graph
'''
### the phrase2 to change it !!!
#with open('phrase2.txt') as fp:
cnt1 =0 
### the phrase12 is the merge of phrase and phrase2
with open('phrase12.txt') as fp:
    li = []
    todo= set()
    for line in fp:
        line=line.strip()
        if line:
            if line!='----------':
                li.append(line)
            else:
                ## ser phrases of a sentence
                for i in range(len(li)-1):
                    if all(x==1 for x in (len(li[i].split()),len(li[i+1].split()))) and all(x!='SUM' and x!='-4' for x in(li[i],li[i+1])):
                        fir,sec=li[i],li[i+1]
                        if fir == sec:
                            continue
                        if dict.get('   '.join(li[i:i+2])):
                            ngd = float(dict.get('   '.join(li[i:i+2])))
                        else:
                            try:
                                ngd = float(dict.get(li[i+1]+'   '+li[i]))
                            except:
                                #print li[i],'   ',li[i+1],"miss it"
                                todo.add('   '.join(li[i:i+2]))
                        cnt1+=1
                        association= 1 - ngd  ## some asso is zero
                        DG.add_edge(fir.decode('utf8'),sec.decode('utf8'),weight=association)
                        DG.add_edge(sec.decode('utf8'),fir.decode('utf8'),weight=association)
                li = []

    
    already = set()
    for n in DG:
        already.add(n.encode('utf8'))

    for i in lexicon.keys():
        if i not in already:
            DG.add_node(i.decode('utf8'))
print "oov length of NGD:",len(todo)

print "cnt of graph edges is ",cnt1
fw = open("todo.txt",'w')
for i in todo:
    fw.write(i+'\n')
fw.close()
nx.write_gpickle(DG,"paper.gpickle")
