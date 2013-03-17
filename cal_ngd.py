import math,time
print "starts",time.asctime()

fo2=open("./single.txt")
fo3=open('./merge.txt')
fw = open("./ngd.txt",'w')

dict = {}
list=[]
for line in fo2:
    line=line.strip()
    parts=line.split()
    dict[parts[0]]=parts[1]
    list.append(int(parts[1]))
list.sort()
print "the max indexed:",list[-1]
print "there are %s query items " % len(dict)


N=10000000000
## 1204070806
cnt=0
total=0
lost = set()
for line in fo3:
    line=line.strip()
    parts=line.split()
    total+=1
    a,b= parts[0],parts[1]
    try:
        Fx=int(dict.get(a));
    except:
        #print "miss a",a
        lost.add(a)
    try:
        Fy=int(dict.get(b));
    except:
        #print "miss b",b
        lost.add(b)
    try:
        Fxy=int(parts[2])
    except:
        print "miss fxy::",line
    logx=math.log(Fx);logy=math.log(Fy);logxy=math.log(Fxy)
    ngd=(max(logx,logy)-logxy) / float(math.log(N)-min(logx,logy))
    if ngd >1:
        cnt+=1
        ngd= 1 ##### ??
    fw.write('   '.join(parts[0:2])+'---'+str(ngd)+"\n")
    
print "times that ngd bigger than one:",cnt
print "the radio is :", float(cnt)/total
fw.close()

for i in lost:
    print i

print "end.:",time.asctime()
        


