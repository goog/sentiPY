import os,sys
import re



fo1 = open('./oov.txt')
fo2 = open('./oov1.txt')
a =set()
b= set()
for line in fo1:
    line=line.strip()
    if line:
        a.add(line.split()[0])

#print len(a)


for line in fo2:
    line=line.strip()
    if line:
        b.add(line)

print  len(b-a)        
for i in (b -a):
    print i






                
                
