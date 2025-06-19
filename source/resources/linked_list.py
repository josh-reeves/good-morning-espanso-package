class Node:
    data = None
    next = None

    def __init__(self, data):
        self.data = data

class LinkedList:
    head: Node = None
    tail: Node = None

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def __iter__(self):
        return LinkedListIterator(self)
    
    def __add__(self, other):
        result: LinkedList = LinkedList()
        result.appendNode(self.head)
        result.appendNode(other.head)
        
        return result

    def prepend(self, value):
        self.prependNode(Node(value))

        return

    def prependNode(self, node: Node):
        temp: Node = self.head
        self.head = node
        self.head.next = temp

        if (self.tail is None):        
            self.tail = self.head

        while (self.tail.next is not None):
            self.tail = self.tail.next

        return

    def append(self, value):
        self.appendNode(Node(value))

        return

    def appendNode(self, node: Node):
        if (self.head is None):
            self.head = node
            self.tail = self.head

            while (self.tail.next is not None):
                self.tail = self.tail.next
  
            return
        
        if (self.tail is None):
            self.tail = self.head

        while (self.tail.next is not None):
            self.tail = self.tail.next

        self.tail.next = node
        self.tail = self.tail.next

        return

class LinkedListIterator:
    iterator: Node = None

    def __init__(self, list: LinkedList):
        self.iterator = list.head

    def __next__(self):
        if (self.iterator is None):
            raise StopIteration

        item = self.iterator.data
        
        self.iterator = self.iterator.next

        return item
