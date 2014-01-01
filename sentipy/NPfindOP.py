import re
import os
pwd = os.path.dirname(os.path.realpath(__file__))

'''
according features(noun phrase) to find the corresponding opinion
'''

han = re.compile(ur'[\u4e00-\u9fa5]+')

def extractDEP(dep,order=0):
    ''' extract two key words from a dependency '''
    li1 = dep.split('(')
    content = li1[1]
    li2 = content.split()
    ele1 = li2[0][:li2[0].find('-')]
    ele2 = li2[1][:li2[1].find('-')]
    if order:
        return [ele2,ele1]
    return [ele1,ele2]

## this method needs a special Chinese parser.
def opinionSEARCH(path1,path2):
    ## load the frequent feature
    dic = {}
    #with open('./itemsets.txt') as fo1:
    with open('./itemsetsMANUAL.txt') as fo1:
        for line in fo1:
            line = line.strip()
            dic[line]=1
    
    '''  according the typed dependency to find opinions  
	#todo: create a dictionary to filter the another word in the dep
    '''   
    with open(path1) as fo,open(path2,'w') as fw:
        for line in fo:
            line = line.strip()
            if line.startswith('nn(---2, ---1)'):
                continue
            li = line.split('   ')
            ##  some dependencies: assmod  , nsubj , [nsubjpass 名词性被动主语,not a good idea]
            for i in li:
                if i.startswith('amod'):
                    word = i.split('-')[0][5:]
                    if dic.get(word):
                        fw.write(' '.join(extractDEP(i,order=1))+'\n')
                elif i.startswith('assmod'):
                    word = i.split('-')[0][7:]
                    if dic.get(word):
                        fw.write(' '.join(extractDEP(i,order=1))+'\n')        
        fw.close()



    #######################################
    ##what's called the adjacent adjective#
    #######################################

## search the adjacent adjective
sp = re.compile(r'#\w{1,3}')
def opinionSEARCH2(path1,path2):
    ## path1: the POSed files
    
    ## load the frequent feature
    dic = {}
    #with open('./itemsets.txt') as fo1:
    with open('./itemsetsMANUAL.txt') as fo1: ## under testing
        for line in fo1:
            line = line.strip()
            dic[line]=1
    
    with open(path1) as fo,open(path2,'w') as fw:
        for line in fo:
            line = line.strip()
            if line == "--#PU --#PU --#PU --#PU --#PU":
                continue
            li = line.split()
            LINE = line.decode('utf8')
            match = sp.sub('',LINE)
            match = match.split()
            hanLIST = map(lambda x:x.strip().encode('utf8'), match)
            for i,item in enumerate(hanLIST):
                if dic.get(item) and (i < len(hanLIST)-1):
                    for j in range(i+1,len(hanLIST),1):   ## afterward
                        if li[j].split("#")[0] in [',','，','。','!','！']:  ##break before next subsentence
                            break
                        if (j <= i+4) and (li[j].endswith("#VA")==True):   ## find the adj within a fixed intervals
                            fw.write(item+"   "+li[j].split("#")[0]+"\n")
                            break
        fw.close()

def opinionSEARCH3(str1):
    ## param: the POSed line
    
    ## load the frequent feature
    dic = {}
    with open(os.path.join(pwd,'itemsetsMANUAL.txt')) as fo1:
        for line in fo1:
            line = line.strip()
            dic[line]=1
    
    fCNT = 0
    li = str1.split()
    LINE = str1.decode('utf8')
    match = sp.sub('',LINE)
    match = match.split()
    hanLIST = map(lambda x:x.strip().encode('utf8'), match)

    npop = []
    for i,item in enumerate(hanLIST):
        if dic.get(item):
            fCNT +=1
            if i < len(hanLIST)-1:
                for j in range(i+1,len(hanLIST),1):   ## afterward
                    if li[j].split("#")[0] in [',','，','。','!','！']:  ##break before next subsentence
                        break
                    if (j <= i+4) and (li[j].endswith("#VA")==True):   ## find the adj within a fixed intervals
                        npop.append(item+"   "+li[j].split("#")[0]+"\n")
                        break
    return npop,fCNT

if __name__ == '__main__':
    opinionSEARCH('./neg_parsed_formatnb.txt','./np-op.txt')
    opinionSEARCH2('./evaluation.txt','./np-op.txt')
    npop,FCNT=opinionSEARCH3('屏幕大')
    print npop
    print FCNT                

