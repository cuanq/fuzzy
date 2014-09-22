# Python Web Fuzzer

Installation & Setup
=====================

1. Download all files
* or clone the Github repository
2. Install the following depenencies using pip 
    * Python (at least 2.4)
    * BeautifulSoup (pip install beautifulsoup4)
    * Requests (pip install requests)


Usage
====== 

Discover
========

1. Navigate your terminal/command prompt to the fuzzy directory
2. Type the command:
	‘python fuzz.py discover *Link* —-common-words=*CommonWords* *Options*

	*Link* 		= link you want to use the fuzzier on (ex. http://www.pythonforbeginners.com)
	*CommonWords* 	= Newline-delimited file of common words to be used in page guessing and input guessing
	*Options* 	= —-custom-auth=dvwa or —-custom-auth=bodgeit to use our hard-coded authentication for the related website
	

No Authorization
-----------------

Authorization
--------------


