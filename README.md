#SentiPY
SentiPY is a sentiment ananlysis system based on the SentiDP algorithm and implemented by Python.SentiDP stands for the "Sentiment Drop Point", utilizes the sentiment word strength(like "good" labeled with the value +3) to classify reviews. 


### what's the Features
1, Sentiment classificaton based on sentiment word strengths;  
2, Sentiment rating;   
3, Sentiment effectiveness rank;  
4, Extracting aspect-opinions;

##Requirement 
We need a Stanford NLP service, but its size is more than 300Mb, so we need to download it manually from Dropbox.  
1,**install corenlp-python**(include the Stanford CoreNLP)  
```wget https://www.dropbox.com/s/21wkispu69cmk7n/corenlp.tar.gz```  
```tar xvzf corenlp.tar.gz```  
```cd corenlp-python```    
```python corenlp/corenlp.py```  
then the NLP server is running.

##usage:
install the python package first
####1,nlp(to do segment\pos\parse)
```from sentipy import nlp```  
```server = nlp.StanfordNLP()```  
```print nlp.parser1(server,"我在广州") ```  
####2,sentiment analysis
```from sentipy import senti```  
```s = senti.senti()```  
`s.sentiFLY("新年快乐")`


