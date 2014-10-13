"""
File: test.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import random

""" 
Takes in an assortment of web urls, and user enabled 
testing options (i.e. vectors, sensititive, random, slow)
"""
def test_pages(forms, testing_options):

	""" Setup strategy """
	if testing_options["random"].lower() == "true"
		print("random shuffling enabled")
		random.shuffle(url)

	sanitize = VulnerabilityStrategy(forms, Sanitization(), testing_options)
	delayResponse = VulnerabilityStrategy(forms, DelayReponse(), testing_options)
	httpResponse = VulnerabilityStrategy(forms, HttpResponse(), testing_options)
	sensistive = VulnerabilityStrategy(forms, SensitiveData(), testing_options)

	sanitize.run()
	delayResponse.run()
	httpResponse.run()
	sensistive.run()

