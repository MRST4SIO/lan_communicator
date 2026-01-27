import threading
import time


def parz_kawe():
    print("Zaczynam parzyć kawę...")
    time.sleep(3)  # Symulacja czekania (I/O)
    print("Kawa gotowa!")

def smaz_jajka():
    print("Zaczynam smażyć jajka...")
    time.sleep(2)  # Symulacja czekania (I/O)
    print("Jajka gotowe!")


thread1 = threading.Thread(target=parz_kawe)
thread2 = threading.Thread(target=smaz_jajka)

thread1.start()
thread2.start()

thread1.join()
thread2.join()


