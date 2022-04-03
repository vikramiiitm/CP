class Node:
    def __init__(self,data):
        self.next = None
        self.data = data
    
class linkedlist:

    def __init__(self):
        self.head = None

    # FRONT:new node added at front of head, new node becomes head
    def addfront(self,data):
        # create new node
        new_node = Node(data)
        # store the ref of list attached to head
        new_node.next = self.head
        # store the addres of new node in head making first element
        self.head = new_node

    def addEnd(self,data):

        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        last = self.head
        # traverse last node
        while last.next:
            last = last.next
        # assign new node at last
        last.next = new_node

    def traverse(self):
        if self.head is None:
            print("Linked list empty")
            return
        else:
            temp = self.head

            while temp:
                print(temp.data,end=" -> ")
                temp = temp.next
        print()

    def delFront(self):
        if self.head is None:
            print("LL is empty")
        else:
            temp = self.head
            temp = temp.next
            self.head = temp

        print()

if __name__ == '__main__':

    # start with empty linkedlist
    ll = linkedlist()

    ll.addfront(1)
    ll.addfront(2)
    ll.addfront(3)
    ll.addfront(4)
    ll.addfront(5)
    ll.addEnd(6)
    ll.addEnd(7)
    ll.traverse()
    ll.delFront()
    ll.traverse()
    
