import feedparser
import os
import sys
import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
from goose3 import Goose
from elasticsearch import Elasticsearch
import time

def get_texts(URL, folder_name):
    os.chdir(sys.path[0])
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    os.chdir(folder_name)

    links = []
    d = feedparser.parse(URL)
    for item in d["entries"]:
        try:
            link = item["link"]
            links.append(link)
        except Exception as e:
            print(e)
    
    for elem in links:
        try:
            g = Goose()
            html = g.extract(url = elem)
            
            final_dict = {}
            final_dict["url"] = html.final_url
            final_dict["title-of-article"] = html.title
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            final_dict["time-stamp"] = timestamp
            final_dict["content"] = html.cleaned_text
            jsonD = json.dumps(final_dict, indent = 3)
            title = html.title.encode('utf-8')
            id = hashlib.sha1(title).hexdigest()
        

            f = open("document-%s.json" % id, 'w')
            f.write(jsonD)
            f.close()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    folder = 'internship_test'
    f = open(os.path.join(sys.path[0], "rss-game.txt"))
    for line in f.readlines():
        try:
            url = line.strip()
            get_texts(url, folder)
        except Exception as e:
            print(e)