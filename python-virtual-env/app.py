import os

from flask import Flask, request
from flask import send_from_directory
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch
import json
import asyncio
import uuid 
from graphs import second_graph
import logging
import numpy as np
import threading
import requests
import hashlib 

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_url_path='', static_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", 'www', 'public')))
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/')
def root():
    return serve_static("index.html")

def process(query, sid):
    es = Elasticsearch([{'host':'localhost','port':9200}])

    res = requests.get("http://localhost:9200/internship_jsons/json/_count?q=*")
    ncorpus = json.loads(res.text)["count"]
    logging.info(f"Found {ncorpus} total documents")

    res = es.search(index='internship_jsons', size=10, doc_type='json', body={
        "query": {
            "simple_query_string": {
                "query": query
            }
        }
    })
    hits = res['hits']['hits']

    jsons = []
    for hit in hits:
        jsons.append(hit['_source']['data'])
    nserp = len(jsons)
    d = second_graph(jsons)
    new_data = []
    for item in d:
        f = item["frequency"]
        if f > 2:
            new_data.append(item)
    d = new_data
    logging.debug(d)
    sessions[sid] = {
        "ncorpus": ncorpus,
        "nserp": nserp,
        "data": d
    }

sessions = {}

def _search(query, sid):
    process(query, sid)

def convert(o):
    if isinstance(o, np.generic): return o.item()  
    raise TypeError


@app.route('/status')
@cross_origin()
def status():
    sid = request.args.get("sid")
    print(sid)
    d = sessions.get(sid)
    if d is not None:
        logging.debug(d)
        return json.dumps(d, default=convert)
    return json.dumps({})

@app.route('/search')
@cross_origin()
def search():
    query = request.args.get("query")
    sid = hashlib.md5(query.encode()).hexdigest()
    t = threading.Thread(target=_search, args=(query,sid,))
    t.start()
    return sid

if __name__ == "__main__":
    #app.debug = True
    app.run(port=18080)