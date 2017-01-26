#web_server.py
#
#Web interface for summarization
#
#Written by Andrew Arpasi

from flask import Flask
from flask import request
from flask import Response
from url_summarize import URLSummarize
import json
import re

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Tet!"

@app.route("/articleSummarize/", methods=['POST','OPTIONS'])
def summarize():
    rawStr = str(request.stream.read())
    rawStr = rawStr.replace("b'","")
    rawStr = rawStr[:-1]
    data = json.loads(rawStr)
    print(data)
    url = data['url']
    length = int(data['length'])
    urlsum = URLSummarize(url)
    info = {}
    info['metadata'] = urlsum.metadata()
    info['summary'] = urlsum.summarize_article(length)
    resultJSON = json.dumps(info, ensure_ascii=False)
    response = Response(resultJSON,content_type="application/json")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    app.debug = True
