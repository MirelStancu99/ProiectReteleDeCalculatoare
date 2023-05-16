import socket
import threading
import os

class Server:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.clients = {} # dictionar cu clientii conectati

    def listen(self):
        self.socket.listen(5)
        print(f"Serverul asculta pe portul {self.port}...")
        while True:
            conn, addr = self.socket.accept()
            print(f"S-a conectat un client nou: {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                if command == 'publish':
                    # publica un fisier
                    filename = conn.recv(1024).decode().strip()
                    filesize = conn.recv(1024).decode().strip()
                    filedata = conn.recv(int(filesize))
                    self.publish_file(addr, filename, filedata)
                    conn.sendall("Fisierul a fost publicat cu succes!".encode())
                elif command == 'list':
                    # trimite o lista cu toate fisierele publicate
                    self.get_file_list(conn) 
                elif command == 'download':
                    # descarca un fisier
                    filename = conn.recv(1024).decode().strip()
                    filedata = self.get_file(filename)
                    if filedata:
                        conn.sendall(filedata)
                    else:
                        conn.sendall(f"Fisierul {filename} nu exista!".encode())
                elif command == 'read':
                    # citeste un fisier
                    filename = conn.recv(1024).decode().strip()
                    filedata = self.get_file(filename)
                    if filedata:
                        conn.sendall(filedata)
                    else:
                        conn.sendall(f"Fisierul {filename} nu exista!".encode())
                elif command == 'showDirectories':
                    # trimite lista de directoare catre client
                    directories = self.get_directories()
                    conn.sendall(directories.encode())
                elif command == 'exit':
                    # deconecteaza clientul
                    self.remove_client(addr)
                    conn.close()
                    print(f"S-a deconectat clientul: {addr}")
                    break
        except Exception as e:
            print(f"Eroare la comunicarea cu clientul {addr}: {e}")
            self.remove_client(addr)
            conn.close()

    def publish_file(self, addr, filename, filedata):
        # publica un fisier
        directory = f"client_{addr[0]}_{addr[1]}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f"{directory}/{filename}", "wb") as f:
            f.write(filedata)
        print(f"Clientul {addr} a publicat fisierul {filename}")
        self.notify_clients(addr)

        
    def get_file_list(self, conn):
    # Construim lista de fișiere publicate
        filelist = ""
        for client_addr, client_dir in self.clients.items():
            directory = f"client_{client_addr[0]}_{client_addr[1]}"
            if os.path.exists(directory):
                files = os.listdir(directory)
                for file in files:
                    filelist += f"{file}\n"
        filelist += "<END>"
        conn.sendall(filelist.encode())







    def get_file(self, filename):
        # returneaza continutul unui fisier
        for client in self.clients.values():
            directory = f"client_{client[0]}_{client[1]}"
            if os.path.exists(f"{directory}/{filename}"):
                with open(f"{directory}/{filename}", "rb") as f:
                    return f.read()
        return None

    def notify_clients(self, new_client):
        # trimite o notificare tuturor clientilor despre adaugarea unui client nou
        for client_addr, conn in self.clients.items():
            conn.sendall(f"Noul client {new_client} s-a conectat!".encode())

    def remove_client(self, addr):
        # elimina un client din lista de clienti conectati
        if addr in self.clients:
            del self.clients[addr]

    def get_directories(self):
    # returneaza o lista cu toate directoarele de gazda
        directories = ""
        for client in self.clients.values():
            directories += f"client_{client[0]}_{client[1]}\n"
        directories += "<END>"  # Adăugați acest rând pentru a marca sfârșitul listei de directoare
        return directories


    
if __name__ == '__main__':
    port = 5000
    server = Server(port)
    server.listen()
