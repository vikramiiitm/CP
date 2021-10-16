from collections import deque
class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key
        
def inorder(temp):
    if not temp:
        return

    q = deque()

    q.append(temp)
    while q:
        # c denotes size of q for the level
        c = len(q)
        while c>0:
            temp = q.popleft()
            print(temp.val, end=' ')

            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
            c-=1
        print(' ')


root = Node(10)

"""   1 
    /   \
   None None """

root.left = Node(11)
root.left.left = Node(7)
root.right = Node(9)

root.right.left = Node(15)
root.right.right = Node(8)

# levelorder(root)
inorder(root)