
def findSENTIdroppoint(sentence):
    sentence =sentence.strip()
    if sentence:
        li = sentence.split('|')
        ## there is a summary
        if 's' in li:
            for k,i in enumerate(li):  # find last 's'
                 if i=='s':
                     index=k
            if index==len(li)-1:    ## s in last position
                try:
                    return float(li[index-1])
                except:
                    print "sentiment miss",sentence
                    return 0.0
            else:   
                return float(li[index+1])
                
        else:
            # case 2 begin and end
            if len(li)==1:
                return float(li[0])
            begin = float(li[0]);end = float(li[-1])
            if abs(begin)>abs(end):
                return begin
            elif abs(begin)<abs(end):
                return end
            else:
                if len(li)==2:
                    return end
                else:  ##length more than two,** strength vs count ** neg strengths are weak 
                    newLIST= [abs(float(i)) for i in li[1:-1]]
                    ind = newLIST.index(max(newLIST))
                    ## if float(li[1:-1][ind]) smaller than two ,count 
                    return float(li[1:-1][ind])
## for negativfe,  there is a issue. 

           


def calORIENTATION(strength):
    if strength>0:
        return 1
    elif strength<0:
        return -1
    else:
        return 0




    
    












            
    
            




                
                
