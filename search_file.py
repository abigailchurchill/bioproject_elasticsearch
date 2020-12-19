from elasticsearch import Elasticsearch
import pickle,heapq
import json
import pandas as pd

es = Elasticsearch()
global res


# Uses the JSON file with the edited dataset(see script.py).
# File contains the archive data for project records - archive ID, name, title and description.
# Creates new Elasticsearch index, one record at a time. The resulting index is returned.

def create_index():
    res = None

    with open('static/changed_dataset.json') as f:
        archives = json.loads(f.read())

    count = 1

    if es.indices.exists(index="archives_new"):
        return res

    print(len(archives))
    for archive in archives:
        res = es.index(index="archives_new", id=count, body=archive)
        count += 1

    print("Finished indexing")
    es.indices.refresh(index="archives_new")

    return res


# The search query is processed and a match phrase process is conducted using the ES search API.

def search_query(user_query):
    create_index()
    res = es.search(index="archives_new", size = 100,
                    body={"query":{
                        "multi_match" : {
                            "query": user_query,
                            "type": "phrase",
                            "fields": [ "title", "name", "description" ]
                        }
        }})

    return res


def find_name_pair(user_query):
    filename = open('static/mammals_europe.txt')
    df = pd.read_table(filename)
    df = df.iloc[:, :-1]
    df = df.iloc[:-1, :]
    dictionary = df.set_index('Scientific name')['English name'].to_dict()

    pair = ''
    for key, value in dictionary.items():
        if user_query == key:
            pair = value
        if user_query == value:
            pair = key

    return pair


# Delete the index
def delete_index():
    es.indices.delete(index='archives_new')
    print("Existing index has been deleted. Index again.")



