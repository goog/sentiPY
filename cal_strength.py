import networkx as nx
import math

#####
'''there be unicode / utf8 '''
#####

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

DG=nx.read_gpickle("paper.gpickle")
nn= DG.number_of_nodes()
print "the number of nodes:",nn

cnt_sole=0
for n in DG:
    if not DG.predecessors(n):
        cnt_sole+=1
print "sole nodes:",cnt_sole

#init the strength
senti = loadSENTI('./sentiment2.txt')
for n in DG:
    DG.node[n]['s']=senti.get(n.encode('utf8'))
    
#iter
for i in xrange(100):
    li = []
    for n in DG:
        if DG.in_degree(n)==0:
            DG.node[n]['s1']=DG.node[n]['s']
        else:
            DG.node[n]['s1']=0
            neighbors=DG.predecessors(n)
            for nb in neighbors:
                try:
                    w=DG[nb][n]['weight'] / float(DG.out_degree(nb,weight='weight'))
                    if senti.get(n.encode('utf8'))*senti.get(nb.encode('utf8'))<0:
                        w*=-1
                    DG.node[n]['s1']+= w*DG.node[nb]['s']
                except:
                    print n.encode('utf8'),nb.encode('utf8')
                    ## no ngd
            try:
                DG.node[n]['s1']+=DG.node[n]['s']
            except:
                pass
        li.append(DG.node[n]['s1'])
            
    #normalize the strength: method
    li.sort(reverse=True)
    a = []
    print "the mormalized factor :",li[0]
    for n in DG:
        #DG.node[n]['s1']=DG.node[n]['s1']/math.sqrt(sums)
        DG.node[n]['s1']=DG.node[n]['s1']/li[0]
        try:
            a.append(abs(DG.node[n]['s1']-DG.node[n]['s']))
        except:
            pass
        DG.node[n]['s']=DG.node[n]['s1']

    a.sort(reverse=True)
    if a[0] < 0.02:
        print "iter %s th stop" % i
        break

fw=open("mySTRENGTH.txt","w")           
for n in DG:
    fw.write(n.encode('utf8')+"    "+str(DG.node[n]['s'])+"\n")
fw.close()
