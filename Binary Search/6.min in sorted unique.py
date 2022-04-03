[3,4,5,1,2]# Number of Times a Sorted array is Rotated

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

    def search(self,array)->int:
        
        lo,hi = 0,len(array)-1 # could be [0, n], [1, n] etc. Depends on problem
        
        while (lo < hi):
            mid = lo + (hi-lo+1)//2 #taking the right middle
            n = len(array)
            print(lo, mid, hi)
            # time.sleep(1)
            
            # check if mid array is less then lo array, it means min element is present in left side, ignore right part
            if array[mid]<array[lo]:
                hi = mid-1
            else:   
                #ignore left part
                lo = mid
        
        # returning lo+1 as lo will be the element left to min element(it just how it works with this implementation)
        return lo+1  #answer = (n-(lo+1))%n
            
# arr = [4,5,6,7,1,2,3]
arr1 =[8,9,1,2,3,4]
arr = [11,13,15,17]
# arr = [3,4,5,1,2]
n = len(arr)
bs = BinarySearch()
answer =bs.search(arr)
print("arrat: ",arr)
print("Roation times :",(n-answer)%n)
print(arr[(answer)%n])