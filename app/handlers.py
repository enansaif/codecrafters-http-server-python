import os
import sys
import gzip
from .utils import HTTPResponse
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, request):
        return NotImplementedError('Each handler must be implemented')


class UserAgentHandler(BaseHandler):
    def handle(self, request):
        response = HTTPResponse()
        user_agent = request.headers["User-Agent"]
        response.headers["Content-Type"] = "text/plain"
        response.headers["Content-Length"] = len(user_agent)
        response.body = user_agent
        return response
    
    
class EchoHandler(BaseHandler):
    def handle(self, request):
        data = request.path.split("/")[-1]
        response = HTTPResponse()
        response.headers["Content-Type"] = "text/plain"
        if "Accept-Encoding" in request.headers:
            encodings = request.headers["Accept-Encoding"].split(", ")
            if "gzip" in encodings:
                response.headers["Content-Encoding"] = "gzip"
                content = data.encode("utf-8")
                gzip_content = gzip.compress(content)
                response.headers["Content-Length"] = len(gzip_content)
                response.body = gzip_content
        else:
            response.headers["Content-Length"] = len(data)
            response.body = data
        return response


class FileHandler(BaseHandler):
    def handle(self, request):
        file_name = request.path.split("/")[-1]
        response = HTTPResponse()
        if request.method == "POST":
            file = open(sys.argv[2] + file_name, 'w')
            file.write(request.body)
            file.close()
            response.status_code = 201
            response.status_text = "Created"
        elif os.path.isfile(sys.argv[2] + file_name):
            file = open(sys.argv[2] + file_name, 'r')
            content = file.read()
            response.headers["Content-Type"] = "application/octet-stream"
            response.headers["Content-Length"] = len(content)
            response.body = content
            file.close()
        else:
            response.status_code = 404
            response.status_text = "Not Found"
        return response
    