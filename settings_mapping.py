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
      "similarity": "boolean"
    },
    "writer": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "boolean"
    },
    "production_company": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "boolean"
    },
    "actors": {
      "type": "text",
      "analyzer": "standard", 
      "similarity": "boolean"
    },
    "description": {
      "type": "text",
      "analyzer": "english",
      "similarity": "boolean"   
    },
    "avg_vote": {
      "type": "half_float"
    }
}

http://127.0.0.1:5000/search/?text=cleopatra&genre=Biography&country=UK&language=English&yeargte=1945&yearlte=1963&durationgte=138&durationlte=200&avg_vote=6.5