import socket
import threading
import time
import json
import base64
from nacl.secret import SecretBox
from nacl.exceptions import CryptoError

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
HOST = config['my_ip']
CLIENT = config['target_ip']
PORT = config['port']
KEY_B64 = config['secret_key']

key = base64.b64decode(KEY_B64)
box = SecretBox(key)

def encrypt_message(msg_str):
  encrypted = box.encrypt(msg_str.encode('utf-8'))
  return encrypted

def decrypt_message(encrypted_bytes):
  try:
    plaintext = box.decrypt(encrypted_bytes)
    return plaintext.decode('utf-8')
  except CryptoError:
    return None



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
            message = decrypt_message(data)
            if message is None:
              print("[Błąd] Nie udało się zweryfikować lub odszyfrować wiadomości.")
              continue
            print(f"Otrzymano: \"{message}\" od {addr}")
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
        encrypted_message = encrypt_message(message)
        s.send(encrypted_message)
      except (BrokenPipeError, ConnectionResetError):
        print("\n[Błąd] Nie można wysłać wiadomości. Połączenie zerwane.")
        break




server_thread = threading.Thread(target=recieve, daemon=True)
client_thread = threading.Thread(target=send)

server_thread.start()
client_thread.start()

client_thread.join()
