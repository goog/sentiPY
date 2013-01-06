mv $1_seged.txt /home/googcheng/pos
cd ~/pos
./stanford-postagger.sh models/chinese-nodistsim.tagger $1_seged.txt > $1_tagged.txt
mv $1_tagged.txt ~/py/paper2/


