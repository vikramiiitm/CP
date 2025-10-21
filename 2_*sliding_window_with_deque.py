'''
You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right.
You can only see the k numbers in the window. Each time the sliding window moves right by one position.
https://www.youtube.com/watch?v=NwBvene4Imo
'''
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        dq = deque()  # store indices
        ans = []

        for right in range(len(nums)):
            # Remove smaller numbers from the back
            while dq and nums[dq[-1]] < nums[right]:
                dq.pop()

            # Add current index
            dq.append(right)

            # Remove leftmost index if it’s out of window
            if dq[0] <= right - k:
                dq.popleft()

            # Add to result once the first window is ready
            if right >= k - 1:
                ans.append(nums[dq[0]])

        return ans
    
    
    
'''
Intuition
I originally wrote two solutions that has the correct logic, but they run in O(n*k), so they wouldn't pass, which I find annoying.

Approach
We use sliding window with deque to solve this problem. The pure sliding window logic of this problem is not very difficult to me, but using deque is where threw me off a bit.

We need to keep our deque in a descending order, so dq[0] is the greatest, and dq[-1] should be the smallest. We start each iterations with cleaning up the deque, if the smallest is smaller than the current element nums[right], we pop() it.
Then we add in the new index; remember, deque is used for keeping track of indices, not values.

Then, as long as dq is valid, we check if the largest in the deque is outside of the window, if it is, we remove it. Then in the end, we check if we have a valid sized window, and append the greatest element in the deque.
'''
