#url_summarize.py
#
#Takes content from a news article URL and summarizes it
#
#Written by Andrew Arpasi

from summarize import Summarize
from newspaper import Article

class URLSummarize(object):

    url = ""
    article = None

    def __init__(self,url):
        self.url = url
        self.article = Article(self.url)
        self.initialize_article()

    def initialize_article(self):
        self.article.download()
        self.article.parse()

    def summarize_article(self,numSentences = 4,algorithm = 2):
        summarizer = Summarize()
        sum = "Error: Could not summarize. Please make sure you have entered a valid article URL."
        if len(self.article.text) > 3:
            sum = summarizer.summarize_text(self.article.text,numSentences,algorithm)
        return sum

    def metadata(self):
        data = {}
        data['title'] = self.article.title
        data['img'] = self.article.top_image
        data['authors'] = self.article.authors
        return data