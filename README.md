# CLI LAN Communicator 💬

A simple, robust command-line interface (CLI) messenger application written in pure Python. It allows two computers on the same Local Area Network (LAN) to exchange messages in real-time using TCP sockets and multi-threading.

## 🚀 Features

*   **Real-time Communication:** Uses separate threads for sending and receiving messages simultaneously.
*   **Robust Connection Handling:** Automatically attempts to reconnect if the target machine is unreachable.
*   **Zero Dependencies:** Built using only Python's standard libraries (`socket`, `threading`, `json`).
*   **JSON Configuration:** Easy-to-edit configuration file for network setup.
*   **Clean Interface:** Simple terminal-based UI.

## 🛠️ Prerequisites

*   Python 3.6 or higher
*   Two computers connected to the same local network (Wi-Fi or Ethernet)

## ⚙️ Configuration

Before running the application, you need to configure the IP addresses in `config.json`.

1.  **Check your IP Address:**
    *   Windows: `ipconfig` (look for IPv4 Address)
    *   Linux/Mac: `ip a` or `ifconfig`

2.  **Edit `config.json`:**

**On Computer A:**
```json
{
    "my_ip": "192.168.1.53",      <-- IP of Computer A
    "target_ip": "192.168.1.44",  <-- IP of Computer B
    "port": 5005
}
```

**On Computer B:**
```json
{
    "my_ip": "192.168.1.44",      <-- IP of Computer B
    "target_ip": "192.168.1.53",  <-- IP of Computer A
    "port": 5005
}
```

> **Note:** The `port` must be the same on both machines.

## ▶️ How to Run

1.  Clone the repository or download the files.
2.  Navigate to the project directory.
3.  Run the script:

```bash
python main.py
```

4.  Wait for the connection. Once both clients are running, you can start typing messages!
5.  Type `exit` to close the connection and quit the program.

## 🧠 How it Works

The application uses a **Peer-to-Peer (P2P)** architecture simulated with a client-server model:

*   **Receiver Thread:** Acts as a server. It binds to `my_ip` and listens for incoming connections. When data arrives, it prints it to the console.
*   **Sender Thread:** Acts as a client. It constantly tries to connect to `target_ip`. Once connected, it waits for user input and sends messages.

This split architecture allows you to type and receive messages at the same time without blocking the program.

## 📜 License

This project is open-source and available for educational purposes.
