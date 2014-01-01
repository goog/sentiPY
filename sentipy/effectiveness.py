import re
import numpy as np
from numpy import array
from eigenvector import ev


## input params:
## ev: the eigenvector
## means: the means of six measures
def efSCORE(scores,ev,means):
    scores = array(scores)  ## the score array of one review
    means = array(means,dtype=np.float)
    score = scores /means   ## equalization
    return np.dot(score,ev)



if __name__=="__main__":
    m = array([[0.5,0.5,0.6,0.1,0.2,0.3],
               [0.5,0.5,0.3,0.2,0.2,0.4],
               [0.4,0.7,0.5,0.3,0.3,0.4],
               [0.9,0.8,0.7,0.5,0.5,0.6],
               [0.8,0.8,0.7,0.5,0.5,0.6],
               [0.7,0.7,0.6,0.4,0.4,0.5], 
              ])
    scores = [1,2,3,4,5,6]
    means  = [0.9,1.8,3,4,5,6]
    print "the score is:",efSCORE(scores,ev(m),means)
    
    
    
    

            
            
            
    
    
                         
