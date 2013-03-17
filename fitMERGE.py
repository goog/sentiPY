import math,time
print "starts",time.asctime()


fo3=open('./merge.txt')
fw = open("./merge1.txt",'w')

total = 0
for line in fo3:
    line=line.strip()
    if line:
        if line.find("+")!=-1:
            print line
            total+=1
        else:
            fw.write(line+"\n")
    

fw.close()



print "end.:",time.asctime()
        


