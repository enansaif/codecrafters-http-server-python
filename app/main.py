import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept() 
        msg = conn.recv().decode("utf-8")
        print(msg)
        conn.close()

if __name__ == "__main__":
    main()
