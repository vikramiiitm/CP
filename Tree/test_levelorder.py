
from collections import deque
class Node:
    def __init__(self,data):
        self.data = data
        self.prev = None
        self.next = None

class Levelorder:
    def __init__(self,root):
        self.root = root


    def level(self):
        temp = self.root
        if not temp:
            return

        q = deque()
        q.append(temp)

        while q:
            c = len(q)
            while c>0:
                temp =q.popleft()
                print(temp.data,end = " ")

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

    traverse = Levelorder(root)
    traverse.level()



