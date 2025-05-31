import random
from models.bagaj import generate_bagaj

class Passenger:
    def __init__(self, sira, yolcu_id=None):
        self.queue_number = f"Yolcu #{sira}"
        self.id = yolcu_id if yolcu_id else self._generate_id()
        self.bagaj = generate_bagaj()

    def _generate_id(self):
        return str(random.randint(10000, 99999))

    def __str__(self):
        return f"{self.queue_number} - ID: {self.id}"
