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
    def __init__(self):
        self.headers = {}
        self.version = "HTTP/1.1"
        self.status_code = 200
        self.status_text = "OK"
        self.body = ""
    
    def to_bytes(self) -> bytes:
        status_line = [self.version, str(self.status_code), self.status_text]
        status_line = ' '.join(status_line)
        headers = '\r\n'.join([k+": "+str(v) for k, v in self.headers.items()])
        response = '\r\n'.join([status_line, headers])
        response += '\r\n\r\n'
        if type(self.body) == str:
            response += self.body
            return response.encode('utf-8')
        return b"".join([response.encode('utf-8'), self.body])
