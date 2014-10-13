"""
File: sensitivedata.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import random

class SensitiveData():

    def run( self, forms, args, strategy ):
    	vectors = open(test_options['vectors'], "r").read().splitlines()

    	if args['random'].lower() == "true":
    		form = random.choice(forms)
    		for vector in vectors:
    			response = strat.runVector( form, vector )

    			if response != None:
    				sensitive = open( args["sensitive"], "r").read().splitlines()
    				checkSensitive( vector, response, sensitive, form )

    	else:
    		for form in forms:
    			for vector in vectors:
    				response = strategy.runVector( form, vector )

    				if response != None:
    					sensitive = open( args["sensitive"], "r").read().splitlines()
    					checkSensitive( vector, response, sensitive, form )

    def checkSensitive( self, vector, response, sensitive, form):
    	for data in sensitive:
    		if data in response.text:
    			print("\nSensitive Data Leaked:\n\tPage: " + form['url'] + 
    										  "\n\tVector: " + vector +
    										  "\n\tForm: " + form['name'] )