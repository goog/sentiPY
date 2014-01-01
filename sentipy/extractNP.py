import re
from check import file2dic,splitSegmented
'''
Nouns(2): NR, NN
'''

pat = re.compile(ur'\S*#N[NR]')
def pos2basket(path,out):
    exclude = file2dic("./feature-exclude.txt")
    with open(path) as fo,open(out,'w') as fw:
        nnLIST= []
        for line in fo:
            line = line.strip()
            #if line == "--#PU --#PU --#PU --#PU --#PU":
            if line == "---------#NR -#PU":
                if nnLIST:
                    fw.write(','.join(nnLIST)+'\n')
                    nnLIST= []
            else:
                line = line.decode('utf8')
                match = pat.findall(line)
                if match:
                    nouns = map(lambda x:x.encode('utf8'), match)
                    for noun in nouns:
                        noun = noun.replace("#NN",'').replace("#NR",'')
                        if exclude.get(noun):
                            continue
                        nnLIST.append(noun)
        fw.close()

if __name__ == '__main__':
    #pos2basket('./computer.txt','./features.basket')
    pos2basket('./evaluation.txt','./features.basket')
    #splitSegmented("/home/drill/evaluation_seged.txt","/home/drill/evaluation-segged.txt")
                         
