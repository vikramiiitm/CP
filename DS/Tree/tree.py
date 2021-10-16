# Insert element at first level empty node

from collections import deque
class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

def inorder(temp):
    if not temp:
        return
    
    inorder(temp.left)
    print(temp.val, end=" ")
    inorder(temp.right)

def insert(temp,key):
    if not temp:
        temp = Node(temp)
        return
    
    q = deque()
    # temp is reference of root node
    q.append(temp)
    
    while len(q):
        # we pop the first element add it's children to q
        temp = q.popleft()
        
        # temp is address of node
        # print("temp : ",temp)

        # if left child is absent attch key here
        if not temp.left:
            temp.left = Node(key)
            break
        else: # else add child of left node to queue
            q.append(temp.left)

        if not temp.right:
            temp.right = Node(key)
            break
        else:
            q.append(temp.right)


# root node
root = Node(10)

"""   1 
    /   \
   None None """

root.left = Node(11)
root.left.left = Node(7)
root.right = Node(9)

root.right.left = Node(15)
root.right.right = Node(8)

inorder(root)
print()
insert(root,12)
inorder(root)
