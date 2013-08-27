java -mx1g -cp "stanford-ner.jar:seg.jar" edu.stanford.nlp.ie.NERServer -port 9191 -sighanCorporaDict data -loadClassifier data/pku.gz  -serDictionary data/dict-chris6.ser.gz
