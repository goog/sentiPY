import os,sys

fo = open("./pos_phrase.txt")
a= set()
for line in fo:
    line = line.strip()
    index = line.find('#')
    a.add(line[index+1:])
            

print a                
                
