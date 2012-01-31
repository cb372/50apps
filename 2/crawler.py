# coding:UTF-8
#
# 50 Apps Challenge
# App 1: A web crawler in Python
#
import sys
import logging
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin

from google.appengine.api import urlfetch
logging.basicConfig(level=logging.DEBUG)

class Crawler:
    def __init__(self, seedURL, depth, keyword):
        self.seedURL = seedURL
        self.maxDepth = depth
        self.depth = 1
        self.keyword = keyword
        self.visited = set()
        self.matched = set()

    def crawl(self):
        urls = set()
        urls.add(self.seedURL)
        self.crawlRecursive(urls, self.depth)
        return self.matched

    def crawlRecursive(self, urls, depth):
        if depth > self.maxDepth:
            return
        else:
            for url in urls:
                if url not in self.visited:
                    links = self.scrape(url)
                    self.crawlRecursive(links, depth+1)
            return

    def scrape(self, url):
        logging.debug("Scraping %s" % url)
        # Mark URL as visited, even if we are going to choke on it
        self.visited.add(url)
        try:
            result = urlfetch.fetch(url)
            if "html" in result.headers['Content-Type']:
                html = unicode(result.content, 'utf-8')
                # Simple substring search of the raw HTML
                if html.find(self.keyword) > -1:
                    self.matched.add((url, level))
                # Use Beautiful Soup to extract links
                soup = BeautifulSoup(html)
                links = [urljoin(url, unicode(link['href'])) for link in soup.findAll('a')]
                return links
            else:
                # Skip non-HTML content
                logging.debug("Skipping non-HTML content at %s" % url)
                return {}
        except Exception, ex:
            logging.exception("Choked on %s" % url)
            return {}

def main(argv):
    if len(argv) != 4:
        printUsage()
        return
    else:
        crawler = Crawler(argv[1], int(argv[2]), argv[3])
        urls = crawler.crawl()
        for url in urls:
            print(url)

def printUsage():
    print("Usage: python crawler.py seedURL depth keyword")

if __name__ == "__main__":
    main(sys.argv)

