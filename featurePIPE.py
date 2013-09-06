import re,os
from check import file2dic
pwd = os.path.dirname(os.path.realpath(__file__))
'''  make a distribution of the features   '''

def count(path,out):
    with open(path) as fo,open(out,'w') as fw:
        posD = file2dic(os.path.join(pwd,'pos.txt'))
        negD = file2dic(os.path.join(pwd,'neg.txt'))
        distribution = {}
        for line in fo:
            line = line.strip()
            feature = line.split('   ')[0]
            opinion = line.split('   ')[1]
            if opinion:
                if posD.get(opinion):
                    if distribution.get(feature) is None:
                        distribution[feature] = {"pos":1,"neg":0}
                    else:
                        distribution[feature]["pos"]+=1
                elif negD.get(opinion):
                    if distribution.get(feature) is None:
                        distribution[feature] = {"pos":0,"neg":1}
                    else:
                        distribution[feature]["neg"]+=1


        for i in distribution.keys():
            posCNT = (0 if distribution[i].get("pos") is None else distribution[i].get("pos"))
            negCNT = (0 if distribution[i].get("neg") is None else distribution[i].get("neg"))
            total = posCNT + negCNT
            posRATIO = "%.4f" %(float(posCNT) /total)
            negRATIO = "%.4f" %(float(negCNT) /total)
            fw.write(i+": "+"the positive ratio: "+posRATIO+" , the negative ratio: "+negRATIO+"\n")    
                                   
        fw.close()

## the distribution is a global variable
distribution = {}
posD = file2dic(os.path.join(pwd,'pos.txt'))
negD = file2dic(os.path.join(pwd,'neg.txt'))
def countSTREAM(npop,distribution):
    line = npop.strip()
    feature = line.split('   ')[0]
    opinion = line.split('   ')[1]
    if opinion:
        if posD.get(opinion):
            if distribution.get(feature) is None:
                distribution[feature] = {"pos":1,"neg":0}
            else:
                distribution[feature]["pos"]+=1
        elif negD.get(opinion):
            if distribution.get(feature) is None:
                distribution[feature] = {"pos":0,"neg":1}
            else:
                distribution[feature]["neg"]+=1

def showCOUNT(distribution):
        for i in distribution.keys():
            posCNT = (0 if distribution[i].get("pos") is None else distribution[i].get("pos"))
            negCNT = (0 if distribution[i].get("neg") is None else distribution[i].get("neg"))
            total = posCNT + negCNT
            posRATIO = "%.4f" %(float(posCNT) /total)
            negRATIO = "%.4f" %(float(negCNT) /total)
            print (i+": "+"the positive ratio: "+posRATIO+" , the negative ratio: "+negRATIO)
            ## return the list
                                   

if __name__ == '__main__':
    #count("./np-op.txt","featureCOUNT.txt")
    fo = open("./np-op.txt")
    for line in fo:
        countSTREAM(line,distribution)
    showCOUNT(distribution)
    
        
                         
