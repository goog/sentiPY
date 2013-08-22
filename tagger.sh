mv $1_seged.txt ~/pos
cd ~/pos
./stanford-postagger.sh models/chinese-nodistsim.tagger $1_seged.txt > $1_tagged.txt
cp $1_tagged.txt ~/py/paper2/



#  pos tagger client
# java -mx300m -cp 'stanford-postagger.jar:' edu.stanfordlp.tagger.maxent.MaxentTaggerServer -port 2020 -client < file.txt





