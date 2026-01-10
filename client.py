# client.py
import sys
import socket
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal, QObject

class MessageSignal(QObject):
    message_received = pyqtSignal(str)

class MessengerClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Чат — Клиент")
        self.setGeometry(100, 100, 550, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите сообщение...")
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_message)

        layout.addWidget(QLabel("Сообщения:"))
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)

        central.setLayout(layout)

        # 🔧 УКАЖИТЕ IP ВАШЕГО КОМПЬЮТЕРА ЗДЕСЬ!
        self.server_host = '10.12.99.161'  # ← ЭТО ВАШ IP ИЗ ipconfig!
        self.server_port = 12345

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.server_host, self.server_port))
            self.local_ip = self.sock.getsockname()[0]
            self.append_message(f"[✅] Подключено к серверу")
            self.append_message(f"[💡] Ваш локальный IP: {self.local_ip}")
        except Exception as e:
            self.append_message(f"[❌] Ошибка подключения: {e}")
            self.local_ip = None
            return

        self.signal = MessageSignal()
        self.signal.message_received.connect(self.process_incoming_message)
        self.listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        self.listen_thread.start()

    def listen_for_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if data:
                    self.signal.message_received.emit(data)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                self.signal.message_received.emit("[❌] Сервер отключён")
                break

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            try:
                self.sock.send(text.encode('utf-8'))
                self.input_field.clear()
            except Exception as e:
                self.append_message(f"[❌] Ошибка отправки: {e}")

    def process_incoming_message(self, raw_msg):
        if raw_msg.startswith('[') and ']: ' in raw_msg:
            ip_part, message = raw_msg[1:].split(']: ', 1)
            if ip_part == self.local_ip or ip_part == '127.0.0.1':
                self.append_message(f"Вы: {message}")
            else:
                self.append_message(f"{raw_msg}")
        else:
            self.append_message(raw_msg)

    def append_message(self, msg):
        self.chat_display.append(msg)

    def closeEvent(self, event):
        self.sock.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessengerClient()
    window.show()
    sys.exit(app.exec())