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
        if document == relevant_documents[0]:
            d2["Title"] = document[0]
            d2["TFIDF"] = document[1][0]
            d[word] = [d2]
        else:
            d2["Title"] = document[0]
            d2["TFIDF"] = document[1][0]
            d[word].append(d2)
    
    f = open("first_graph.json", "w")
    f.write(str(d))
    f.close()

    return d

if __name__ == "__main__":
    first_graph("command")
