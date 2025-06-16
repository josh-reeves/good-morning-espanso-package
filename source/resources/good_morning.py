import random
import datetime
import os
import subprocess
import json

# region Dependency Definitions
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

        self.tail = self.head

        return

    def append(self, value):
        self.appendNode(Node(value))

        return

    def appendNode(self, node: Node):
        if (self.head is None):
            self.head = node
            self.tail = self.head
  
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
    
# endregion

# region Main Program
tagChar: str = ':'

tagged: LinkedList = LinkedList()
shuffle: LinkedList = LinkedList()

personalGreetings = list()
generalGreetings = list()
mondayGreetings = list()
fridayGreetings = list()

# Uses GitHub API to pull list of images in gif directory of repository. This can be used to dynamically obtain the total number of 
# images in the directory later:
gifList = json.loads(subprocess.run(["curl", "https://api.github.com/repos/josh-reeves/good-morning-espanso-package/contents/images", "-s"], capture_output=True).stdout.decode())

# For each name in the names file, check to see if the name includes tagChr. If the name is tagged, add it to the tagged list in the 
# order it appears in the original file. Otherwise, either append or prepend the name to the shuffle list depending on whether a 
# random value between 0 and 99 is even or odd. This builds the list in a semi-random order and prevents the need to shuffle the 
# values later on:
for name in open(file=os.path.join(os.path.dirname(__file__), "names.txt"), encoding="utf-8-sig"):
    if (name.__contains__(tagChar)):
        tagged.append(name[name.index(tagChar)+ 1:].rstrip())
    elif (random.randint(0, 99) % 2 == 0):
        shuffle.append(name.rstrip())
    else:
        shuffle.prepend(name.rstrip())

for greeting in open(file=os.path.join(os.path.dirname(__file__), "personalGreetings.txt"), encoding="utf-8-sig"):
    personalGreetings.append(greeting.rstrip())

for greeting in open(file=os.path.join(os.path.dirname(__file__), "generalGreetings.txt"), encoding="utf-8-sig"):
    generalGreetings.append(greeting.rstrip())

for greeting in open(file=os.path.join(os.path.dirname(__file__), "mondayGreetings.txt"), encoding="utf-8-sig"):
    mondayGreetings.append(greeting.rstrip())

for greeting in open (file=os.path.join(os.path.dirname(__file__), "fridayGreetings.txt"), encoding="utf-8-sig"):
    fridayGreetings.append(greeting.rstrip())

for name in (tagged + shuffle):
    print(f"{personalGreetings[random.randint(0, personalGreetings.__len__() - 1)]} {name}!")

if (datetime.date.today().weekday() == 0):
    print(f"\n{mondayGreetings[random.randint(0, mondayGreetings.__len__() - 1)]}")
elif (datetime.date.today().weekday() == 4):
    print(f"\n{fridayGreetings[random.randint(0, fridayGreetings.__len__() - 1)]}")    
else:
    print(f"\n{generalGreetings[0]}")

# Attempt to curl a random gif from the gif directory
subprocess.run(["curl", f"https://raw.githubusercontent.com/josh-reeves/good-morning-espanso-package/refs/heads/main/images/{random.randint(1, gifList.__len__())}.gif", "-s", "-o", os.path.join(os.path.dirname(__file__), "tmp.gif")])

# endregion