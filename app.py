import json
import flask
from flask import Flask, request
import pandas as pd
from elasticsearch import Elasticsearch
import pickle
from datetime import datetime
import search_file
import script

es = Elasticsearch()

app = Flask(__name__)


@app.route('/')
def search_page():
    filename = open('static/mammals_europe.txt')
    df = pd.read_table(filename)
    df = df.iloc[:, :-1]
    df = df.iloc[:-1, :]
    return flask.render_template('user_interface.html',
                                 tables=[df.to_html(classes='data')])


@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        user_query = request.form['search']
        search_query = search_file.search_query(user_query)
        hits = search_query['hits']['hits']
        #display scores
        scores = []
        for hit in hits:
            score={
                "Score": hit["_score"],
                "Name": hit["_source"]["name"],
                "Title": hit["_source"]["title"]
            }
            scores.append(score)
        if len(scores) == 0:
            data = {'Data':'No Results found'}
            df=pd.DataFrame(data, index=[0])
        else:
            df = pd.DataFrame(scores)

        # display links
        if len(scores) == 0:
            links=["No links for this query"]
        else:
            a_ids=[]
            links=[]
            for hit in hits:
                a_id = hit['_source']['archive_id']
                a_ids.append(a_id)
            for item in a_ids:
                links.append('https://www.ncbi.nlm.nih.gov/bioproject/'+item)

        # Sister query
        sister_query = search_file.find_name_pair(user_query)
        sister_query_search = search_file.search_query(sister_query)
        newhits = sister_query_search['hits']['hits']
        newscores = []
        for newhit in newhits:
            score={
                "Score": newhit["_score"],
                "Name": newhit["_source"]["name"],
                "Title": newhit["_source"]["title"]
            }
            newscores.append(score)
        if len(newscores) == 0:
            data = {'Data':'No Results found'}
            df2=pd.DataFrame(data, index=[0])
        else:
            df2 = pd.DataFrame(newscores)

        # display links
        if len(newscores) == 0:
            newlinks=["No links for this query"]
        else:
            a_ids2=[]
            newlinks=[]
            for newhit in newhits:
                a_id2 = newhit['_source']['archive_id']
                a_ids2.append(a_id2)
            for item in a_ids2:
                newlinks.append('https://www.ncbi.nlm.nih.gov/bioproject/'+item)

    return flask.render_template('results.html',
                                 query=user_query,
                                 tables=[df.to_html(classes='data')],
                                 search_query=search_query,
                                 links=links,
                                 sister_query=sister_query,
                                 newtables=[df2.to_html(classes='data')],
                                 newlinks=newlinks)


@app.route('/data')
def data():
    pickle_in = open("static/movie_list_paras_full.pickle","rb")
    movies = pickle.load(pickle_in)
    return flask.render_template('experimental.html',
                                 data=movies)


@app.route('/experimental')
def experiment():
    index = search_file.create_index()
    return flask.render_template("nested.html",
                                 nest=index)


if __name__ == '__main__':
    app.run()

