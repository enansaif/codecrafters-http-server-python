import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, _ = server_socket.accept() 
        request = client.recv(1024).decode("utf-8")
        status_lint = request.split("\r\n")[0]
        target = status_lint.split(" ")[1]
        if target == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif target[:6] == "/echo/":
            value = target[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}"
        else:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n"
        client.send(response.encode())
        client.close()

if __name__ == "__main__":
    main()
