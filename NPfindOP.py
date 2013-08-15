import re

'''
according the Feature(noun phrase), to find the corresponding opinion
'''


def opinionSEARCH(path1,path2):

    ## load the frequent feature
    dic = {}
    with open('./itemsets.txt') as fo1:
        for line in fo1:
            line = line.strip()
            line = line.split()[1]
            dic[line]=1
    
    '''  according the typed dependency to find opinions  '''       
    with open(path1) as fo,open(path2,'w') as fw:
        for line in fo:
            line = line.strip()
            if line.startswith('nn(---2, ---1)'):
                continue
            li = line.split('   ')
            ###  some dependencies: assmod
            for i in li:
                if i.startswith('amod'):
                    word = i.split('-')[0][5:]
                    if dic.get(word):
                        fw.write(i+'\n')
		elif i.startswith('assmod'):
                    word = i.split('-')[0][7:]
		    #print i,word
		    #print line
                    if dic.get(word):
                        fw.write(i+'\n')
            
            
        fw.close()

if __name__ == '__main__':
    opinionSEARCH('./neg_parsed_formatnb.txt','./np-op.txt')
                         
