import Orange

def itemset(path,path2):
    items = Orange.data.Table(path)
    fw = open(path2,'w')
    print "the frequent itemset is:"
    ind = Orange.associate.AssociationRulesSparseInducer(support=0.009, storeExamples = True)
    itemsets = ind.get_itemsets(items)
    print "the length of itemset:",len(itemsets)
    for itemset, tids in itemsets:
        ##print type(tids),tids   ## tids: transaction id list
        fw.write(" ".join(items.domain[item].name for item in itemset)+'\n')
    fw.close()


if __name__=="__main__":
    itemset('features.basket','itemsets.txt')




