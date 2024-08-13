import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, _ = server_socket.accept() 
        request = client.recv(1024).decode("utf-8")
        status_lint = request.split("\r\n")[0]
        target = status_lint.split(" ")[1]
        msg = target.split("/")[-1]
        
        response = f"""
            HTTP/1.1 200 OK
            \r\n
            Content-Type: text/plain\r\n
            Content-Length: {len(msg)}\r\n
            \r\n
            {msg}           
        """
        client.send(response.encode())
        client.close()

if __name__ == "__main__":
    main()
