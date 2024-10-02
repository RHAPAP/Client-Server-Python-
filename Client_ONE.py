import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Получено сообщение: {data}')
        except:
            print('Соединение с сервером прервано')
            break

def send_message(conn, name):
    while True:
        message = input()
        conn.sendall(message.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    name = input('Введите имя: ')
    s.sendall(name.encode())

    thread_receive = threading.Thread(target=receive_messages, args=(s,))
    thread_send = threading.Thread(target=send_message, args=(s, name))

    thread_receive.start()
    thread_send.start()

    thread_receive.join()
    thread_send.join()
