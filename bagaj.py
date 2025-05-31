import random

temiz_esyalar = ["Laptop", "Kitap", "Su şişesi", "Makas", "Şarj Cihazı", "Parfüm", "Kamera", "Defter", "Tablet"]
tehlikeli_esyalar = ["Bıçak", "Silah", "Patlayıcı", "Çakı", "El Bombası"]

def generate_bagaj():
    bagaj = random.sample(temiz_esyalar, k=random.randint(4, 6))
    if random.random() < 0.1:
        bagaj.append(random.choice(tehlikeli_esyalar))
    random.shuffle(bagaj)
    return bagaj
