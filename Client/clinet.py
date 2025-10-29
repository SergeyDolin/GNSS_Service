import socket
import struct
import sys
import os


def recv_exactly(sock, n):
    """Читает ровно n байт из сокета. Блокирует, пока не получит все."""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise RuntimeError("Сервер закрыл соединение")
        buf += chunk
    return buf


def send_rinex(host: str, port: int, filepath: str):
    if not os.path.isfile(filepath):
        print(f"Ошибка: файл не найден — {filepath}")
        return

    with open(filepath, 'rb') as f:
        file_data = f.read()
    filename = os.path.basename(filepath)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # --- Отправка файла ---
        s.sendall(struct.pack('>I', len(filename)))      # длина имени (4 байта)
        s.sendall(filename.encode('utf-8'))              # имя файла
        s.sendall(struct.pack('>Q', len(file_data)))     # размер файла (8 байт)
        s.sendall(file_data)                             # содержимое

        # --- Приём ответа ---
        # Читаем первые 4 байта для определения типа ответа
        prefix = recv_exactly(s, 4)

        if prefix == b"OK::":
            # Успех: читаем 8 байт — длину результата
            size_bytes = recv_exactly(s, 8)
            result_size = struct.unpack('>Q', size_bytes)[0]

            # Читаем сам результат (ровно result_size байт)
            result = recv_exactly(s, result_size)

            print("\n=== Результат обработки ===")
            print(result.decode('utf-8'))

        elif prefix.startswith(b"ERR"):  # например, b"ERRO" от "ERROR:..."
            # Дочитываем остаток сообщения об ошибке
            rest = s.recv(1024)
            full_error = (prefix + rest).decode('utf-8', errors='replace')
            print("Сервер вернул ошибку:", full_error)

        else:
            print("Некорректный ответ от сервера:", repr(prefix))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Использование: python client.py <путь_к_файлу.obs>")
        sys.exit(1)
    send_rinex('localhost', 9999, sys.argv[1])
