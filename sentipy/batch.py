import os
from  senti import dbCON,loadSENTI,loadLEXICON,calALL,calPHRASEstrength,statistics
from check import splitLONG
from nlp import StanfordNLP,parser
from preprocess import *
pwd = os.path.dirname(os.path.realpath(__file__))

## the input from mongo line is unicode
def getStrength(nlp,line):
	line = line.strip()
	if line is None:
		return 0
	line = line.encode("utf-8")
	loadSENTI(os.path.join(pwd,'sentiment2.txt'))
	## load the nonlinear sentiment phrase strengths
	nonLINEAR = loadLEXICON(os.path.join(pwd,'nonlinear.txt'))
	## nature language processing

	posed,parsed = parser(nlp,line)
	## find opinion phrases and compute the sentiment strength
	seqs = []
	for pos,parse in zip(posed,parsed):
            phrases = findPHRASE(pos,parse)
	    finalPH = filterPHRASE(phrases)
            
	    phraseNUMBERseqs = calALL(nonLINEAR,os.path.join(pwd,'advxxx.txt'),finalPH)
	    #print "phraseNUMBERseqs: ", phraseNUMBERseqs
            seqs.append(phraseNUMBERseqs)
        #print "seqs:",seqs
	
	senti = statistics("|".join(seqs))
	return senti



if __name__=="__main__":
    db = dbCON('192.168.0.156',27017,'jd')
    coll = db['mobile_evaluation']
    qresult = coll.find({"pid": "1022456996"})
    nlp = StanfordNLP()
    ## create an new collection
    if not ("sentiment" in db.collection_names()):
	db.create_collection("sentiment")
    c2 = db["sentiment"]
    cnt = 0
    
    for doc in qresult:
        if c2.find_one({'_id':doc["_id"]}):
            print "processed once."
	    continue
        line = doc["opnion"]
	line = line.strip()
	if line is None:
	    continue
	strength = getStrength(nlp,doc["opnion"])
        d = doc
	d["strength"] = strength
        c2.insert(d)
	cnt =cnt +1
	print "the count is :",cnt

    print "processe finished ."
               
