# Python Web Fuzzer
### Project Specification
http://www.se.rit.edu/~swen-331/projects/fuzzer/

## Contributors
* Danielle Gonzalez 
* Zack Downs
* Stephan Wlodarczyk

## Installation & Setup


1. Download all files
* or clone the Github repository
2. Install the following depenencies using pip 
    * Python (at least 2.4)
    * BeautifulSoup (pip install beautifulsoup4)
    * Requests (pip install requests)


## -----------Usage-------------


## Discover


1. Navigate your terminal/command prompt to the fuzzy directory
2. Type the command:
	
    ``` python
    python fuzz.py discover [Link] [Options] --common-words=[CommonWords]
    ```

	[Link] 	= link you want to use the fuzzier on (ex. http://www.pythonforbeginners.com)
	
    [CommonWords] 	= Newline-delimited file of common words to be used in page guessing and input guessing
	
    [Options] 	= —-custom-auth=dvwa or —-custom-auth=bodgeit to use our hard-coded authentication for the related website
	

### No Authorization
 Omit the --custom-auth parameter 

### Authorization
 include the --custom-auth parameter and specify either dvwa or bodgeit

## Testing

### Vulnerabilities
Fuzzy uses test vectors to check for the following:
    1. Cross-Site Scripting (XSS)
    2. Buffer Overflows
    3. Format String Errors 
    4. Integer Overflows
    5. SQL Injection - Active AND Passive
    6. LDAP Injection
    7. XML Injection
These vectors were obtained from https://www.owasp.org/index.php/OWASP_Testing_Guide_Appendix_C:_Fuzz_Vectors

### Usage

1. Following the directions in Installation and Setup
2. Type the command: 
    ``` python
    python fuzz.py test [Link] [Options] --sensitive=[Sensitive] --vectors=[Vectors]
    ```
    [Link] = link you want to use the fuzzer on

    [Sensitive] = Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response. Required.

    [Vectors] = Newline-delimited file of common exploits to vulnerabilities. Required.
    
    [Options] 
        1. --random=[true|false] When off, try each input to each page systematically.  When on, choose a random page, then a random input field and test all vectors. Default: false.
        2. --slow=500 Number of milliseconds considered when a response is considered "slow". Default is 500 milliseconds
