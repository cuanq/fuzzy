"""
File: test.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import random


""" 
Takes in an assortment of web urls, and user enabled 
testing options (i.e. vectors, sensititive, random, slow)
"""
def test_pages(url, testing_options):

	""" Setup strategy """
	if testing_option.lower() == "true"
		print("random shuffling enabled")
		random.shuffle(url)

	sanitize = VulnerabilityStrategy(url, Sanitization(), testing_options)
	delayResponse = VulnerabilityStrategy(url, DelayReponse(), testing_options)
	httpResponse = VulnerabilityStrategy(url, HttpResponse(), testing_options)
	sensistive = VulnerabilityStrategy(url, SensitiveData(), testing_options)

	""" Execute vulernability strategies """
	sanitize.run()
	delayResponse.run()
	httpResponse.run()
	sensistive.run()

