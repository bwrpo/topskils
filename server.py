# server.py
import socket
import threading

HOST = '0.0.0.0'  # слушать все интерфейсы
PORT = 12345

clients = []

def broadcast(msg, sender_conn):
    for conn, addr in clients[:]:  # копия списка
        if conn != sender_conn:
            try:
                conn.send(msg.encode('utf-8'))
            except:
                try:
                    conn.close()
                except:
                    pass
                if (conn, addr) in clients:
                    clients.remove((conn, addr))
                    print(f"[-] Клиент {addr} удалён из-за ошибки")

def handle_client(conn, addr):
    ip, port = addr
    print(f"[+] Новый клиент: {ip}:{port}")
    clients.append((conn, addr))
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            formatted = f"[{ip}]: {data}"
            print(formatted)
            broadcast(formatted, conn)
    except Exception as e:
        print(f"[-] Ошибка у {ip}:{port} — {e}")
    finally:
        conn.close()
        for c, a in clients[:]:
            if c == conn:
                clients.remove((c, a))
                break
        print(f"[-] Клиент {ip}:{port} отключился")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[✅] Сервер запущен на {HOST}:{PORT}")
        print(f"[💡] Другие устройства должны подключаться к: {get_local_ip()}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    start_server()