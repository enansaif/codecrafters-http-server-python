import socket
import threading
from utils import HTTPRequest, HTTPResponse
from functions import *

def request_handler(request_bytes):
    request = HTTPRequest(request_bytes)
    request_path = request.path.split("/")
    if request_path[1] == "user-agent":
        return handle_user_agent(request)
    if request_path[1] == "echo":
        return handle_echo(request, request_path[-1])
    if request_path[1] == "files":
        return handle_files(request, request_path[-1])
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
