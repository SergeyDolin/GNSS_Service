import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8888)
client_socket.connect(server_address)

try:
    message = "Привет, сервер!"
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024)
    print(f"Получен ответ от сервера {data.decode('utf-8')}")
finally:
    client_socket.close()