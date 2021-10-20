"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.
"""

class Solution:
    def twoSum(self, nums, target):
        for index,val in enumerate(nums):
            nums[index] = None
            if target-val in nums[index:]:
                print([index,nums.index(target-val)])
        
s = Solution() 
nums = [3,3]
s.twoSum(nums,6)       
                
        