# for getting and parsing web pages 
import requests
from urlparse import urljoin
from urlparse import urlparse
from bs4 import BeautifulSoup

class discovery:

    # Fuzzer must crawl and guess pages
    # Includes Link discovery & Page guessing
    def discoverPage(page):
        pass
   
   # Fuzzer should keep a list of URLs that it can reach from init page
   # no off-site links

   
    def discoverLink(page):
        linksFound = []

        parsed_url = urlparse(page)
        site = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)

        page = requests.get(url)
        pageData = page.text
        pageSoup = BeautifulSoup(pageData)
        for link in pageSoup.find_all('a'):
            if (link.get('href')).startswith(site):
                linksFound.append(link.get('href'))
            else:
                linksFound.append(site + link.get('href'))

    # Fuzzer should use common word list to discover potenially unlinked pages
    def guessPage():
        pass