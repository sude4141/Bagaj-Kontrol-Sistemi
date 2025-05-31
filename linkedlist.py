class Node:
    def __init__(self, data):
        self.data = data #yolcu ıd
        self.next = None

class Blacklist:
    def __init__(self):
        self.head = None

    def add(self, yolcu_id):
        yeni = Node(yolcu_id)
        yeni.next = self.head
        self.head = yeni

    def contains(self, yolcu_id):
        current = self.head
        while current:
            if current.data == yolcu_id:
                return True
            current = current.next
        return False