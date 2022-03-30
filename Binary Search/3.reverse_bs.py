import time

class BS():

    def search(self, array, el):
        lo, hi = 0, len(array)-1
        
        while lo < hi:
            mid = lo + (hi - lo + 1)//2
            if el > array[mid]:
                hi = mid - 1
            else:
                lo = mid
                
        return lo if array[lo] == el else -1

bs = BS()
array  = [i for i in range(100,0,-2)]
x = input("Enter key to search: ")
k = bs.search(array,int(x))

print(f'Element found at index {k}')