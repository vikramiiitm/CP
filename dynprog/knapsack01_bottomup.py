import timeit
import numpy as np
import timeit


def knapsack_rec(wt,val,W,n):
    # t = np.full((n+1,W+1),0)
    global t

    start = timeit.default_timer()
    t = [[0 for x in range(W + 1)] for x in range(n + 1)]
    for i in range(n+1):
        for j in range(W+1):
            if i == 0:
                t[i][j] = False
            if j == 0:
                t[i][j] = True

    for i in range(n+1):
        for j in range(W+1):
            if i==0 or j==0:
                t[i][j]=0

            elif(wt[i-1]<=W):
                t[i][j]=max(val[i-1] + t[i-1][j-wt[i-1]],  t[i-1][j])
            
            elif(wt[i-1]>W):
                t[i][j]=t[n-1][j]
    end = timeit.default_timer()

    print("Exec time : ",end-start)
            
    return t[n][W]


# val = np.arange(1,100)*2
# wt = np.arange(1,100)
# W = 10

val = [1,2,3]
wt = [1, 2, 3]
W = 5


start = timeit.default_timer()

j = knapsack_rec(wt,val,W,len(val))

end = timeit.default_timer()

print(j,end-start)
print(t[len(val)][W])