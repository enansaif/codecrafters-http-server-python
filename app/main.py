import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept() 
        msg = conn.recv(1024).decode("utf-8")
        request = msg.split("\r\n")
        target = request[0].split(" ")[1]
        if target == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        conn.close()

if __name__ == "__main__":
    main()
