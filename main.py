import socket
import threading
import time
import json
import os

# Wczytywanie konfiguracji
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
HOST = config['my_ip']
CLIENT = config['target_ip']
PORT = config['port']


def recieve():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[Serwer] Nasłuchuję na {HOST}:{PORT}...")

    
    while True:
      conn, addr = s.accept()
      with conn:
        print(f"\n[Połączono] Ktoś wszedł z adresu: {addr}")
        while True:
          try:
            data = conn.recv(1024)
            if not data:
              print("\n[Rozłączono] Druga strona zamknęła połączenie.")
              break
            print(f"Otrzymano: \"{data.decode('utf-8')}\" od {addr}")
            print("Ty: ", end="", flush=True)
          except ConnectionResetError:
            print("\n[Błąd] Połączenie zerwane nagle.")
            break

def send():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"[Klient] Próbuję połączyć się z {CLIENT}...")
    connected = False
    while not connected:
      try:
        s.connect((CLIENT, PORT))
        connected = True
        print(f"[Klient] Sukces! Połączono z {CLIENT}")
      except ConnectionRefusedError:
        print(".", end="", flush=True)
        time.sleep(2)
      except OSError as e:
        print(f"\n[Błąd sieci] {e}")
        time.sleep(2)

    while True:
      try:      
        message = input("Ty: ")
        if(message.lower() == 'exit'):
          break
        s.send(message.encode("utf-8"))
      except (BrokenPipeError, ConnectionResetError):
        print("\n[Błąd] Nie można wysłać wiadomości. Połączenie zerwane.")
        break




server_thread = threading.Thread(target=recieve, daemon=True)
client_thread = threading.Thread(target=send)

server_thread.start()
client_thread.start()

client_thread.join()
