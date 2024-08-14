import socket
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

class HTTPResponse():
    def __init__(self, values):
        self.headers = values["headers"]
        self.version = values["version"]
        self.status_code = values["status_code"]
        self.status_text = values["status_text"]
        self.body = values["body"]
    
    def to_bytes(self) -> bytes:
        status_line = [self.version, str(self.status_code), self.status_text]
        status_line = ' '.join(status_line)
        headers = '\r\n'.join([k+": "+str(v) for k, v in self.headers.items()])
        response = '\r\n'.join([status_line, headers, self.body])
        return response.encode('utf-8')

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, _ = server_socket.accept() 
        request_bytes = client.recv(1024)
        request = HTTPRequest(request_bytes)
        values = {
            "headers": {},
            "version": "HTTP/1.1",
            "status_code": 200,
            "status_text": "OK",
            "body": "",
        }
        if request.path == "/user-agent":
            user_agent = request.headers["User-Agent"]
            values["headers"]["Content-Type"] = "text/plain"
            values["headers"]["Content-Length"] = len(user_agent)
            values["body"] = user_agent
        elif request.path[:6] == "/echo/":
            path = request.path[6:]
            values["headers"]["Content-Type"] = "text/plain"
            values["headers"]["Content-Length"] = len(path)
            values["body"] = path
        else:
            values["status_code"] = 404
            values["status_text"] = "Not Found"
        client.send(HTTPResponse(values).encode())
        client.close()

if __name__ == "__main__":
    main()
