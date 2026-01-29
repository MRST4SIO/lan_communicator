import base64
from nacl.secret import SecretBox
import nacl.utils

def generate_key():
  key = nacl.utils.random(SecretBox.KEY_SIZE)

  key_b64 = base64.b64encode(key).decode('utf-8')

  print(key_b64)
  with open("secret.key", "w") as key_file:
    key_file.write(key_b64)

if __name__ == "__main__":
  generate_key()