cd ~/parser
java -mx1g -cp stanford-parser.jar:stanford-parser-2.0.4-models.jar:. edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat typedDependencies -encoding utf-8 edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz line.txt  > parsed.txt

