# Secure LAN Communicator 🔒

A secure, encrypted command-line interface (CLI) messenger application written in Python. It allows two computers on the same Local Area Network (LAN) to exchange messages in real-time using TCP sockets, with end-to-end encryption provided by `PyNaCl` (libsodium).

## 🚀 Features

*   **End-to-End Encryption:** Messages are encrypted using **XSalsa20-Poly1305** (via `PyNaCl`), ensuring confidentiality and integrity.
*   **Real-time Communication:** Uses separate threads for sending and receiving messages simultaneously.
*   **Robust Connection Handling:** Automatically attempts to reconnect if the target machine is unreachable.
*   **Secure Configuration:** Keys and IPs are stored in a local JSON file (ignored by git).
*   **Clean Interface:** Simple terminal-based UI.

## 🛠️ Prerequisites

*   Python 3.6 or higher
*   Two computers connected to the same local network (Wi-Fi or Ethernet)

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/lan-communicator.git
    cd lan-communicator
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # or
    venv\Scripts\activate     # Windows
    ```

3.  Install the required dependencies:
    ```bash
    pip install pynacl
    ```

## ⚙️ Configuration

Before running the application, you need to set up the configuration and encryption keys.

### 1. Generate a Secret Key
Since this communicator uses symmetric encryption, **both devices must share the exact same key**.

Run the helper script to generate a new key:
```bash
python gen_key.py
```
The key will be printed to the terminal and saved in a file named `secret.key`. Copy this Base64 string.

### 2. Create `config.json`
Copy the example configuration file:
```bash
cp config.json.example config.json
```

Edit `config.json` on **BOTH** computers:

**On Computer A:**
```json
{
    "my_ip": "192.168.1.53",
    "target_ip": "192.168.1.44",
    "port": 5005,
    "secret_key": "PASTE_THE_KEY_FROM_SECRET_KEY_FILE"
}
```

**On Computer B:**
```json
{
    "my_ip": "192.168.1.44",
    "target_ip": "192.168.1.53",
    "port": 5005,
    "secret_key": "PASTE_THE_SAME_KEY_HERE"
}
```

> **Note:** The `secret_key` and `port` must be identical on both machines.

## ▶️ How to Run

1.  Ensure your virtual environment is active.
2.  Run the main script:

```bash
python secure_main.py
```

3.  Wait for the connection. Once both clients are running and the keys match, you can start typing messages!
4.  Type `exit` to close the connection and quit the program.

## 🧠 Encryption Details

This application uses the `PyNaCl` library (Python binding to `libsodium`).
*   **Algorithm:** XSalsa20 stream cipher for encryption + Poly1305 MAC for authentication.
*   **Security:** This ensures that messages cannot be read by third parties (confidentiality) and cannot be modified in transit without detection (integrity).

## 📜 License

This project is open-source and available for educational purposes.