from bs4 import BeautifulSoup
import os

def extract(path,pathW):
    f = open(path)
    with open(pathW,'a') as fw:
        soup = BeautifulSoup(f)
        comments = soup.find(id='all_comment')
        cs= BeautifulSoup(str(comments))
        for i in cs.find_all("li",class_="clearfix"):
            ### a comment
            isoup = BeautifulSoup(str(i))
            vote = isoup.find(class_="votes pr5")
            pr =   BeautifulSoup(str(vote)).span.contents[0]
            pr = int(pr)
            if pr  >= 0:
                starS = isoup.find("span",class_="stars")
                ans = BeautifulSoup(str(starS))
                comment = isoup.find("p",class_="w490")
##                print type(BeautifulSoup(str(comment)).p.contents[0])
##                print type(ans.span['title'])
##                print type(BeautifulSoup(str(comment)).p.string)

                try:
                    fw.write(ans.span['title'].encode('utf8')+'----------'.encode('utf8')+BeautifulSoup(str(comment)).p.string.encode('utf8')+'\n')
                except:
                    print "error."
    fw.close()
    



def main():
    r=raw_input("type a directory name:")
    for root,dirs,files in os.walk(r):
        for f in files:
            path = os.path.join(root,f)
            extract(path,'./movie.txt')



main()
