''' Binary Search '''

class BinarySearch():

    def search(self,array, el)->int:
        
        left,right = 0,len(array)-1 # could be [0, n], [1, n] etc. Depends on problem
        
        while left <= right :
            mid = left + (right-left)//2
            print("left\t", "mid\t", "right")
            print(left,'\t', mid,'\t', right)
            # condition, it depends on problem
            
            # ignore right
            if array[mid] < el:
                left = mid+1
            elif array[mid]> el:
                right = mid-1
            else:
                return mid
        return -1
            
arr = [1,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
x = input("Enter x : ")
bs = BinarySearch()
answer =bs.search(arr,int(x))

print("answer :",answer)