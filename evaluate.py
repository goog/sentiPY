def findSENTIdroppoint(sentence):
    sentence =sentence.strip()
    if sentence:
        li = sentence.split('|')
        for i in [0,-1]:
            if li and li[i]=='0':
                li.pop(i)
        if not li:
            return 0
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
                    return 0
            else:   
                return float(li[index+1])
                
        else:
            # case 2 begin and end
            if len(li)==1:
                try:
                    return float(li[0])
                except:
                    return 0  
            begin = float(li[0]);end = float(li[-1])
            if abs(begin)>abs(end):
                return begin
            elif abs(begin)<abs(end):
                return end
            else:
                absLI = [abs(float(i)) for i in li]
                ind = absLI.index(max(absLI))
                if ind == 0 or ind==len(li)-1:
                    return begin
                else:
                    return float(li[ind])
    else:
        return 0  #  because of no extraction sentiment

## common method, to aggregate it
def commonSENTI(sentence):
    sentence =sentence.strip()
    sum = 0
    if sentence:
        li = sentence.split('|')
        for i in li:
            try:
                sum+=float(i)
            except:
                continue
    return sum

def calORIENTATION(strength):
    if strength>0:
        return 1
    elif strength<0:
        return -1
    else:
        return 0


if __name__ == '__main__':
    print findSENTIdroppoint('-1.0')
    print commonSENTI('s|1.8|-5.85|0|s|1.0|0')
    




    
    












            
    
            




                
                
