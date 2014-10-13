import time
import random

"""
File: delayresponse.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""

class DelayResponse():

    def run(self, forms, args, strategy):
        delay = args['slow']
        vectors = strategy.getVectors()

        if args['random'].lower() == 'false':
            
            for form in forms['form']:
                for vector in vectors:
                    begin = time.time()
                    response = strategy.runVector(vector,form)
                    end = time.time()
                    if(end - begin) > DelayResponse:
                        print(forms['url'] + ' had a delayed response of ' + end + ' with this vectors:' + vector + '\n')
        else:
            form = random.choice(forms['form'])
            for vector in vectors:
                begin = time.time()
                response = strategy.runVector(vector,form)
                end = time.time()
                if(end - begin) > DelayResponse:
                    print(forms['url'] + ' had a delayed response of ' + end + ' with this vectors:' + vector + '\n')





