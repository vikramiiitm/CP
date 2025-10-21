# Find the maximum and minimum of all subarrays of size k

arr = [1,3,-1,-3,5,3,6,7]
window = 3
def max_of_subarray(arr, window):
    window_sum = sum(arr[:window]) 
    max_sum = window_sum
    left = 0
    
    for right in range(left+1, len(arr)):
         window_sum = window_sum - arr[left] + arr[right]
         
         max_sum = max(window_sum, max_sum)
         left+=1
         
    return max_sum


print(max_of_subarray(arr, window))
    