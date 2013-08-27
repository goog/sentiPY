#  POS tagger client
cat <<< $1 | java -mx300m -cp 'stanford-postagger.jar:' edu.stanford.nlp.tagger.maxent.MaxentTaggerServer -port 2020 -client

