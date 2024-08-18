import socket
import threading
from .utils import HTTPRequest, HTTPResponse
from .handlers import *

class RequestHandler:
    def __init__(self):
        self.handlers = {
            "user-agent": UserAgentHandler(),
            "echo": EchoHandler(),
            "files": FileHandler(),
        }
    
    def handle_request(self, request):
        target = request.path.split("/")[1]
        if target in self.handlers:
            return self.handlers[target].handle(request)
        return self.default_handler()
    
    @staticmethod
    def default_handler():
        response = HTTPResponse()
        response.status_code = 404
        response.status_text = "Not Found"
        return response
    
def worker(client):
    request_bytes = client.recv(1024)
    request = HTTPRequest(request_bytes)
    request_handler = RequestHandler()
    response = request_handler.handle_request(request)
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
