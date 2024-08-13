import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept() # wait for client
        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        conn.close()

if __name__ == "__main__":
    main()
