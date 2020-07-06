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
import logging

#Collect RSS feeds
def get_texts(rss_file):
    logging.info(f"Opening file {rss_file}")
    f = open(os.path.join(sys.path[0], rss_file))

    #ElasticSearch client setup
    es=Elasticsearch([{'host':'localhost','port':9200}])

    #Loop over RSS feeds to collect urls
    links = []
    for line in f.readlines():
        url = line.strip()
        logging.info(f"Processing {url}")
        d = feedparser.parse(url)
        for item in d["entries"]:
            try:
                link = item["link"]
                logging.info(f"Collected {link}")
                links.append(link)
            except Exception as e:
                logging.warn(e)
    #Extracting links
    for elem in links:
        try:
            #Goose library clean html and extract center text
            g = Goose()
            html = g.extract(url = elem)

            title = html.title.encode('utf-8')
            logging.info(f"Extracted {title}")
            lines = html.cleaned_text.split("\n") # replace all newlines with \n
            non_empty_lines = [line for line in lines if line.strip() != ""]
            clean_text = ""
            for line in non_empty_lines:
                clean_text += line + "\n"
            clean_text = clean_text.replace('"', '\"') # replace all " with \"
            logging.info(f"NLP processing {title}")
            url = "http://localhost:6090/v2/api/analyze"
            myobj = { "document": { "text": clean_text}, "features":["syncpos", "dependency", "userdata", "synlab"]}
            headers = {
                'Content-Type': 'application/json'
            }
            x = requests.request("POST", url, headers=headers, data = json.dumps(myobj)) # encoding utf 8?
            js_response = x.text

            id = hashlib.sha1(title).hexdigest()
            logging.info(f"Storing {title}")

            es.index(index='internship_jsons',doc_type='json',id=id,body=js_response)
        except Exception as e:
            logging.error(e)
    logging.info(f"RSS {rss_file} completed")


if __name__ == "__main__":
    logo = """
    
  ____  ____ ____     ____      _ _           _             
 |  _ \/ ___/ ___|   / ___|___ | | | ___  ___| |_ ___  _ __ 
 | |_) \___ \___ \  | |   / _ \| | |/ _ \/ __| __/ _ \| '__|
 |  _ < ___) |__) | | |__| (_) | | |  __/ (__| || (_) | |   
 |_| \_\____/____/   \____\___/|_|_|\___|\___|\__\___/|_|   
                                                            

    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info(logo)
    get_texts("rss-game.txt")