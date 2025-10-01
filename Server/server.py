import socket

# Создаем сокет с IPv4, TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# Слушать клиента (1)
server_socket.listen(1)
print(f"Сервер запущен на {server_address}")

while True:
    # Принимаем входящее соединение
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент {client_address}")

    try:
        # Получаем данные от клиента
        data = client_socket.recv(1024) 
        if data:
            print(f"Получено: {data.decode('utf-8')}")
            response = "Привет от сервера!"
            client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close() 