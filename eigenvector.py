import re
import numpy as np
from numpy import array

'''
方根法是通过判断矩阵计算要素相对重要度常用方法
'''
## 输入优先关系矩阵
def ev(m):
    N = m.shape
    R = np.zeros(N)
    S = np.zeros(N[0])
    
    ## 计算模糊一致矩阵
    r = sum(m.T)  ## the initialized eigenvector
    for i in range(N[0]):
        for j in range(N[1]):
            R[i,j] = float(r[i] - r[j])/(2*N[0]) + 0.5
    print "R:"
    print R
            
    ## 方根法
    for i in range(N[0]):
        S[i]= R[i,:].prod()
    S = np.power(S,1.0/N[0])
    S = S /(S.sum())
    return S



if __name__ =="__main__":
    m = array([[0.5,0.5,0.6,0.1,0.2,0.3],
               [0.5,0.5,0.3,0.2,0.2,0.4],
               [0.4,0.7,0.5,0.3,0.3,0.4],
               [0.9,0.8,0.7,0.5,0.5,0.6],
               [0.8,0.8,0.7,0.5,0.5,0.6],
               [0.7,0.7,0.6,0.4,0.4,0.5], 
              ])
    print m
    print ev(m)
    
            
            
            
    
    
                         
