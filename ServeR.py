import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = {}

def handle_client(conn, addr):
    global clients
    name = conn.recv(1024).decode()
    clients[addr] = (conn, name)
    print(f'Клиент {name} ({addr}) подключился к серверу')

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Сообщение от {name}: {data}')
            for client in clients.values():
                if client != (conn, name):
                    client[0].sendall(f'{name}: {data}'.encode())
        except:
            print(f'Клиент {name} ({addr}) отключился')
            del clients[addr]
            conn.close()
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Сервер запущен на {HOST}:{PORT}')

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
