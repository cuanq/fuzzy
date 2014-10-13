"""
File: httpresponse.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import requests 
import random

class HttpResponse():

    def run(self, forms, args, strategy):
        vectors = strategy.getVectors()
        
        if args['random'].lower() == 'false':
            for form in forms:
                for vector in vectors:
                    response = strategy.runVector(form, vector)
                    if response.status_code != requests.codes.ok:
                        print('Incorrect status code returned')
        else:
            form = random.choice(forms)
            for vector in vectors:
                response = strategy.runVector(form, vector)
                if response.status_code != requests.codes.ok:
                    print('Incorrect status code returned')
