import os

from flask import Flask, request
from flask_cors import CORS, cross_origin
from datetime import datetime
from workflow import workflow

import json
import logging
import numpy as np
import threading
import hashlib

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_url_path='', static_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", 'www', 'public')))
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/')
def root():
    return serve_static("index.html")

sessions = {}

def run(query, sid):
    start = datetime.now().microsecond
    data = workflow(query)
    end = datetime.now().microsecond
    data["sid"] = sid
    delta = (end - start) / 1000
    data["ms"] = delta
    sessions[sid] = data
    logging.info(f"Query {query} in {delta}ms")

def convert(o):
    if isinstance(o, np.generic): return o.item()  
    raise TypeError

@app.route('/status')
@cross_origin()
def status():
    sid = request.args.get("sid")
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
    t = threading.Thread(target=run, args=(query,sid,))
    t.start()
    return sid

if __name__ == "__main__":
    #app.debug = True
    app.run(port=18080)