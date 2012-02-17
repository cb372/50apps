from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
from crawler import Crawler

class MainPage(webapp.RequestHandler):
    def post(self):
        seedURL = cgi.escape(self.request.get('seed'))
        depth = cgi.escape(self.request.get('depth'))
        keyword = cgi.escape(self.request.get('keyword'))

        if seedURL == None or seedURL.strip() == "":
            self.response.out.write("Fill in the seed URL, fool!")
            return
        if depth == None or depth.split() == "":
            self.response.out.write("Fill in the search depth, fool!")
            return
        if keyword == None or keyword.split() == "":
            self.response.out.write("Fill in the search keyword, fool!")
            return
        try:
            depth = int(depth)
        except:
            self.response.out.write("Depth should be a number, fool!")
            return
            
        crawler = Crawler(seedURL, depth, keyword)
        urls = crawler.crawl()

        self.response.out.write('<table class="results">')
        self.response.out.write('<tr><th>URL</th><th>Level</th></tr>')
        for (url, level) in urls:
            self.response.out.write('<tr>')
            self.response.out.write('<td><a class="link" href="%s">%s</a></td>' % (url, url))
            self.response.out.write('<td><span class="level">%s</span></td>' % level)
            self.response.out.write('</tr>')
        self.response.out.write('</table>')
application = webapp.WSGIApplication(
                                     [('/ajax', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
