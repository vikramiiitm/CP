from collections import deque
class Node:
    def __init__(self,val):
        self.next = None
        self.prev = None
        self.val = val

class InOrder:
    def __init__(self,root):
        self.root = root
    

    def inordertraversal(self):
        temp = self.root
        if not temp:
            print("h")
            return
        q = deque()
        q.append(temp)
        while q:
            # c is number of elements in level
            c = len(q)
            while c>0:
                k = q.popleft()
                print(k.val,end=" ")
                
                if temp.prev:
                    q.append(temp.prev)
                if temp.next:
                    q.append(temp.next)
                
                c = c-1
                
            print()

if __name__ == '__main__':
    root = Node(5)
    root.next = Node(11)
    root.next.next = Node(7)
    root.prev = Node(9)
    root.prev.next = Node(15)
    root.prev.prev = Node(8)

    inorder = InOrder(root)
    inorder.inordertraversal()

