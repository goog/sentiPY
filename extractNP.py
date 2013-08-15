import re

'''
Nouns(2): NR, NN
'''

## FOR more efficient, create a filter dictionary to filter the noun(phrase)

pat = re.compile(ur'\S*#N[NR]')
def pos2basket(path,out):
    with open(path) as fo,open(out,'w') as fw:
        for line in fo:
            line = line.strip()
            line = line.decode('utf8')
            match = pat.findall(line)
            if match:
                noun = ','.join(match).encode('utf8')
                noun = noun.replace("#NN",'').replace("#NR",'')
                fw.write(noun+'\n')
        fw.close()

if __name__ == '__main__':
    pos2basket('./computer.txt','./features.basket')
                         
