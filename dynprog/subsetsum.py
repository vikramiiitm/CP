import numpy as np
import timeit

def subsetsum(arr,n,sum):
    start = timeit.default_timer()

    t = ([[ False for i in range(sum+1)] for i in range(n+1)])

    for i in range(n+1):
        for s in range(sum+1):
            if i == 0:
                t[i][s] = False
            if s == 0:
                t[i][s] = True
    # print("t : ",t)
    for i in range(1,n+1):
        for s in range(1,sum+1):
            if arr[i-1]<=sum:
                t[i][s] = t[i-1][s-arr[i-1]] or t[i-1][s]
            if arr[i-1]>sum:
                t[i][s] = t[i-1][s]
    end = timeit.default_timer()
    print("Exec Time : ",end-start)
    print(t)
    return t[n][sum]


arr = np.random.randint(100,size=(10))
sum = 1121

k = subsetsum(arr,len(arr),sum)
print(k)