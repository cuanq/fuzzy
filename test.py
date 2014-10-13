"""
File: test.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import random

""" 
Takes in an assortment of web urls, and user enabled 
testing options (i.e. vectors, sensititive, random, slow)
"""
def test_pages(forms, args):

	""" Setup strategy """
	if args["random"].lower() == "true":
		print("random shuffling enabled")
		random.shuffle(forms)

	sanitize = VulnerabilityStrategy(forms, Sanitization(), args)
	delayResponse = VulnerabilityStrategy(forms, DelayReponse(), args)
	httpResponse = VulnerabilityStrategy(forms, HttpResponse(), args)
	sensistive = VulnerabilityStrategy(forms, SensitiveData(), args)

	sanitize.run()
	delayResponse.run()
	httpResponse.run()
	sensistive.run()

