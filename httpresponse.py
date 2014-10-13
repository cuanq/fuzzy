"""
File: httpresponse.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
import requests 

class HttpResponse():

    def run(forms, strategy, test_options):
        vectors = open(test_options['vectors'], "r").read().splitlines()
        
        if test_options['random'].lower() == 'false':
            for form in forms['form']:
                for vector in vectors:
                    # TODO: add vulnerability strategy call
                    if response.status_code != requests.codes.ok:
                        print('Incorrect status code returned by ' + forms['url'] + '\n' + 'code: ' 
                                 + response.status_code + ' with vector ' + vector '\n')
        else:
            # somehow randomly choose a form 
            for vector in vectors:
                # TODO: add vulnerability strategy call
                if response.status_code != requests.codes.ok:
                    print('Incorrect status code returned by ' + forms['url'] + '\n' + 'code: ' 
                             + response.status_code + ' with vector ' + vector '\n')
