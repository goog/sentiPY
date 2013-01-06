#/home/googcheng/segmenter/segment.sh ctb preprocess-$1.txt UTF-8 0 > $1_seged.txt
cd ~/segmenter
java -mx1g -cp seg.jar edu.stanford.nlp.ie.crf.CRFClassifier -sighanCorporaDict data -loadClassifier data/ctb.gz -testFile preprocess-$1.txt -inputEncoding UTF-8 -sighanPostProcessing true -serDictionary data/dict-chris6.ser.gz,data/cedict.txt,data/ntusd.txt  -keepAllWhitespaces false >$1_seged.txt 
cp $1_seged.txt ~/py/paper2/
