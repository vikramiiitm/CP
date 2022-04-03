# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def addTwoNumbers(self, l1, l2):
        c = 0
        dummy = k = ListNode(0)
        while l1 or l2 or c:
            
            if l1:
                c = c + l1.val
                l1 = l1.next
            if l2:
                c = c + l2.val
                l2 = l2.next
                
            k.next = ListNode(c%10)
            k = k.next
            
            c = c//10
            
        return dummy.next
    
