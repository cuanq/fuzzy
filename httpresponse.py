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
            for form in forms['form']:
                for vector in vectors:
                    response = strategy.runVector(vector,form)
                    if response.status_code != requests.codes.ok:
                        print('Incorrect status code returned by ' + forms['url'] + '\n' + 'code: ' 
                                 + response.status_code + ' with vector ' + vector '\n')
        else:
            form = random.choice(forms['form'])
            for vector in vectors:
                response = strategy.runVector(vector,form)
                if response.status_code != requests.codes.ok:
                    print('Incorrect status code returned by ' + forms['url'] + '\n' + 'code: ' 
                             + response.status_code + ' with vector ' + vector '\n')
