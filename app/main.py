import socket
import threading
from .utils import HTTPRequest, HTTPResponse
from .handlers import *

def request_handler(request_bytes):
    request = HTTPRequest(request_bytes)
    request_path = request.path.split("/")
    handlers = {
        "user-agent": UserAgentHandler(),
        "echo": EchoHandler(),
        "files": FileHandler(),
    }
    if request_path[1] == "user-agent":
        return handlers["user-agent"].handle(request)
    if request_path[1] == "echo":
        return handlers["echo"].handle(request)
    if request_path[1] == "files":
        return handlers["files"].handle(request)
    response = HTTPResponse()
    if request_path[1] != '':
        response.status_code = 404
        response.status_text = "Not Found"
    return response
    
def worker(client):
    request_bytes = client.recv(1024)
    response = request_handler(request_bytes)
    client.send(response.to_bytes())
    client.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, _ = server_socket.accept()
        t = threading.Thread(target=worker, args=(client,))
        t.start()

if __name__ == "__main__":
    main()
