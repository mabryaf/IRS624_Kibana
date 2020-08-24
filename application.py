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
    text = request.args.get('text', '')
    genre = request.args.get('genre', '')
    country = request.args.get('country', '')
    language = request.args.get('language', '')
    yeargte = request.args.get('yeargte', '')
    yearlte = request.args.get('yearlte', 2020)
    durationgte = request.args.get('durationgte', '')
    durationlte = request.args.get('durationlte', 1000)
    avg_vote = request.args.get('avg_vote', '')

    query = {
    "from" : 0, "size" : 10,
    "query": {
        "bool": {
            "must": [],
            "filter": []
            }
        }
    }

    if text:
        text = {
          "multi_match": {
            "query": text,
            "fields": ["original_title", "genre", "country", "language", "director", "writer","production_company", "description"]
          }
        }
        query["query"]["bool"]["must"].append(text)
    if genre:
        genre = { "match": { "genre": genre}}
        query["query"]["bool"]["must"].append(genre)
    if country:
        country = {"match": {"country": country}}
        query["query"]["bool"]["must"].append(country)
    if language:
        language = {"match": {"language": language}}
        query["query"]["bool"]["must"].append(language)
    if yeargte:
        year = {"range": { "year": { "gte": yeargte, "lte": yearlte}}}
        query["query"]["bool"]["filter"].append(year)
    if durationgte:
        duration = {"range": { "duration": { "gte": durationgte, "lte": durationlte}}}
        query["query"]["bool"]["filter"].append(duration)
    if avg_vote:
        avg_vote = {"range": { "avg_vote": { "gte": avg_vote }}}
        query["query"]["bool"]["filter"].append(avg_vote)

    res = es.search(index="faf42_test4",body=query)

    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(year)s: %(original_title)s" % hit["_source"])
    return res

if __name__ == '__main__':
    app.run(debug=True)
