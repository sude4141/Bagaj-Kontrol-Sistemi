from collections import deque

class PassengerQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, passenger):
        self.queue.append(passenger)

    def dequeue(self):
        return self.queue.popleft() if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0