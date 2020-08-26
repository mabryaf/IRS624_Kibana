PUT /_settings
{
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": { 
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "autocomplete_filter"
          ]
        }
      }
    }
}

PUT /_mapping
{
    "imdb_title_id": {
      "type": "text"
    },
    "original_title": {
      "type": "text",
      "analyzer": "autocomplete", 
      "search_analyzer": "standard",
      "similarity": "BM25"
    },
    "year": { 
      "type": "short"
    },
    "genre": { 
      "type": "text",
      "analyzer": "standard",
      "similarity": "BM25"
    },
    "duration": {
      "type": "short"
    },
    "country": { 
      "type": "text",
      "analyzer": "standard",
      "similarity": "BM25"
    },
    "language": { 
      "type": "text",
      "analyzer": "standard",
      "similarity": "BM25"
    },
    "director": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "BM25"
    },
    "writer": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "BM25"
    },
    "production_company": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "BM25"
    },
    "actors": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "BM25"
    },
    "description": {
      "type": "text",
      "analyzer": "english",
      "similarity": "BM25"   
    },
    "avg_vote": { 
      "type": "half_float"
    }
}

GET faf42_movies1
GET faf42_movies2
GET faf42_movies3_
GET faf42_movies4
GET faf42_movies5
GET faf42_movies6
GET faf42_movies7_

GET /_search
{
    "query": {
        "bool": {
            "should": [
              { "match": { "original_title": {"query": "Avengers Chris Zak Penn", "boost": 5 }}},
              { "match": { "actors": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "genre": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "country": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "language": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "director": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "writer": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "production_company": {"query": "Avengers Chris Zak Penn", "boost": 1 }}},
              { "match": { "description": {"query": "Avengers Chris Zak Penn", "boost": 1 }}}
              ],
            "filter": [
              {"bool": {"must": [
                {"match": {"genre": {"query": "Biography, History"}}},
                {"match": {"language": {"query": "German"}}},
                {"match": {"country": {"query": "UK"}}}
                ]
              }},
              {"range": { "year": { "gte": 1966, "lte": 2020}}},
              {"range": { "duration": { "gte": 0, "lte": 300}}},
              {"range": { "avg_vote": { "gte": 0 }}}
              ]
            }
        }
    }

GET /_search
{
  "query": {
    "multi_match" : {
      "query":    "Traitor Amos Oz", 
      "fields": ["original_title", "director", "writer"]
    }
  }
}

https://www.elastic.co/guide/en/elasticsearch/reference/master/search-analyzer.html
https://www.elastic.co/guide/en/elasticsearch/reference/master/index-modules-similarity.html
https://rebeccabilbro.github.io/intro-doc-similarity-with-elasticsearch/
http://imdbrecommender.azurewebsites.net/search/?title=cleopatra

http://127.0.0.1:5000/search/?text=cleopatra&genre=Biography&country=UK&language=English&yeargte=1945&yearlte=1963&avg_vote=6.5