''' Binary Search
Comparing the target to mid
By comparing our target to mid, we can identify which side of the boundary does
the target belong. For example, If our target is greater than mid,
this means it must exist in the right of mid . In this case, there is no reason
to even keep a record of all the numbers to its left. And this is the fundamental
mechanics of binary search - keep shrinking the boundary.
'''
import time

# by default BS implemetation(Your implementation only) gives right most element.

class BinarySearch():
    def __init__(self):
        self.res = [-1,-1]
        self.count = 0

    def search(self,array, el)->int:
        
        lo,hi = 0,len(array)-1 # could be [0, n], [1, n] etc. Depends on problem
        while (lo < hi):
            mid = lo + (hi-lo+1)//2 #taking the right middle
            # print("left\t", "mid\t", "right")
            # print(lo,'\t', mid,'\t', hi)
            # time.sleep(1)
            # if target element is less then mid
            if (el < array[mid]):
                hi = mid - 1
            else:
                lo = mid; 

        
        # if we found searched element at lo key then we find the element in array(0 to lo) recursively
        if array[lo] == el:
            # store the found keys of element and replace untill we found left most key
            self.res[0] = lo
            
            # store the right most index of element, we get this first time
            if self.count == 0:
                self.res[1] = lo
                self.count+=1
            return self.search(array[:lo],el)
            
        else:
            return self.res
            
arr = [1,3,5,11,11,11,13,17,19,23,29,31,11,37,41,43,47,53,59]
x = input("Enter x : ")
bs = BinarySearch()
answer =bs.search(arr,int(x))

print("answer :",answer)