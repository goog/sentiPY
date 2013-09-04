mv $1_seged.txt ~/pos
cd ~/pos
./stanford-postagger.sh models/chinese-nodistsim.tagger $1_seged.txt > $1_tagged.txt
cp $1_tagged.txt ~/py/paper2/









