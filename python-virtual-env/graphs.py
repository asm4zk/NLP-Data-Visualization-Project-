import get_documents
import os
import sys
import re
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import NMF
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def first_graph(word):
    """
    Get values of tfidf for relevant documents
    """

    es = Elasticsearch([{'host':'localhost','port':9200}])
    res = es.search(index='internship_jsons', doc_type='json', size=1000)

    hits = res['hits']['hits']

    jsons = []
    for hit in hits:
        jsons.append(hit['_source']['data'])

    d = {}

    tfidf = get_documents.TFIDF(jsons)
    relevant_documents = get_documents.get_associated_documents(tfidf, word)

    relevant_jsons = []
    for document in relevant_documents:
        relevant_jsons.append(jsons[document[0] + 1])
    
    relevant_tfidf = get_documents.TFIDF(relevant_jsons)

    coordinates_data_frame = data_frame_nmf_documents(relevant_tfidf)

    for document in relevant_documents:
        d2 = {}
        if document == relevant_documents[0]:
            d2["Title"] = document[0]
            d2["TFIDF"] = document[1][0]
            for index, row in coordinates_data_frame.iterrows():
                if row["json"] == document[0]:
                    d2["x"] = row["principal component 1"]
                    d2["y"] = row["principal component 2"]
                    break
            d2["Main Lemmas"] = hits[document[0]]['_source']['data']['mainLemmas']
            d[word] = [d2]
        else:
            d2["Title"] = document[0]
            d2["TFIDF"] = document[1][0]
            for index, row in coordinates_data_frame.iterrows():
                if row["json"] == document[0]:
                    d2["x"] = row["principal component 1"]
                    d2["y"] = row["principal component 2"]
            d2["Main Lemmas"] = hits[document[0]]['_source']['data']['mainLemmas']
            d[word].append(d2)
    
    f = open("first_graph.json", "w")
    f.write(str(d))
    f.close()

    return d

def data_frame_nmf_documents(X):
    jsons = X[:,0] # Get list of titles
    jsons = np.delete(jsons, 0, 0) # Remove empty corner space
    X = np.delete(X, 0, 1) # Delete the list of titles
    words = X[0,:] # Get the list of words
    X = np.delete(X, 0, 0) # Delete the list of words
    X = X.astype('float') # Change type to float as there are only floats left

    d = {} # Create new dictionary to create the data frame with pandas. Get words one by one as the keys and the list of frequencies per document as the values
    for word in words:
        d[word] = X[:,0]
        X = np.delete(X, 0, 1)
    d["json"] = jsons # Add the jsons titles at the end of the dictionary

    data_frame = pd.DataFrame(d) # Create the data frame with pandas

    x = data_frame.loc[:, words].values # Separate out the words

    data = StandardScaler().fit_transform(x) # Standardize the words with the sklearn library

    lowest = np.amin(data) # Get minimum value in data

    for x in np.nditer(data, op_flags=['readwrite']): # Translate every value in data into a positive value by adding the absolute value of the lowest, keeping the distance between values
        x[...] += abs(lowest)

    nmf = NMF(n_components=2) # Create a 2-dimension nmf using the nmf method in the sklearn library

    principalComponents = nmf.fit_transform(data) # Get the standardized data and put it in the nmf

    principal_data_frame = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2']) # Create new data frame with the new adjustments

    final_data_frame = pd.concat([principal_data_frame, data_frame[['json']]], axis = 1) # Add the json titles at then end of the data frame

    return final_data_frame

def second_graph(word):
    """
    Get values of tfidf for relevant documents
    """

    es = Elasticsearch([{'host':'localhost','port':9200}])
    res = es.search(index='internship_jsons', doc_type='json', size=1000)

    hits = res['hits']['hits']

    jsons = []
    for hit in hits:
        jsons.append(hit['_source']['data'])

    d = {}

    tfidf = get_documents.TFIDF(jsons)
    relevant_documents = get_documents.get_associated_documents(tfidf, word)

    relevant_jsons = []
    for document in relevant_documents:
        relevant_jsons.append(jsons[document[0] + 1])
    
    relevant_tfidf = get_documents.TFIDF(relevant_jsons)
    
    coordinates_data_frame = data_frame_nmf_words(relevant_tfidf)

    relevant_words = []
    for term in range(len(relevant_tfidf[0])):
        if term != 0:
            relevant_words.append(relevant_tfidf[0][term])

    d[word] = []
    for index, row in coordinates_data_frame.iterrows():
        d2 = {}
        d2["Word"] = row["json"]
        d2["x"] = row["principal component 1"]
        d2["y"] = row["principal component 2"]
        d[word].append(d2)
    
    f = open("second_graph.json", "w")
    f.write(str(d))
    f.close()

    return d


def data_frame_nmf_words(X):
    X = np.transpose(X)
    jsons = X[:,0] # Get list of titles
    jsons = np.delete(jsons, 0, 0) # Remove empty corner space
    X = np.delete(X, 0, 1) # Delete the list of words
    words = X[0,:] # Get the list of words
    X = np.delete(X, 0, 0) # Delete the list of titles
    X = X.astype('float') # Change type to float as there are only floats left

    d = {} # Create new dictionary to create the data frame with pandas. Get words one by one as the keys and the list of frequencies per document as the values
    for word in words:
        d[word] = X[:,0]
        X = np.delete(X, 0, 1)
    d["json"] = jsons # Add the jsons titles at the end of the dictionary

    data_frame = pd.DataFrame(d) # Create the data frame with pandas

    x = data_frame.loc[:, words].values # Separate out the words

    data = StandardScaler().fit_transform(x) # Standardize the words with the sklearn library

    lowest = np.amin(data) # Get minimum value in data

    for x in np.nditer(data, op_flags=['readwrite']): # Translate every value in data into a positive value by adding the absolute value of the lowest, keeping the distance between values
        x[...] += abs(lowest)

    nmf = NMF(n_components=2) # Create a 2-dimension nmf using the nmf method in the sklearn library

    principalComponents = nmf.fit_transform(data) # Get the standardized data and put it in the nmf

    principal_data_frame = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2']) # Create new data frame with the new adjustments

    final_data_frame = pd.concat([principal_data_frame, data_frame[['json']]], axis = 1) # Add the json titles at then end of the data frame

    return final_data_frame

if __name__ == "__main__":
    second_graph("command")
