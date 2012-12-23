import os,sys
dict1={}
dict2={}
fo1 = open('./1.txt')
fo2 = open('./2.txt')
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



                
                
