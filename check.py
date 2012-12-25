## do check things methods

def checkoutPHRASE(path):
    ## path to the final phrase
    emptyLIST=[]
    fo =open(path)
    flag=0
    lineNO=0
    for line in fo:
        line=line.strip()
        if line:
            if line=="----------":
                lineNO+=1
                if flag==1:
                    emptyLIST.append(lineNO)
                flag=1
            else:
                flag=0
    print "the length of empty phrase reviews is:",len(emptyLIST)
    return emptyLIST



list  = checkoutPHRASE('phrase2.txt')  #to analyze the final phrase
#print list
fo = open('./neg_tagged.txt')
fw = open('reviewNOphrase.txt','w')
buf = ""
lineNO=0
for line in fo:
    line=line.strip()
    if line:
        if line=="----------#NR":
            lineNO+=1
            if lineNO in list:
                fw.write(buf+'\n')
            buf=''
        else:
            buf+=line
fw.close()
            
            

