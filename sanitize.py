"""
File: sanitize.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""

import random

class Sanitization():

	def _run(self, forms, vulnerability):
		"""
		execute vulernability - fuzz all inputs and make sure 
		they have been sanitized
		"""
		vectors = vulernability._getVectors()

		logger.info("Checking that input has been sanitized, random is currently set to " \
						+ vulernability.options[random)

		for page in pages:
			forms = page.get("inputs").get("forms")
			url = page.get("url")
			
			if vulernability.options.random == "False" or vulernability.options.random == "false":
		
				# sequentially fuzz forms..
				for form in forms:
					for vector in vectors:
						response = vulernability._executeVector(url, vector, form)

						if response != None:
							self._checkForSanitization(vector, response, url)
			else:
			
				if len(forms) > 0:
					form = random.choice(forms) # randomly choose a form

					for vector in vectors:
						response = vulernability._executeVector(url, vector, form)

						if response != None:
							self._checkForSanitization(vector, response, url)

		logger.info("Sanitization checks complete")


	def _checkForSQLExploit(self, response, url):
		"""
		checks if the response has a sql exploit 
		"""
		
		if "MySQL " in response.text:
			logger.info("Possible SQL exploit found on page: " + url)


	def _checkForSpecialChars(self, vector, response, url):
		"""
		checks to see that a few of the common special characters if in the vector has been 
		sanitized in 'da' response
		"""

		if "<" in vector or ">" in vector or "/" in vector or "\"" in vector or "?" in vector:
			if vector in response.text:
				logger.info("Special characters were not sanitized or escaped in page " + url)


	def _checkForSanitization(self, vector, response, url):
		""" 
		checks that response has been sanitized. 
		"""
		self._checkForSQLExploit(response, url)
		self._checkForSpecialChars(vector, response, url)
