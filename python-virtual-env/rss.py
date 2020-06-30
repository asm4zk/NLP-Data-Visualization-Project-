import feedparser
import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from goose3 import Goose
from elasticsearch import Elasticsearch
import time

def get_texts():
    f = open(os.path.join(sys.path[0], "rss-game.txt"))

    links = []
    for line in f.readlines():
        url = line.strip()
        d = feedparser.parse(url)
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
            
            # final_dict = {}
            # final_dict["url"] = html.final_url
            # final_dict["title-of-article"] = html.title
            # now = datetime.now()
            # timestamp = datetime.timestamp(now)
            # final_dict["time-stamp"] = timestamp
            # final_dict["content"] = html.cleaned_text
            # jsonD = json.dumps(final_dict, indent = 3)

            title = html.title.encode('utf-8')
            lines = html.cleaned_text.split("\n") # replace all newlines with \n
            non_empty_lines = [line for line in lines if line.strip() != ""]
            clean_text = ""
            for line in non_empty_lines:
                clean_text += line + "\n"
            clean_text = clean_text.replace('"', '\"') # replace all " with \"
            url = "http://emtest.expertsystem.us:6090/v2/api/analyze"
            myobj = { "document": { "text": clean_text}, "features":["syncpos", "dependency", "userdata", "synlab"]}
            headers = {
                'Content-Type': 'application/json'
            }
            x = requests.request("POST", url, headers=headers, data = json.dumps(myobj)) # encoding utf 8?
            js_response = x.text

            id = hashlib.sha1(title).hexdigest()

            # f = open("document-%s.json" % id, 'w')
            # f.write(jsonD)
            # f.close()

            es=Elasticsearch([{'host':'localhost','port':9200}])
            es.index(index='internship_jsons',doc_type='json',id=id,body=js_response)
        except Exception as e:
            print(e)
    print("ok")


if __name__ == "__main__":
    get_texts()