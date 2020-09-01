# Why: Explain the purpose of the search engine and what difference you can make.
- The goal of the project is to create a search engine that revolves on the dataset that was obtained from Kaggle. The search engine will be capable of accepting a query and filters as a request from the user. Then, it will give out a list of movies which have the closest similarity to the query while at the same time filtering based on the requirements of the user. The similarity score is computed via BM25, a scoring similar to TF-IDF. Moreover, specific fields have been boosted based on the importance decided by the researchers: title, actors, director, genre, and others. 
- Thus, the output is a list of movies which show most of the important details in one screen. This makes it easier to view the list of movies compared to most search engines which just show the title, year, description, and rating. The UI is not flashy, but the results of the search engine are direct to the point which will cater to the user who just wants the list and its details, with no added clicks to navigate to different information about the movie.
- However, the titles are hyperlinked to the IMDb website if they do choose to get a more detailed view of the title.
# What: Describe the data and domain in which you build the search engine index. Please provide details about where the data source is and how you collected the data.
- The dataset is 'IMDb movies.csv' which comes from Kaggle (https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset). It contains 81,273 movies with 22 attributes. However, the researchers trimmed the said dataset to retain 12 attributes. Other attributes were removed because they were either missing too much information or they were not useful for the purpose of the project. The final list of fields are listed below.

| Columns  | Data Type | Description |
| ------------- | ------------- | ------------- |
| imdb_title_id  | String  | Unique identifier of the film in the IMDb website  |
| original_title  | String  | The name of the film  |
| year  | Integer  | The year of production  |
| genre  | String  | Keyword or category that classifies the film  |
| duration  | Integer  | The total time it takes to watch the film  |
| country  | String  | The places where the film was shot  |
| language  | String  | The communications used in the film  |
| director  | String  | The person/s who was in charge of production  |
| writer  | String  | The person/s who created the story  |
| production_company  | String  | The organization which was in charge of creating the film  |
| actors  | String  | The person/s who represented the characters  |
| description  | String  | A written representation or plot summary of the film   |
| avg_vote  | Float  | The average rating  |
- Using Kibana’s elasticsearch, the researchers were able to upload the dataset and at the same time leverage the built-in analyzers and similarity scoring that it already had. 
- IMDb or the Internet Movie Database is a website that stores details about films or facts related to films. Some examples are the cast, production crew, personal biographies, plot summaries, trivias, and ratings and reviews.
# Who: Explain whom your search engines may serve and their basic information needs. Ideally You should be able to describe three use cases (information needs).
- The search engine is for people who want a quicker or straightforward way of getting the list of movies that is related to their query. It does not boast a very excellent UI that other sites have, but that is exactly why it is better for people who just want the titles and information about it much quicker. There is no need to click other buttons or navigate to other pages to get more information about the movie. Moreover, unlike websites like Netflix, the titles in the search engine cater to a more broad audience who may want something that is from the early 1900s, but it is fully equipped with the latest titles from 2018 as well.
- First Use Case: The user will be capable of entering a query and they will receive a list of movies with the highest similarity to the query.
- Second Use Case: The user will be capable of adding filters to the query and movies matching the filter will be removed from the list
- Third Use Case: The user will be capable of receiving a random list of films

# How: Describe related decisions you have made and steps you have taken to build the Engine
## Steps:
1. Obtain dataset from Kaggle.
2. Preprocess the data to retain attributes of interest and remove rows with missing details.
3. Setup free trial account in Kibana.
4. Upload dataset in Kibana and manage the settings and mapping.
5. Test queries using the dev tools of Kibana.
6. Create Github repository for source control.
7. Create an endpoint to utilize Kibana using Python with Flask framework.
8. Translate test queries from Kibana to queries in Python.
9. Design and create User Interface.
10. Deploy the source code in Heroku.
11. https://imdbsearchengine.herokuapp.com/	

## 1. Describe the data fields related to the project and how they should be analyzed and indexed. Select proper data types, analyzers, filters, etc. for each field, and provide your rationale.
- Below are the index settings and mapping which was made for Elasticsearch. The field types were assigned such that the least number of bits would be used for storing the data. For example, short was used instead of long because short was sufficient to store the data we have for the whole numbers. This is done to decrease memory footprint and try to obtain maximum processing speed when querying. 
- Next, the analyzer decides how the contents of the field will be tokenized. For the purposes of the project, autocomplete, standard, and english were used. Autocomplete would tokenize at index time based on multiple combinations of the field content, not just on the delimiters. This is done by the "edge_ngram" which specifies the minimum and maximum length that is stored. For example, the term 'quick' would be indexed as terms: ['q', 'qu', 'qui', 'quic', 'quick]. Using autocomplete as analyzer and standard as search_analyzer would allow the query to be matched to the content of the field despite lacking some letters or having misspellings. Meanwhile, standard and english would tokenize based on the delimiter and remove stopwords as well. English analyzer has stemming for english words, meaning it gets the root word by removing prefixes or suffixes.
```
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
```
```
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
```

## 2. Describe your search queries in terms the use cases (needs):
### Use Case 1: Query
For the first use case, the user simply needs to input a query in the search bar and they will receive the top 30 films which matches the query. The score would then be calculated based on the fields: original_title, actors, director, genre, country, language, writer, production_company, description. Each field comes with a specific boost or multiplier based on importance. The structure uses bool with should as it tries to match the query for all fields, but it is not required to match all of them. However, more matches and matches on the boosted fields would provide a higher score.
```
GET /_search
{
    "query": {
        "bool": {
            "should": [
                { "match": { "original_title": {"query": "Avengers", "boost": 4 }}},
                { "match": { "actors": {"query": "Avengers", "boost": 3 }}},
                { "match": { "director": {"query": "Avengers", "boost": 3 }}},
                { "match": { "genre": {"query": "Avengers", "boost": 2 }}},
                { "match": { "country": {"query": "Avengers", "boost": 1 }}},
                { "match": { "language": {"query": "Avengers", "boost": 1 }}},
                { "match": { "writer": {"query": "Avengers", "boost": 1 }}},
                { "match": { "production_company": {"query": "Avengers", "boost": 1 }}},
                { "match": { "description": {"query": "Avengers", "boost": 1 }}}
                ]
            }
        }
    }
```
### Use Case 2: Filters
#### Filter Only
For the second use case, the user simply needs to input the filters and they will receive 30 films which have the specifications entered. The structure uses bool with filter so that the score will not be affected if the user decides to use the filter functionality along with the query matching. Filtering simply removes the films which do not have the specifications inputted by the user and this is done with the use of the 'must'. The fields that can be filtered are genre, language, country, year, and avg_vote.
```
GET /_search
{
    "query": {
        "bool": {
            "filter": [
                {"bool": {"must": [
                {"match": {"genre": {"query": "Action, Drama"}}},
                {"match": {"language": {"query": "English"}}},
                {"match": {"country": {"query": "USA"}}}
                ]
                }},
                {"range": { "year": { "gte": 2000, "lte": 2020}}},
                {"range": { "avg_vote": { "gte": 7 }}}
                ]
            }
        }
    }
```
#### Query with Filter
```
GET /_search
{
    "query": {
        "bool": {
            "should": [
                { "match": { "original_title": {"query": "Avengers", "boost": 4 }}},
                { "match": { "actors": {"query": "Avengers", "boost": 3 }}},
                { "match": { "director": {"query": "Avengers", "boost": 3 }}},
                { "match": { "genre": {"query": "Avengers", "boost": 2 }}},
                { "match": { "country": {"query": "Avengers", "boost": 1 }}},
                { "match": { "language": {"query": "Avengers", "boost": 1 }}},
                { "match": { "writer": {"query": "Avengers", "boost": 1 }}},
                { "match": { "production_company": {"query": "Avengers", "boost": 1 }}},
                { "match": { "description": {"query": "Avengers", "boost": 1 }}}
                ],
            "filter": [
                {"bool": {"must": [
                {"match": {"genre": {"query": "Action, Drama"}}},
                {"match": {"language": {"query": "English"}}},
                {"match": {"country": {"query": "USA"}}}
                ]
                }},
                {"range": { "year": { "gte": 2000, "lte": 2020}}},
                {"range": { "avg_vote": { "gte": 7 }}}
                ]
            }
        }
    }
```
### Use Case 3:Random List
For the third use case, the user simply needs to click the 'Surprise Me' button and they will receive a list of random films. The structure replaces the match from use case 1 for easier modifications in the backend code. However, it could simply be query and then immediately the function_score. Match_all gives all documents with a score of 1, and the random_score gives it a multiplier. Through this, the films are given a score between 0-1, and they are returned in decreasing order based on the score. This can also be used along with the filtering functionality. This use case is for users who do not have a specific film in mind, but would like to find out something new.
#### Random List
```
GET /_search
{
  "query": {
    "bool": {
      "should": [
        {
          "function_score": {
            "query": { "match_all": {} },
            "random_score": {}
          }
        }
        ]
    }
  }
}
```
#### Random List with Filters
```
GET /_search
{
  "query": {
    "bool": {
      "should": [
        {
          "function_score": {
            "query": { "match_all": {} },
            "random_score": {}
          }
        }
        ],
        "filter": [
                {"bool": {"must": [
                {"match": {"genre": {"query": "Action"}}},
                {"match": {"language": {"query": "English"}}},
                {"match": {"country": {"query": "USA"}}}
                ]
                }},
                {"range": { "year": { "gte": 2000, "lte": 2020}}},
                {"range": { "avg_vote": { "gte": 7 }}}
                ]
            }
        }
    }
```

## 3. Select related similarity, scoring, and boosting methods accordingly. Describe them and provide your reasons.
- The similarity scoring used is BM25, which is derived from TF-IDF. Compared to TF-IDF, BM25 multiplies a k value and adds 1 to the TF therefore the TF score would be an asymptote curve and would take longer for the TF to reach saturation. It also compares the documents much faster as it take into account the length of the document relative to the average document length so the scoring is much faster for short documents. As relevance is always changing. It is good to use BM25 for a much robust system t handle short descriptions and such.
- Specific fields have their scores boosted because the researchers decided that certain fields are more important than others. The main focus were the title, actors, director, and genre, which were boosted by 4, 3, 3, and 2, respectively. As fellow users of film search engines, this is also true for the researchers when they try to search for films to watch. Also, popular streaming websites, like Netflix, would explicitly show 'Titles,people,genre' as help text in their search bar. However, scores are also calculated based on the similarity to the country, language, writer, production_company, and description fields, but with no boosting involved. 

## 4. Create your index, mappings, and load data.

# How good: Test and evaluate your search engine index
## 1. Test your query for each use case (information need); you may limit the number of hits for your search.
## 2. Examine the results and judge each document’s relevance in terms of the information need.
## 3. Provide a formal evaluation in terms of metrics such as precision, recall, F1,and/or nDCG.
## 4. Discuss the results. You are encouraged to try different settings and compare their results.
| Query | Type | DCG | nDCG | Recall | 
|-------|------|-----|------|--------|
|  "Avengers"     |  Title - generic    | 5.2531254248668064 | 0.8954792535685231 | 0.6 |
|   "Avengers Age of Ultron"    |  Title - specific    | 2 | 1.0 | 1 |
|     "Avengers" - 2018 |   Title - filtered   |   5.123212623289701 | 1.0 | 1 |
|     "Michael"  |   Director - generic   | 2.5616063116448506 | 1.0 | 0 |
|     "Michael Bay" - action  |   Director - filtered   |  5.735283409071832 | 0.788246835854919 | 0.7 |
|     "Anthony Hopkins"  |   Actor - specific   | 3.261859507142915 | 1.0 | 0.2 ||
|     "French Comedy"  |   Genre - specific   | 4.253327913222679 | 0.9287981500785571 | 1 |
|     "Surprise Me!" - French - Comedy |   filtered   |9.087118676176692 | 1.0 | 1 |
|     "Surprise Me!" - pre-2000 - Western - American |   filtered   |   9.087118676176692 | 1.0 | 1 |

From these overall results, we can generalize that if a user wants to search for a specific movie, it's best practice to type the whole movie title to retrieve the specific movie as in the example of 'Avengers Age of Ultron'. Generally, more spicific search queries result to higher recall as more relevant results are retrieved.
If a user wishes to get recommendations with filters applied, hitting "Surprise Me" button is a fun was to get recommendations. Precision is not calculated because it needs false negatives. it would be impossible to know which movies were not retrieved since there are millions of titles in the database. Recall is restricted to the top 10 results. In this application. Recall is the amount of relevant movies in the top 10. But for some applications where we expect a certain amount (ex. 1 specific movie title), recall is 1, as long as the movie is shown in the top spot. 
(For in depth discussion on each query and result, refer to the notebook file: INFO624-Evaluations.ipynb) 


# Where: Where is your search engine (index)? Provide the names of your indices. 
- The search engine index is located in a free trial account in Kibana Elastic Search. The indices are named faf42_movies1, faf42_movies2, faf42_movies3_, faf42_movies4, faf42_movies5, faf42_movies6, and faf42_movies7_. 

# Experiences: Discuss your team experiences working on the search engine. What works? What doesn’t? What could have been done better? What have you learned as a team? And your thoughts on future works?
- Challenges:
    - Indices seemed to have a limit of 10,000 lines and the researchers had to create 7 indices to accommodate the entirety of the dataset.
    - Mapping and settings could not be modified once initialized. New index has to be created to initialize new mapping and settings.
    - Deployment on azure did not work and the researchers had to deploy in heroku.
    - Design has to be simple yet elegant.
- Lessons:
    - Filters have no effect on scoring.
- Future work:
    - Recommended titles could be added once a specific title is clicked.
    - Boosting and query can be further enhanced for better results.

# 1.2 Code and Interface (if applicable)
- Simply visit the site: https://imdbsearchengine.herokuapp.com/, input the search query and filters, and press search.

# References
- https://www.elastic.co/guide/en/elasticsearch/reference/master/search-analyzer.html
- https://www.elastic.co/guide/en/elasticsearch/reference/master/index-modules-similarity.html
- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html
- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html
- https://https://www.imdb.com/
- https://rebeccabilbro.github.io/intro-doc-similarity-with-elasticsearch/
