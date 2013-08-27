# the first parameter is a string 、  bash，ksh或zsh中也可以用here-字串
java -mx700m -cp "stanford-ner.jar:" edu.stanford.nlp.ie.NERServer -port 9191 -client  <<< $1
