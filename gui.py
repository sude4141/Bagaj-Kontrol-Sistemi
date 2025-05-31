import pygame
import tkinter as tk
from tkinter import messagebox,Scrollbar,Canvas,Frame
from models.stack import BaggageStack
from models.yolcu import Passenger
from models.queue import PassengerQueue
from models.linkedlist import Blacklist
from utils.olasilik import esya_tehlikeli_mi

# === GUI Global ===
yolcu_kuyrugu_gui = PassengerQueue()
kara_liste_gui = Blacklist()
kara_liste_idler = ["42354", "23071", "69532"]

for kid in kara_liste_idler:
    kara_liste_gui.add(kid)

yolcu_sayaci = 1
toplam_yolcu = 0
kara_liste_yolcu = 0
temiz_yolcu = 0
alarm_sayisi = 0

def log_yaz(mesaj):
    log_text.config(state='normal')
    log_text.insert(tk.END, mesaj + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')


def yolcu_olustur():
    global yolcu_sayaci, toplam_yolcu
    yolcu = Passenger(sira=yolcu_sayaci)
    yolcu_sayaci += 1
    toplam_yolcu += 1
    yolcu_kuyrugu_gui.enqueue(yolcu)
    queue_listbox.insert(tk.END, str(yolcu))
    log_yaz(f"✈ {yolcu.queue_number} kuyruğa eklendi. (ID: {yolcu.id})")


def rastgele_yolcu_ekle():
    from random import randint
    yolcu = Passenger(randint(100, 999))
    global toplam_yolcu
    toplam_yolcu += 1
    yolcu_kuyrugu_gui.enqueue(yolcu)
    queue_listbox.insert(tk.END, str(yolcu))
    log_yaz(f"🎲 Rastgele yolcu eklendi: {yolcu.queue_number} (ID: {yolcu.id})")


def manuel_yolcu_ekle_penceresi():
    pencere = tk.Toplevel()
    pencere.title("Manuel Yolcu Ekle")
    pencere.geometry("400x300")

    tk.Label(pencere, text="Yolcu ID'si (boş kalırsa rastgele verir):").pack(pady=5)
    id_entry = tk.Entry(pencere, width=25)
    id_entry.pack()

    tk.Label(pencere, text="Eşyaları girin").pack(pady=5)
    esya_entry = tk.Entry(pencere, width=40)
    esya_entry.pack()

    def ekle():
        global yolcu_sayaci, toplam_yolcu
        yolcu_id = id_entry.get().strip()
        esya_metni = esya_entry.get().strip()

        # Eğer ID girilmişse, aynı ID kuyrukta var mı kontrol et
        if yolcu_id:
            for yolcu in yolcu_kuyrugu_gui.queue:
                if yolcu.id == yolcu_id:
                    log_yaz(f"⚠ Bu ID'ye sahip yolcu mevcut: {yolcu_id}")
                    pencere.destroy()
                    return
        else:
            yolcu_id = None  # Random üretilecek

        # Eşyaları hazırla
        if esya_metni:
            esyalar = [e.strip() for e in esya_metni.split(",")]
        else:
            from models.bagaj import generate_bagaj
            esyalar = generate_bagaj()

        from models.yolcu import Passenger
        yolcu = Passenger(sira=yolcu_sayaci, yolcu_id=yolcu_id)
        yolcu.bagaj = esyalar

        yolcu_sayaci += 1
        toplam_yolcu += 1
        yolcu_kuyrugu_gui.enqueue(yolcu)
        queue_listbox.insert(tk.END, str(yolcu))
        log_yaz(f"📝 Manuel yolcu eklendi: {yolcu.queue_number} (ID: {yolcu.id})")
        pencere.destroy()

    tk.Button(pencere, text="Ekle", command=ekle).pack(pady=10)



def bagaj_tarama(yolcu):
    tehlike = False
    stack_listbox.delete(0, tk.END)
    log_yaz(f"{yolcu.queue_number} - Bagaj kontrolü başlıyor...")

    stack = BaggageStack()

    for esya in yolcu.bagaj:
        stack.push(esya)

    while not stack.is_empty():
        esya = stack.pop()
        stack_listbox.insert(0, esya)
        if esya_tehlikeli_mi(esya):
            stack_listbox.itemconfig(0, {'bg': 'red', 'fg': 'white'})
            log_yaz(f"⚠ TEHLİKELİ EŞYA: {esya}")
            tehlike = True
        else:
            log_yaz(f"   – {esya} (Güvenli)")

    return tehlike



def simulasyonu_baslat():
    global alarm_sayisi, kara_liste_yolcu, temiz_yolcu
    if yolcu_kuyrugu_gui.is_empty():
        messagebox.showwarning("Uyarı", "Kuyrukta yolcu yok!")
        return
    yolcu = yolcu_kuyrugu_gui.dequeue()
    queue_listbox.delete(0)
    log_yaz(f"\n➡ {yolcu.queue_number} ({yolcu.id}) kontrol ediliyor...")

    if kara_liste_gui.contains(yolcu.id):
        kara_liste_yolcu += 1
        log_yaz(f"🚫 {yolcu.queue_number} (ID: {yolcu.id}) → Kara liste uyarısı!")
        log_yaz(f"🔥 {yolcu.queue_number} → YÜKSEK RİSK")

    tehlike = bagaj_tarama(yolcu)

    if tehlike:
        alarm_sayisi += 1
        log_yaz(f"⚠ {yolcu.queue_number} – TEHLİKELİ EŞYA TESPİT EDİLDİ!")
        log_yaz(f"{yolcu.queue_number} → Alarm verildi 🚨")

        if not kara_liste_gui.contains(yolcu.id):  # Önceden yoksa sayaç artır
            kara_liste_yolcu += 1
            kara_liste_gui.add(yolcu.id)
            kara_liste_listbox.insert(0, f"ID: {yolcu.id} → {yolcu.queue_number}")
            log_yaz(f"{yolcu.queue_number} → Kara listeye eklendi!")

    elif not kara_liste_gui.contains(yolcu.id):
        temiz_yolcu += 1
        log_yaz(f"✅ {yolcu.queue_number} → Temiz, geçiş izni verildi.")
    log_yaz("=" * 60)


def hazir_veri_yukle():
    for _ in range(30):
        yolcu_olustur()
    log_yaz("✅ 30 yolcu başarıyla yüklendi.")


def rapor_goster():
    messagebox.showinfo("Rapor", f"""📊 Gün Sonu Raporu
Toplam Yolcu: {toplam_yolcu}
Kara Liste Yolcu: {kara_liste_yolcu}
Temiz Yolcu: {temiz_yolcu}
🚨 Alarm Sayısı: {alarm_sayisi}""")


def baslat_gui():
    global log_text, queue_listbox, stack_listbox, kara_liste_listbox
    pygame.mixer.init()
    pygame.mixer.music.load("ucus_sesi.wav")
    pygame.mixer.music.play()

    pencere = tk.Tk()
    pencere.title("Turkish Airlines")
    pencere.geometry("850x750")

    canvas = Canvas(pencere)
    scrollbar = Scrollbar(pencere, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="Yolcu Kuyruğu", font=("Arial", 12, "bold")).pack(pady=5)
    queue_listbox = tk.Listbox(scrollable_frame, width=80, height=8, relief="solid", bd=2)

    queue_listbox.pack()

    button_frame = tk.Frame(scrollable_frame)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="New Passenger", command=yolcu_olustur).pack(side="left", padx=5)
    tk.Button(button_frame, text="Random Passenger", command=rastgele_yolcu_ekle).pack(side="left", padx=5)
    tk.Button(button_frame, text="Load 30 Passengers", command=hazir_veri_yukle).pack(side="left", padx=5)
    tk.Button(button_frame, text="Manuel Yolcu Ekle", command=manuel_yolcu_ekle_penceresi).pack(side="left", padx=5)

    # Başlıklar
    tk.Label(scrollable_frame, text="Bagaj Kontrol ve Kara Liste", font=("Arial", 12, "bold")).pack(pady=5)

    # Ortak çerçeve içine al
    yan_frame = tk.Frame(scrollable_frame)
    yan_frame.pack(pady=5)

    # Stack (Bagaj kontrol) kutusu
    stack_frame = tk.Frame(yan_frame)
    stack_frame.pack(side="left", padx=10)
    tk.Label(stack_frame, text="Stack - Bagaj Kontrol").pack()
    stack_listbox = tk.Listbox(stack_frame, width=40, height=6, relief="solid", bd=2)
    stack_listbox.pack()

    # Kara Liste kutusu
    kara_liste_frame = tk.Frame(yan_frame)
    kara_liste_frame.pack(side="left", padx=10)
    tk.Label(kara_liste_frame, text="Kara Liste").pack()
    kara_liste_listbox = tk.Listbox(kara_liste_frame, width=40, height=6, relief="solid", bd=2)
    kara_liste_listbox.pack()

    for kid in kara_liste_idler:
        kara_liste_listbox.insert(tk.END, f"ID: {kid}")

    kontrol_frame = tk.Frame(scrollable_frame)
    kontrol_frame.pack(pady=5)
    tk.Button(kontrol_frame, text="Start Simulation", command=simulasyonu_baslat).pack(side="left", padx=10)
    tk.Button(kontrol_frame, text="Generate Report", command=rapor_goster).pack(side="left", padx=10)

    tk.Label(scrollable_frame, text="Log Paneli", font=("Arial", 12, "bold")).pack(pady=5)

    log_frame = tk.Frame(scrollable_frame, relief="solid", bd=2)
    log_frame.pack(pady=5)

    log_text = tk.Text(log_frame, height=15, width=100, state='disabled', bg="white")
    log_text.pack()

    pencere.mainloop()