# Hieght of binary tree

class Node:
    def __init__(self,data):
        self.left = None
        self.right = None
        self.data = data
    
class height:
    def Height(self,root):
        temp = root

        if temp is None:
            return 0

        lh = self.Height(temp.left)
        rh = self.Height(temp.right)

        if lh > rh:
            return lh + 1
        else:
            return rh+1

if __name__ == '__main__':
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    h= height()
    k = h.Height(root)
    print("Height of tree is : ",k)