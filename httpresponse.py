"""
File: httpresponse.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import requests 

class HttpResponse():

    def run(forms, strategy, test_options):
        vectors = open(test_options['vectors'], "r").read().splitlines()
        
        if test_options['random'].lower() == 'false':
            for form in forms:
                for vector in vectors:
                    # TODO: 
