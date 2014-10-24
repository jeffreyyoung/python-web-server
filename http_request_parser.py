from urlparse import urlparse

class ParsedHttpRequest:
	def __init__(self, request):
		self.parse_request(request)
	def parse_request(self, request):

		try:
			message = request.split('\r\n\r\n', 1)
			lines = message[0].split("\r\n")
			requestLineWords = lines[0].split()
			self.method = requestLineWords[0]
			self.url = urlparse(requestLineWords[1])
			#self.url = requestLineWords[1]
			self.version = requestLineWords[2]
			self.headers = {}
			for i in range(1, len(lines)):
				splitheader = lines[i].split(":", 1)
				self.headers[splitheader[0].strip()] = splitheader[1].strip()

			#check for required headers
			print self.method
			if self.method != "HEAD" and self.method != "GET":
				self.statusCode = "501"
			elif self.url is None:
				self.statusCode = "501"
			else:
				self.statusCode = "200"
		except:
			self.statusCode = "400"




# request = "GET www.google.com HTTP1.1\r\nheadfield1: value1\r\nheadfield2: value2\r\n\r\n"
# request = "GET http://www.google.com/ HTTP1.1\r\nheadfield1: value1\r\nheadfield2: value2\r\n\r\n"

# r = ParsedHttpRequest(request)
# print r.statusCode