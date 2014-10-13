"""
File: sanitize.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""

import random

class Sanitization():

	def run(self, forms, args, vulnerability):

		vectors = vulnerability.getVectors()

		print("Checking for sanitized input; random = " + args["random"])
		
		if args["random"].lower() == "false":
			for form in forms:
				for vector in vectors:
					response = vulnerability.runVector(form, vector)

					if response != None:
						self.checkSanitization(vector, response, form["url"])
		else:
		
			if len(forms) > 0:
				form = random.choice(forms)

				for vector in vectors:
					response = vulnerability.runVector(form, vector)

					if response != None:
						self.checkSanitization(vector, response, form["url"])

	def checkSQLExploit(self, response, url):	
		if "MySQL " in response.text:
			print("SQL exploit found: " + url)
	def checkSpecialChars(self, vector, response, url):
		if "<" in vector or ">" in vector or "/" in vector or "\"" in vector or "?" in vector:
			if vector in response.text:
				print("Special characters have not be escaped/santized: " + url)

	def checkSanitization(self, vector, response, url):
		self.checkSQLExploit(response, url)
		self.checkSpecialChars(vector, response, url)
