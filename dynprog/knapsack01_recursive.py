import timeit
import numpy as np
import sys
sys.setrecursionlimit(1500)

def knapsack_rec(wt,val,W,n):
    if W ==0 or n == 0: #base condtion
        return 0
    
    if (wt[n-1]<=W): # if weight  is less then given total weight
        # include
        return max(val[n-1]+knapsack_rec(wt,val,W-wt[n-1],n-1), knapsack_rec(wt,val,W,n-1))
    
    #if weight greater then max
    else:
        return knapsack_rec(wt,val,W,n-1)



val = np.arange(1,100)
wt = np.arange(1,100)
W = 200
start = timeit.default_timer()
k = knapsack_rec(wt.tolist(),val.tolist(),W,len(val))
end = timeit.default_timer()
print(k,end-start)