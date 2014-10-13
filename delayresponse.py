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
            
            for form in forms:
                for vector in vectors:
                    begin = time.time()
                    response = strategy.runVector(form, vector)
                    end = time.time()
                    if(end - begin) > delay:
                        print(form['url'] + ' had a delayed response of ' + end + ' with this vectors:' + vector + '\n')
        else:
            form = random.choice(forms)
            for vector in vectors:
                begin = time.time()
                response = strategy.runVector(form, vector)
                end = time.time()
                if(end - begin) > delay:
                    print(form['url'] + ' had a delayed response of ' + end + ' with this vectors:' + vector + '\n')





