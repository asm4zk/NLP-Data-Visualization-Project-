import os

from flask import Flask, request
from flask import send_from_directory
app = Flask(__name__, static_url_path='', static_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", 'www', 'public')))

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/')
def root():
    return serve_static("index.html")

if __name__ == "__main__":
    #app.debug = True
    app.run()