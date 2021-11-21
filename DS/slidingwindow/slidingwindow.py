def windowsum(arr,k):
    start = 0
    end = 0
    sum = 0

    while (end-start+1) <= k:
        sum =sum + arr[end]
        end+=1
    l = []
    l.append(sum)
    while end<len(arr):
        sum = sum-arr[start]+arr[end]
        l.append(sum)
        start+=1
        end+=1
    return l

arr = [1,2,3,4,5]
k = 2

l = windowsum(arr,k)
print(max(l))