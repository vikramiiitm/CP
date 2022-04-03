[3,4,5,1,2]# Number of Times a Sorted array is Rotated

''' Binary Search
If every element in the sorted array were to appear exactly twice,
they would occur in pairs at indices i, i+1 for all even i.
Equivalently, nums[i] = nums[i+1] and nums[i+1] != nums[i+2] for all even i.

When we insert the unique element into this list, the indices of all the pairs following it will
be shifted by one, negating the above relationship.

So, for any even index i, we can compare nums[i] to nums[i+1].

    If they are equal, the unique element must occur somewhere after index i+1
    If they aren't equal, the unique element must occur somewhere before index i+1

Using this knowledge, we can use binary search to find the unique element.
We just have to make sure that our pivot index is always even, 
so we can use 
                mid = 2 * ((lo + hi) // 4) instead of the usual mid = (lo + hi) // 2.
'''
import time
class BinarySearch():

    def search(self, nums) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = 2 * ((lo+hi) // 4) #ensuring mid is even
            print(lo,mid,hi,end=' -> ')
            if nums[mid] == nums[mid+1]:
                lo = mid+2
            else:
                hi = mid
            print(lo,mid,hi)
        return lo
            
# arr = [4,5,6,7,1,2,3]
arr1 =[8,9,1,2,3,4]
nums = [1,1,2,2,3,3,4,4,5,5,7,7,8,10,10]
# arr = [3,4,5,1,2]
n = len(nums)
bs = BinarySearch()
answer =bs.search(nums)
print("arrat: ",nums[answer])
# print("Roation times :",(n-answer)%n)
# print(arr[(answer)%n])