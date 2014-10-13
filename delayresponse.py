import time
"""
File: delayresponse.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""

class DelayResponse():

    def run(forms, strategy, test_options):
        delay = test_options['slow']
        vectors = open(test_options['vectors'], "r").read().splitlines()

        if test_options['random'].lower() == 'false':
            
            for form in forms:
                for vector in vectors:
                    begin = time.time()
                    # TODO: add vulnerability strategy call
                    end = time.time()
                    if(end - begin) > DelayResponse:
                        print(forms['url'] + ' had a delayed response of ' + end + ' with this vectors: \n' + vector)
        else:
            # TODO: randomly choose a form here somehow
            for vector in vectors:
                begin = time.time()
                # TODO: add vulnerability strategy call
                end = time.time()
                if(end - begin) > DelayResponse:
                    print(forms['url'] + ' had a delayed response of ' + end + ' with this vectors: \n' + vector)





