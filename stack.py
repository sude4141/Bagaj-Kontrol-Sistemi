# models/stack.py

class BaggageStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack) #kaç adet bagaj (eleman)

    def peek(self):
        return self.stack[-1] if not self.is_empty() else None