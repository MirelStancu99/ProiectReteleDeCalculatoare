import socket
import os

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def publish(self, filename):
        self.socket.send("publish".encode())
        self.socket.send(filename.encode())
        filesize = os.path.getsize(filename)
        self.socket.send(str(filesize).encode())
        with open(filename, "rb") as f:
            filedata = f.read()
            total_sent = 0
            while total_sent < len(filedata):
                sent = self.socket.send(filedata[total_sent:])
                if sent == 0:
                    raise RuntimeError("Trimiterea datelor a eșuat.")
                total_sent += sent
        response = self.socket.recv(1024).decode()
        print(response)


    def list_files(self):
        self.socket.sendall("list".encode())
        print("Sent list command to server.")
        filelist = b""
        while True:
            data = self.socket.recv(4096)
            if not data:
                break
            filelist += data
            if filelist.endswith(b"<END>"):
                break
        filelist = filelist.rstrip(b"<END>")
        print("Received data from server:")
        print(filelist.decode())








    def download(self, filename):
        self.socket.sendall("download".encode())
        self.socket.sendall(filename.encode())
        filedata = self.socket.recv(4096)
        if filedata.startswith(b"Fisierul"):
            print(filedata.decode())
        else:
            with open(filename, "wb") as f:
                f.write(filedata)
            print(f"Fisierul {filename} a fost descarcat cu succes!")


    def read(self, filename):
        self.socket.sendall("read".encode())
        self.socket.sendall(filename.encode())
        filedata = self.socket.recv(4096)
        if filedata.startswith("Fisierul".encode()):
            print(filedata.decode())
        else:
            print(f"Continutul fisierului {filename}:\n{filedata.decode()}")

    def show_directories(self):
        self.socket.sendall("showDirectories".encode())
        print("Sent showDirectories command to server.")
        directory_list = b""
        while True:
            data = self.socket.recv(4096)
            if not data:
                break
            directory_list += data
            if directory_list.endswith(b"<END>"):
                break
        directory_list = directory_list.rstrip(b"<END>")
        print("Received data from server:")
        print(directory_list.decode())



    def exit(self):
        self.socket.sendall("exit".encode())
        response = self.socket.recv(1024).decode()
        print(response)
        self.socket.close()
        print("Deconectat de la server.")

if __name__ == '__main__':
    host = 'localhost'  # Adresa IP a serverului sau un alt host
    port = 5000  # Portul serverului

    client = Client(host, port)

    while True:
        print("\nComenzi disponibile:")
        print("1. publish")
        print("2. list")
        print("3. download")
        print("4. read")
        print("5. showDirectories")
        print("6. exit")

        command = input("\nIntroduceti o comanda: ")
        if command == 'publish':
            filename = input("Introduceti numele fisierului pentru publicare: ")
            client.publish(filename)
        elif command == 'list':
            client.list_files()
        elif command == 'download':
            filename = input("Introduceti numele fisierului pentru descarcare: ")
            client.download(filename)
        elif command == 'read':
            filename = input("Introduceti numele fisierului pentru citire: ")
            client.read(filename)
        elif command == 'showDirectories':
            client.show_directories()
        elif command == 'exit':
            client.exit()
            break
        else:
            print("Comanda invalida. Va rugam incercati din nou.")
