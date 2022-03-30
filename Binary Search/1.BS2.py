''' Binary Search
Comparing the target to mid
By comparing our target to mid, we can identify which side of the boundary does
the target belong. For example, If our target is greater than mid,
this means it must exist in the right of mid . In this case, there is no reason
to even keep a record of all the numbers to its left. And this is the fundamental
mechanics of binary search - keep shrinking the boundary.
'''
import time
class BinarySearch():

    def search(self,array, el)->int:
        
        lo,hi = 0,len(array)-1 # could be [0, n], [1, n] etc. Depends on problem
        
        while (lo < hi):
            mid = lo + (hi-lo+1)//2 #taking the right middle
            print("left\t", "mid\t", "right")
            print(lo,'\t', mid,'\t', hi)
            time.sleep(1)
            # if target element is less then mid
            if (el < array[mid]):
                hi = mid - 1
            else:
                lo = mid; 

        return lo if array[lo]==el else -1
            
arr = [1,3,5,7,8,9,11,11,11,11,11,11,41,43,47,53,59]
x = input("Enter x : ")
bs = BinarySearch()
answer =bs.search(arr,int(x))

print("answer :",answer)