from nacl.public import PrivateKey, PublicKey, Box
import base64

alice_private = PrivateKey.generate()
alice_public = alice_private.public_key



bob_private = PrivateKey.generate()
bob_public = bob_private.public_key


alice_box = Box(alice_private, bob_public)

bob_box = Box(bob_private, alice_public)

message = b"Tajne haslo do wifi"

encrypted = alice_box.encrypt(message)

try:
  decrypted = bob_box.decrypt(encrypted)
  if message == decrypted:
    print(message, decrypted)
except Exception as e:
  print("Błąd")