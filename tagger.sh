cd ~/pos
./stanford-postagger.sh models/chinese-nodistsim.tagger $1_seged.txt > $1_tagged.txt
mv $1_tagged.txt ~/py/paper2/


