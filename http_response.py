import time
import os
import stat

class HttpResponseBuilder:
	def __init__(self, config):
		self.config = config

	def getResponse(self, request):
		path = ""

		if request.statusCode == "200":	
			path = self.getPath(request.url)
		
		return HttpResponse(path, self.config, request.statusCode, request.method).toString()


	def getPath(self, url):
		path = url.path
		if path.endswith(('/')):
			path += "index.html"

		if url.netloc in self.config.hosts:
			path = self.config.hosts[url.netloc] + path
		else:
			path = self.config.hosts["default"] + path
		return path

class HttpResponse:
	def __init__(self, path, config, code, method):
		self.headers = {}
		self.path = path
		self.headers["Date"] = str(time.time())
		self.headers["Server"] = "jeffrey_server3.0"
		self.code = code
		self.config = config
		self.requestMethod = method
		if code is "200":
			self.addFileHeaders(path, config)
	def hasFilePermissions(self, path):
		st = os.stat(path)
		return bool(st.st_mode & stat.S_IRGRP)
	def addFileHeaders(self, path, config):
		print os.path.exists(path), path
		if os.path.exists(path):
			if self.hasFilePermissions(path):
				extension = os.path.splitext(path)[1]
				self.headers["Content-Type"] = config.medias[extension[1:]]
				self.headers["Content-Length"] = str(os.path.getsize(path))
				self.headers["Last-Modified"] = str(os.stat(path).st_mtime)
			else:
				self.code = "403" 
		else:
			self.code = "404"

	def getStatusLine(self, code):
		statusLine = ""
		
		if code is "200":
			statusLine += "HTTP/1.1 " +self.code + " OK" + "\r\n" #change this	
		elif code is "400":
			statusLine += "HTTP/1.1 " + self.code + " BAD REQUEST" + "\r\n"
		elif code is "403":
			statusLine += "HTTP/1.1 " + self.code + " Forbidden" + "\r\n"
		elif code is "404":
			statusLine += "HTTP/1.1 " + self.code + " NOT FOUND" + "\r\n"
		elif code is "500":
			statusLine += "HTTP/1.1 " + self.code + " Internal Server Error" + "\r\n"
		elif code is "501":
			statusLine += "HTTP/1.1 " + self.code + " Not Implemented" + "\r\n"

		return statusLine;

	def getResponseBody(self, code):
		resbody = ""
		if code is "200":
			pass
		elif code is "400":
			resbody = "<html><body><h1>400 Bad Request</h1></body></html>"
		elif code is "403":
			resbody = "<html><body><h1>403 Forbidden</h1></body></html>"
		elif code is "404":
			resbody = "<html><body><h1>404 Not Found</h1></body></html>"
		elif code is "500":
			resbody = "<html><body><h1>500 Internal Server Error</h1></body></html>"
		elif code is "501":
			resbody = "<html><body><h1>501 Not Implemented</h1></body></html>"
		return resbody;

	def toString(self):
		res = self.getStatusLine(self.code)

		if self.requestMethod == "HEAD" and self.code is "200":
			resbody = self.getResponseBody(self.code)
			self.addResponseBodyHeaders(resbody)
			res += self.headersToString()
		else:
			resbody = self.getResponseBody(self.code)
			self.addResponseBodyHeaders(resbody)
			res += self.headersToString()
			if self.code is "200":
				with open(self.path, "rb") as f:
		 		    res += f.read()
			else:
				res += resbody

		return res

	def addResponseBodyHeaders(self, resbody):
			if self.code == "200":
				extension = os.path.splitext(self.path)[1]
				self.headers["Content-Type"] = self.config.medias[extension[1:]]
				self.headers["Content-Length"] = str(os.path.getsize(self.path))
				self.headers["Last-Modified"] = str(os.stat(self.path).st_mtime)
			else:
				self.headers["Content-Type"] = self.config.medias["html"]
				self.headers["Content-Length"] = str(len(resbody))
				self.headers["Last-Modified"] = str(time.time()) 

	def headersToString(self):
		res = ""
		for key, value in self.headers.iteritems():
			res += key + ": " + value + "\r\n"

		res += "\r\n"
		return res

