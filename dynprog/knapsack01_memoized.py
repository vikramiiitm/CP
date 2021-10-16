import timeit
import numpy as np
import sys
sys.setrecursionlimit(1500)

global t
def knapsack_rec(wt,val,W,n):
    if n==0 or W==0:
        return 0

    if t[n][W] !=-1: #base condtion
        return t[n][W] 
    
    if (wt[n-1]<=W): # if weight  is less then given total weight
        # include
        t[n][W] =  max(val[n-1]+knapsack_rec(wt,val,W-wt[n-1],n-1), knapsack_rec(wt,val,W,n-1))
        return t[n][W]
    
    #if weight greater then max
    else:
        t[n][W] = knapsack_rec(wt,val,W,n-1)
        return t[n][W]


val = np.arange(1,1000)*2
wt = np.arange(1,1000)
W = 1000

t = np.full((len(val)+1,W+1),-1)

start = timeit.default_timer()

knapsack_rec(wt,val,W,len(val))

end = timeit.default_timer()

print(t[len(val),W],end-start)
print(t)