
import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
CLIENT_DATA_PATH = "client_data"
DOWNLOAD_DATA_PATH = "download_data"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))
    username = "Unknown"
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        
        if cmd == "LISTSERVER":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "LISTCLIENT":
            files = os.listdir(CLIENT_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The client directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "LISTDOWNLOAD":
            files = os.listdir(DOWNLOAD_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The download directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            print(f" {username} has uploaded file {name}")
            conn.send(send_data.encode(FORMAT))
    

            
        elif cmd == "DOWNLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(DOWNLOAD_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File downloaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGIN":
            username= data[1]
            print(f"[NEW LOGGED IN] {addr} {username} connected.")
            send_data = "OK@Te-ai logat cu succes "+ username
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    filepath = os.path.join(SERVER_DATA_PATH, filename)
                    os.remove(filepath)
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP":
            data = "OK@"
            data += "LOGIN: Connect with a username to the server.\n"
            data += "LISTSERVER: List all the files from the server.\n"
            data += "LISTCLIENT: List all the files from the client.\n"
            data += "LISTDOWNLOAD: List all the files from the download folder.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DOWNLOAD <filename>: Download a file from the clients.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."

            conn.send(data.encode(FORMAT))
        elif cmd == "INCORRECT":
            data = "OK@"
            data += "You have only those commands:\n\n"
            data += "LOGIN: Connect with a username to the server.\n"
            data += "LISTSERVER: List all the files from the server.\n"
            data += "LISTCLIENT: List all the files from the client.\n"
            data += "LISTDOWNLOAD: List all the files from the download folder.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."

            conn.send(data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
