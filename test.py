"""
File: test.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import random

from vulnerability_strategy import *
from sensitivedata import *
from sanitize import *
from delayresponse import *
from httpresponse import *

""" 
Takes in an assortment of web urls, and user enabled 
testing options (i.e. vectors, sensititive, random, slow)
"""
def test_pages(forms, args):
	
	for form in forms:
		print("1 " + form + " 2")

	""" Setup strategy """
	if args["random"].lower() == "true":
		print("random shuffling enabled")
		random.shuffle(forms)

	sanitize = VulnerabilityStrategy(forms, Sanitization(), args)
	delayResponse = VulnerabilityStrategy(forms, DelayResponse(), args)
	httpResponse = VulnerabilityStrategy(forms, HttpResponse(), args)
	sensistive = VulnerabilityStrategy(forms, SensitiveData(), args)

	sanitize.run()
	delayResponse.run()
	httpResponse.run()
	sensistive.run()

