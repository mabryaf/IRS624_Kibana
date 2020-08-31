from flask import Flask, jsonify, request, render_template, url_for
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
#gumana ka plls
@app.route("/")
def home():
    genre = ['Drama', 'Western', 'Comedy', 'Horror', 'Mystery', 'Fantasy', 'Adventure', 'Romance', 'Sci-Fi', 'Crime', 'Musical', 'Thriller', 'Music', 'Biography', 'Action', 'History', 'War', 'Family', 'Animation', 'Sport']
    country= ['USA', 'Italy', 'Germany', 'Denmark', 'France', 'Belgium', 'Hungary', 'Russia', 'Mexico', 'Sweden', 'Australia', 'Japan', 'UK', 'Austria', 'Spain', 'Czechoslovakia', 'India', 'Brazil', 'Portugal', 'Turkey', 'Netherlands', 'Finland', 'Norway', 'Poland', 'Switzerland', 'Argentina', 'Romania', 'Canada', 'China', 'Yugoslavia', 'Greece', 'Egypt', 'Israel', 'Ireland', 'Philippines', 'Cuba', 'Bulgaria', 'Lebanon', 'Bolivia', 'Chile', 'Iran', 'Croatia', 'Peru', 'Taiwan', 'Senegal', 'Syria', 'Jamaica', 'Algeria', 'Ethiopia', 'Venezuela', 'Mali', 'Indonesia', 'Vietnam', 'Iceland', 'Colombia', 'Tunisia', 'Gibraltar', 'Albania', 'Latvia', 'Ukraine', 'Kazakhstan', 'Estonia', 'Slovakia', 'Bangladesh', 'Georgia', 'Singapore', 'Slovenia', 'Thailand', 'Kuwait', 'Lithuania', 'Ecuador', 'Liechtenstein', 'Pakistan', 'Serbia', 'Uruguay', 'Moldova', 'Malta', 'Nepal', 'Malaysia', 'Armenia', 'Luxembourg', 'Bhutan', 'Iraq', 'Bahamas', 'Jordan', 'Morocco', 'Kosovo', 'Azerbaijan', 'Greenland', 'Palestine', 'Honduras', 'Uganda', 'Guatemala', 'Cyprus', 'Korea', 'Nigeria', 'Mongolia', 'Kyrgyzstan', 'Brunei', 'Panama', 'Yemen', 'Myanmar', 'Paraguay', 'Cambodia', 'Montenegro']
    lang = ['English', 'Italian', 'German', 'Danish', 'French', 'Hungarian', 'Russian', 'Spanish', 'Swedish', 'None', 'Japanese', 'Czech', 'Portuguese', 'Ukrainian', 'Turkish', 'Yiddish', 'Dutch', 'Finnish', 'Norwegian', 'Polish', 'Romanian', 'Hindi', 'Slovenian', 'Mandarin', 'Arabic', 'Serbo-Croatian', 'Bengali', 'Albanian', 'Greek', 'Croatian', 'Urdu', 'Hebrew', 'Sinhalese', 'Esperanto', 'Korean', 'Persian', 'Slovak', 'Estonian', 'Bulgarian', 'Georgian', 'Cantonese', 'Latin', 'Kannada', 'Armenian', 'Bambara', 'Indonesian', 'Vietnamese', 'Irish', 'Malayalam', 'Icelandic', 'Serbian', 'Tamil', 'Saami', 'Bosnian', 'More', 'Latvian', 'Kazakh', 'Haitian', 'Tajik', 'Khmer', 'Wolof', 'Catalan', 'Mongolian', 'Thai', 'Afrikaans', 'Telugu', 'Marathi', 'Kirghiz', 'Macedonian', 'Chinese', 'Tagalog', 'Tibetan', 'Lithuanian', 'Punjabi', 'Frisian', 'Maya', 'Basque', 'Malay', 'Inuktitut', 'Kabuverdianu', 'Kurdish', 'Nepali', 'Dari', 'Dzongkha', 'Zulu', 'Luxembourgish', 'Guarani', 'Tarahumara', 'Flemish', 'Maltese', 'Kinyarwanda', 'Gujarati', 'Tigrigna', 'Filipino', 'Pushto', 'Azerbaijani', 'Swahili', 'Samoan', 'Pular', 'Lao', 'Amharic', 'Aromanian', 'Maori', 'Burmese', 'Gallegan', 'Welsh', 'Aboriginal', 'Assamese', 'Rhaetian', 'Yakut', 'Aymara', 'Neapolitan']
    
    return render_template("index.html",genres=genre, countries=country, langs=lang)

@app.route('/result/', methods=['GET','POST'])
def result():
    input_genre = ['Drama', 'Western', 'Comedy', 'Horror', 'Mystery', 'Fantasy', 'Adventure', 'Romance', 'Sci-Fi', 'Crime', 'Musical', 'Thriller', 'Music', 'Biography', 'Action', 'History', 'War', 'Family', 'Animation', 'Sport']
    input_country= ['USA', 'Italy', 'Germany', 'Denmark', 'France', 'Belgium', 'Hungary', 'Russia', 'Mexico', 'Sweden', 'Australia', 'Japan', 'UK', 'Austria', 'Spain', 'Czechoslovakia', 'India', 'Brazil', 'Portugal', 'Turkey', 'Netherlands', 'Finland', 'Norway', 'Poland', 'Switzerland', 'Argentina', 'Romania', 'Canada', 'China', 'Yugoslavia', 'Greece', 'Egypt', 'Israel', 'Ireland', 'Philippines', 'Cuba', 'Bulgaria', 'Lebanon', 'Bolivia', 'Chile', 'Iran', 'Croatia', 'Peru', 'Taiwan', 'Senegal', 'Syria', 'Jamaica', 'Algeria', 'Ethiopia', 'Venezuela', 'Mali', 'Indonesia', 'Vietnam', 'Iceland', 'Colombia', 'Tunisia', 'Gibraltar', 'Albania', 'Latvia', 'Ukraine', 'Kazakhstan', 'Estonia', 'Slovakia', 'Bangladesh', 'Georgia', 'Singapore', 'Slovenia', 'Thailand', 'Kuwait', 'Lithuania', 'Ecuador', 'Liechtenstein', 'Pakistan', 'Serbia', 'Uruguay', 'Moldova', 'Malta', 'Nepal', 'Malaysia', 'Armenia', 'Luxembourg', 'Bhutan', 'Iraq', 'Bahamas', 'Jordan', 'Morocco', 'Kosovo', 'Azerbaijan', 'Greenland', 'Palestine', 'Honduras', 'Uganda', 'Guatemala', 'Cyprus', 'Korea', 'Nigeria', 'Mongolia', 'Kyrgyzstan', 'Brunei', 'Panama', 'Yemen', 'Myanmar', 'Paraguay', 'Cambodia', 'Montenegro']
    input_lang = ['English', 'Italian', 'German', 'Danish', 'French', 'Hungarian', 'Russian', 'Spanish', 'Swedish', 'None', 'Japanese', 'Czech', 'Portuguese', 'Ukrainian', 'Turkish', 'Yiddish', 'Dutch', 'Finnish', 'Norwegian', 'Polish', 'Romanian', 'Hindi', 'Slovenian', 'Mandarin', 'Arabic', 'Serbo-Croatian', 'Bengali', 'Albanian', 'Greek', 'Croatian', 'Urdu', 'Hebrew', 'Sinhalese', 'Esperanto', 'Korean', 'Persian', 'Slovak', 'Estonian', 'Bulgarian', 'Georgian', 'Cantonese', 'Latin', 'Kannada', 'Armenian', 'Bambara', 'Indonesian', 'Vietnamese', 'Irish', 'Malayalam', 'Icelandic', 'Serbian', 'Tamil', 'Saami', 'Bosnian', 'More', 'Latvian', 'Kazakh', 'Haitian', 'Tajik', 'Khmer', 'Wolof', 'Catalan', 'Mongolian', 'Thai', 'Afrikaans', 'Telugu', 'Marathi', 'Kirghiz', 'Macedonian', 'Chinese', 'Tagalog', 'Tibetan', 'Lithuanian', 'Punjabi', 'Frisian', 'Maya', 'Basque', 'Malay', 'Inuktitut', 'Kabuverdianu', 'Kurdish', 'Nepali', 'Dari', 'Dzongkha', 'Zulu', 'Luxembourgish', 'Guarani', 'Tarahumara', 'Flemish', 'Maltese', 'Kinyarwanda', 'Gujarati', 'Tigrigna', 'Filipino', 'Pushto', 'Azerbaijani', 'Swahili', 'Samoan', 'Pular', 'Lao', 'Amharic', 'Aromanian', 'Maori', 'Burmese', 'Gallegan', 'Welsh', 'Aboriginal', 'Assamese', 'Rhaetian', 'Yakut', 'Aymara', 'Neapolitan']

    text = request.form['text']
    search = text
    genre=request.form.getlist('gens')
    country = request.form.getlist('count')
    language = request.form.getlist('lange')
    avg_vote = request.form['avg_vote']
    yeargte = request.form['yeargte']
    yearlte = request.form['yearlte']
    random = request.form['random']

    if not yearlte:
        yearlte = 2020

    query = {
    "from" : 0, "size" : 30,
    "query": {
        "bool": {
            "should": [],
            "filter": [{
                "bool": {
                    "must": [   ]
                }
            }
            ]
            }
        }
    }

    if text:
        text = [
              { "match": { "original_title": {"query": text, "boost": 4 }}},
              { "match": { "director": {"query": text, "boost": 3 }}},
              { "match": { "actors": {"query": text, "boost": 3 }}},
              { "match": { "genre": {"query": text, "boost": 2 }}},
              { "match": { "country": {"query": text, "boost": 1 }}},
              { "match": { "language": {"query": text, "boost": 1 }}},
              { "match": { "writer": {"query": text, "boost": 1 }}},
              { "match": { "production_company": {"query": text, "boost": 1 }}},
              { "match": { "description": {"query": text, "boost": 1 }}}
              ]
        query["query"]["bool"]["should"].extend(text)
    if random:
        random_query =  {
          "function_score": {
            "query": { "match_all": {} },
            "random_score": {}
          }
        }
        query["query"]["bool"]["should"].extend(random_query)
    if yeargte:
        year = {"range": { "year": { "gte": yeargte, "lte": yearlte}}}
        query["query"]["bool"]["filter"].append(year)
    if avg_vote:
        avg_vote = {"range": { "avg_vote": { "gte": avg_vote }}}
        query["query"]["bool"]["filter"].append(avg_vote)
    if genre:
        genre = {"match": {"genre": {"query": " ".join(genre)}}}
        query["query"]["bool"]["filter"][0]["bool"]["must"].append(genre)
    if country:
        country = {"match": {"country": {"query": " ".join(country)}}}
        query["query"]["bool"]["filter"][0]["bool"]["must"].append(country)
    if language:
        language = {"match": {"language": {"query": " ".join(language)}}}
        query["query"]["bool"]["filter"][0]["bool"]["must"].append(language)

    print(query)
    res = es.search(index="",body=query)

    try:
        print("%d Entries:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print(hit["_score"])
            print("%(avg_vote)s: %(original_title)s (%(year)s)" % hit["_source"])
    except:
        res = es.search(index="faf42_movies1",body=query)

    return render_template("results.html", q_exact=res['hits'], texts=search, genres=input_genre, countries=input_country, langs=input_lang)

if __name__ == '__main__':
    app.run(debug=True)
