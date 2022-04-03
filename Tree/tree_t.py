from  collections import deque
class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

def inorder(temp):
    if not temp:
        return
    inorder(temp.left)
    print(temp.val,end=" ")
    inorder(temp.right)

def levelorder(temp):
    if not temp:
        return
    p = deque()

    p.append(temp)

    while len(p):
        c = len(p)
        while c>0:
            temp = p.popleft()
            print(temp.val, end=" ")

            if temp.left:
                p.append(temp.left)
            if temp.right:
                p.append(temp.right)
            c-=1
        print()

def insert(temp,key):
    if not temp:
        temp = Node(temp)
        return

    q = deque()
    q.append(temp)

    while len(q):
        temp = q.popleft()
        
        # if left is empty insert the node with value  = key
        if not temp.left:
            temp.left = Node(key)
            break
        else:
            q.append(temp.left)
        if not temp.right:
            temp.right = Node(key)
            break
        else:
            q.append(temp.right)


if __name__ == '__main__':
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
    insert(root,7)
    print()
    inorder(root)

    print()
    levelorder(root)
