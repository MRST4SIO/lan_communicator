import socket
import threading
import time
import json
from nacl.exceptions import CryptoError
from nacl.public import Box, PrivateKey, PublicKey

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
HOST = config['my_ip']
CLIENT = config['target_ip']
PORT = config['port']

private_key = PrivateKey.generate()
public_key = private_key.public_key


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
        try:
          raw_client_pub = conn.recv(32)
          conn.send(public_key.encode())
          client_public_key = PublicKey(raw_client_pub)
          session_box = Box(private_key, client_public_key)
          print("[System] Szyfrowanie ustalone.")
        except Exception as e:
          print("[Błąd Handshake] {e}")
          continue
        while True:
          try:
            data = conn.recv(1024)
            if not data:
              print("\n[Rozłączono] Druga strona zamknęła połączenie.")
              break
            message = session_box.decrypt(data).decode("utf-8")
            print(f"Otrzymano: \"{message}\" od {addr}")
            print("Ty: ", end="", flush=True)
          except CryptoError:
            print("[Błąd] Nie udało się zweryfikować lub odszyfrować wiadomości.")
            continue
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
        s.send(public_key.encode())
        raw_client_pub = s.recv(32)
        client_public_key = PublicKey(raw_client_pub)
        session_box = Box(private_key, client_public_key)
        print("[System] Szyfrowanie ustalone.")
        
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
        encrypted_message = session_box.encrypt(message.encode("utf-8"))
        s.send(encrypted_message)
      except (BrokenPipeError, ConnectionResetError):
        print("\n[Błąd] Nie można wysłać wiadomości. Połączenie zerwane.")
        break


server_thread = threading.Thread(target=recieve, daemon=True)
client_thread = threading.Thread(target=send)

server_thread.start()
client_thread.start()

client_thread.join()
