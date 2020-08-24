from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import ssl

# from datetime import datetime
# from bson.json_util import dumps
# from json import loads


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

es = Elasticsearch(
['ca98ff291d2d43b0b4b58d6690388e2d.eastus2.azure.elastic-cloud.com'],
http_auth=('elastic', 'G05ZW6nzrSsKsByMfdwYzrDn'),
scheme="https",
port=9243,
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
        "fields": ["original_title", 'description']
        }
    }
    }

    res = es.search(index="faf42_imdbmovies",body=query)

    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(year)s: %(original_title)s" % hit["_source"])
    return res

if __name__ == '__main__':
    app.run(debug=True)