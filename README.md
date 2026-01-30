# Secure LAN Communicator (P2P) 🔒

A secure, encrypted CLI messenger for local networks. This version features automated key exchange using the **Diffie-Hellman** protocol (X25519), eliminating the need for manual key management.

## 🚀 Features

*   **Perfect Forward Secrecy:** Uses Ephemeral Diffie-Hellman keys. Every session generates a unique encryption key that is never stored.
*   **End-to-End Encryption (E2EE):** All messages are encrypted using **XSalsa20-Poly1305** (via `PyNaCl`).
*   **Zero Configuration Security:** No need to copy secret keys between devices. Just set the IPs and talk.
*   **Real-time Full-Duplex:** Concurrent sending and receiving using Python threads.

## 🛠️ Prerequisites

*   Python 3.6+
*   Two devices on the same LAN (or connected via VPN like WireGuard/Tailscale).

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/lan-communicator.git
    cd lan-communicator
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

Copy the example config and edit it on both machines:
```bash
cp config.json.example config.json
```

**On Computer A:**
```json
{
    "my_ip": "192.168.1.53",
    "target_ip": "192.168.1.44",
    "port": 5005
}
```

**On Computer B:**
```json
{
    "my_ip": "192.168.1.44",
    "target_ip": "192.168.1.53",
    "port": 5005
}
```

## ▶️ Running

Simply run the secure script on both machines:

```bash
python secure_main.py
```

The application will automatically perform a handshake, exchange public keys, and establish a secure tunnel. Once you see `[System] Szyfrowanie ustalone`, you are ready to chat.

## 📜 How it works (Cryptography)

1.  **Identity:** At startup, each instance generates a temporary X25519 Private/Public key pair.
2.  **Handshake:** Upon TCP connection, devices exchange their Public Keys.
3.  **Key Derivation:** Using the Diffie-Hellman algorithm, both sides compute the same **Shared Secret** without ever sending it over the wire.
4.  **Encryption:** Messages are encrypted using this secret. If the program is restarted, new keys are generated, ensuring that even if one session is compromised, others remain secure.

## 📜 License

MIT / Educational Purpose
