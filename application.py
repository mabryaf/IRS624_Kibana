from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context

# from datetime import datetime
# from bson.json_util import dumps
# from json import loads
import ssl

app = Flask(__name__)

context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

es = Elasticsearch(
    ['tux-es1.cci.drexel.edu','tux-es2.cci.drexel.edu','tux-es3.cci.drexel.edu'],
    http_auth=('faf42', 'ohs4aeceeziz'),
    scheme="https",
    port=9200,
    ssl_context = context,
)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/search/', methods=['GET'])
def search():
    title = request.args.get('title', '')
    query = {
    "from" : 0, "size" : 10,
    "query": {
        "multi_match" : {
        "query": title,
        "fields": ["original_title"]
        }
    }
    }

    res = es.search(index="faf42_info624_201904_movies",body=query)

    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(year)s: %(original_title)s" % hit["_source"])
    return res

@app.route('/test/', methods=['GET'])
def test():
    return {}

@app.route('/searching/', methods=['GET'])
def searching():
    res = es.search(index="faf42_info624_201904_movies")

    return res

if __name__ == '__main__':
    app.run(debug=True)