from numpy.random.mtrand import randint


def equalsumpartition(arr,n):
    sum = 0
    sum = [sum := sum+i for i in arr]
    print("sum : ", sum)
    # sum = sum/2
    # if sum%2 != 0:
    #     return False

    # creating matrix of  size n+1,sum+1
    t = ([[False for i in range(sum+1)] for i in range(n+1)])

    # initialize matrix
    for i in range(0,n+1):
        for j in range(0,sum+1):
            if i==0:
                t[i][j] = False
            if j == 0:
                t[i][j] = True

    # solution
    for i in range(1,n+1):
        for j in range(1,sum+1):

            if arr[j-1]<=sum:
                t[i][j] = t[i-1][j-arr[i-1]] or t[i-1][j]
            if arr[j-1] > sum:
                t[i][j] = t[i-1][j]
            
    return t[n][sum]

arr = [1,5,11,5]

k = equalsumpartition(arr,len(arr))
print(k)