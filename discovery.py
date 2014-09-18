import requests
import sys
from bs4 import BeautifulSoup

class discovery:

    # Fuzzer must crawl and guess pages
    # Includes Link discovery & Page guessing
    def discoverPage(page):
        pass
   
   # Fuzzer should keep a list of URLs that it can reach from init page
   # no off-site links

    # !!!! ISSUE: not everything is a full URL but some things are
    def discoverLink(page):
        linksFound = []

        aPage = requests.get(page)
        pageData = aPage.text
        pageSoup = BeautifulSoup(pageData)
        for link in pageSoup.find_all('a'):
            linksFound.append(link.get('href'))

    # Fuzzer should use common word list to discover potenially unlinked pages
    def guessPage():
        pass
    # Fuzzer should attempt to discover every possible input into system
    # Includes Parse URLs, Form parameters, & Cookies 
    def discoverInput():

        pass