import os
import sys
import gzip
import socket
import threading
from typing import Dict

class HTTPRequest:
    method: str
    path: str
    version: str
    body: str
    headers: Dict[str, str]
    
    def __init__(self, request_bytes) -> None:
        self.headers = {}
        self.from_bytes(request_bytes=request_bytes)
    
    def from_bytes(self, request_bytes: bytes) -> None:
        request = request_bytes.decode('utf8')
        request_split = request.split('\r\n')
        status = request_split[0]
        self.method, self.path, self.version = status.split(' ')
        self.body = request_split[-1]
        headers = request_split[1 : -2]
        for header in headers:
            key, value = header.split(': ', 1)
            self.headers[key] = value

class HTTPResponse:
    def __init__(self, metadata):
        self.headers = metadata["headers"]
        self.version = metadata["version"]
        self.status_code = metadata["status_code"]
        self.status_text = metadata["status_text"]
        self.body = metadata["body"]
    
    def to_bytes(self) -> bytes:
        status_line = [self.version, str(self.status_code), self.status_text]
        status_line = ' '.join(status_line)
        headers = '\r\n'.join([k+": "+str(v) for k, v in self.headers.items()])
        response = '\r\n'.join([status_line, headers])
        response += '\r\n\r\n' + self.body
        return response.encode('utf-8')

def request_handler(client):
    request_bytes = client.recv(1024)
    request = HTTPRequest(request_bytes)
    metadata = {
        "headers": {},
        "version": "HTTP/1.1",
        "status_code": 200,
        "status_text": "OK",
        "body": "",
    }
    request_path = request.path.split("/")
    if request_path[1] == "":
        pass
    elif request_path[1] == "user-agent":
        user_agent = request.headers["User-Agent"]
        metadata["headers"]["Content-Type"] = "text/plain"
        metadata["headers"]["Content-Length"] = len(user_agent)
        metadata["body"] = user_agent
    elif request_path[1] == "echo":
        metadata["headers"]["Content-Type"] = "text/plain"
        if "Accept-Encoding" in request.headers:
            encodings = request.headers["Accept-Encoding"].split(", ")
            if "gzip" in encodings:
                metadata["headers"]["Content-Encoding"] = "gzip"
                content = request_path[-1].encode("utf-8")
                gzip_content = gzip.compress(content).decode("utf-8")
                metadata["headers"]["Content-Length"] = len(gzip_content)
                metadata["body"] = gzip_content
        else:
            metadata["headers"]["Content-Length"] = len(request_path[-1])
            metadata["body"] = request_path[-1]
    elif request_path[1] == "files" and os.path.isfile(sys.argv[2] + request_path[-1]):
        file = open(sys.argv[2] + request_path[-1], 'r')
        content = file.read()
        metadata["headers"]["Content-Type"] = "application/octet-stream"
        metadata["headers"]["Content-Length"] = len(content)
        metadata["body"] = content
        file.close()
    elif request_path[1] == "files" and request.method == "POST":
        file = open(sys.argv[2] + request_path[-1], 'w')
        file.write(request.body)
        file.close()
        metadata["status_code"] = 201
        metadata["status_text"] = "Created"
    else:
        metadata["status_code"] = 404
        metadata["status_text"] = "Not Found"
    response = HTTPResponse(metadata)
    client.send(response.to_bytes())
    client.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, _ = server_socket.accept()
        t = threading.Thread(target=request_handler, args=(client,))
        t.start()
        

if __name__ == "__main__":
    main()
