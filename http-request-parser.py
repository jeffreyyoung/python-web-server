class ParsedHttpRequest:
	def __init__(self, request):
		self.isValid = False
		self.statusCode = None
		self.parse_request(request)
	def parse_request(self, request):

		try:
			message = request.split('\r\n\r\n', 1)
			lines = message[0].split("\r\n")
			requestLineWords = lines[0].split()
			self.method = requestLineWords[0]
			self.url = requestLineWords[1]
			self.version = requestLineWords[2]
			self.headers = {}
			for i in range(1, len(lines)):
				splitheader = lines[i].split(" ", 1)
				self.headers[splitheader[0]] = splitheader[1]

			#check for required headers

			self.isValid = True
			self.statusCode = 200
		except:
			self.isValid = False
			self.statusCode = 400




request = "GET www.google.com HTTP1.1\r\nheadfield1 value1\r\nheadfield2 value2\r\n\r\n"

r = ParsedHttpRequest(request)
print r.isValid, r.statusCode, r.method, r.url, r.version, r.headers