import time


import os




class HttpResponseBuilder:
	def __init__(self, config):
		self.config = config

	def getResponse(self, request):

		path = self.getPath(request.url)

		return HttpResponse(path, self.config, "200").toString()

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
	def __init__(self, path, config, code):
		self.headers = {}
		self.path = path
		self.headers["Date"] = str(time.time())
		self.headers["Server"] = "jeffrey_server3.0"
		self.code = code
		if code is "200":
			self.appendFile(path, config)


	def appendFile(self, path, config):
		print os.path.exists(path), path
		if os.path.exists(path):
			extension = os.path.splitext(path)[1]
			self.headers["Content-Type"] = config.medias[extension[1:]]
			self.headers["Content-Length"] = str(os.path.getsize(path))
			self.headers["Last-Modified"] = str(os.stat(path).st_mtime) 
		else:
			self.code = "404"

	def toString(self):
		res = ""
		if self.code is "200":
			res += "HTTP/1.1 " +self.code + "OK" + "\r\n" #change this
			res += self.headersToString()
			if self.code is "200":
				with open(self.path, "rb") as f:
				    res += f.read()
			return res
		elif self.code is "400":
			return res
		elif self.code is "403":
			return res
		elif self.code is "404":
			return res
		elif self.code is "500":
			return res
		elif self.code is "501":
			return res

	def headersToString(self):
		res = ""
		for key, value in self.headers.iteritems():
			res += key + ": " + value + "\r\n"

		return res

