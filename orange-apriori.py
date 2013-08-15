import Orange
fw = open('itemsets.txt','w')
items = Orange.data.Table("features.basket")
print "the frequent itemset is:"
ind = Orange.associate.AssociationRulesSparseInducer(support=0.006, storeExamples = True)
itemsets = ind.get_itemsets(items)
print "the length of itemset:",len(itemsets)
for itemset, tids in itemsets:
    ##print type(tids),tids   ## tids: transaction id list
    fw.write(str(len(tids)/float(len(items)))+"       "+" ".join(items.domain[item].name for item in itemset)+'\n')

fw.close()




