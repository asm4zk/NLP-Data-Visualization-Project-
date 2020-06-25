import get_documents
import os
import sys
import json

def first_graph(word):
    """
    Get values of tfidf for relevant documents
    """
    jsons = []
    directory = (os.path.join(sys.path[0], "internship_test"))
    for j in os.listdir(directory):
        new_directory = os.path.join(directory, j)
        f = open(new_directory, encoding = "utf-8")
        info = f.read()
        data = json.loads(info)
        jsons.append(data)

    d = {}

    tfidf = get_documents.TFIDF(jsons)
    relevant_documents = get_documents.get_associated_documents(tfidf, word)

    d2 = {}
    for document in relevant_documents:
        d2[document[0]] = document[1][0]
        d[word] = d2

    return d
