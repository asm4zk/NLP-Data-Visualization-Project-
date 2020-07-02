import get_documents
import os
import sys
import re
import json
import numpy as np
import pandas as pd
import gensim.corpora as corpora
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from gensim.models import CoherenceModel

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

    nmf = coordinates_data_frame.drop('json', axis=1)
    (best_k_means, best_HA, best_LDA) = get_best_clusterings(coordinates_data_frame)

    k_means = KMeans(n_clusters=best_k_means).fit_predict(nmf)

    best_hierarchical = AgglomerativeClustering(n_clusters = best_HA).fit_predict(nmf)

    kmeans_helper = KMeans(n_clusters = best_LDA) # Create K-means
    lda_point = LatentDirichletAllocation(n_components = best_LDA).fit_transform(X=nmf) # Create lda and fit transform it into out_lda using nmf as the dataset
    LDA = kmeans_helper.fit_predict(lda_point) # Use the fit_predict method in kmeans to get a value for the lda

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
            d2["k-means"] = k_means[0]
            k_means = np.delete(k_means, 0)
            d2["Hierarchical Agglomerative"] = best_hierarchical[0]
            best_hierarchical = np.delete(best_hierarchical, 0)
            d2["LDA"] = LDA[0]
            LDA = np.delete(LDA, 0)
            d[word] = [d2]
        else:
            d2["Title"] = document[0]
            d2["TFIDF"] = document[1][0]
            for index, row in coordinates_data_frame.iterrows():
                if row["json"] == document[0]:
                    d2["x"] = row["principal component 1"]
                    d2["y"] = row["principal component 2"]
            d2["Main Lemmas"] = hits[document[0]]['_source']['data']['mainLemmas']
            d2["k-means"] = k_means[0]
            k_means = np.delete(k_means, 0)
            d2["Hierarchical Agglomerative"] = best_hierarchical[0]
            best_hierarchical = np.delete(best_hierarchical, 0)
            d2["LDA"] = LDA[0]
            LDA = np.delete(LDA, 0)
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
    
    nmf = coordinates_data_frame.drop('json', axis=1)
    (best_k_means, best_HA, best_LDA) = get_best_clusterings(coordinates_data_frame)

    k_means = KMeans(n_clusters=best_k_means).fit_predict(nmf)

    best_hierarchical = AgglomerativeClustering(n_clusters = best_HA).fit_predict(nmf)

    kmeans_helper = KMeans(n_clusters = best_LDA) # Create K-means
    lda_point = LatentDirichletAllocation(n_components = best_LDA).fit_transform(X=nmf) # Create lda and fit transform it into out_lda using nmf as the dataset
    LDA = kmeans_helper.fit_predict(lda_point) # Use the fit_predict method in kmeans to get a value for the lda

    d[word] = []
    for index, row in coordinates_data_frame.iterrows():
        d2 = {}
        d2["Word"] = row["json"]
        d2["x"] = row["principal component 1"]
        d2["y"] = row["principal component 2"]
        d2["k-means"] = k_means[0]
        k_means = np.delete(k_means, 0)
        d2["Hierarchical Agglomerative"] = best_hierarchical[0]
        best_hierarchical = np.delete(best_hierarchical, 0)
        d2["LDA"] = LDA[0]
        LDA = np.delete(LDA, 0)
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


def get_best_clusterings(nmf, test_clusters=10):
    """
    Return the best number of clusters for K-means, Hierarchical Agglomerative, and LDA clusterings
    """
    nmf = nmf.drop('json', axis=1) # Drop the json column

    k_means_x = []
    k_means_y = []
    for i in range(2, test_clusters):
        kmeans_point = KMeans(n_clusters = i).fit(nmf)
        preds = kmeans_point.fit_predict(nmf)
        x = i # x-value = Number of clusters
        k_means_x.append(x)
        y = silhouette_score(nmf, preds) # y-value = Silhouette Score
        k_means_y.append(y)

    hierarchical_agglomerative_x = []
    hierarchical_agglomerative_y = []
    for i in range(2, test_clusters):
        hierarchical_agglomerative_point = AgglomerativeClustering(n_clusters = i).fit(nmf)
        preds = hierarchical_agglomerative_point.fit_predict(nmf)
        x = i # x-value = Number of clusters
        hierarchical_agglomerative_x.append(x)
        y = silhouette_score(nmf, preds) # y-value = Silhouette Score
        hierarchical_agglomerative_y.append(y)
    
    latent_dirichlet_allocation_x = []
    latent_dirichlet_allocation_y = []
    for i in range(2, test_clusters):
        latent_dirichlet_allocation_point = LatentDirichletAllocation(n_components = i).fit(nmf) # Create LDA
        x = i # x-value = Number of components or topics
        latent_dirichlet_allocation_x.append(x)
        y = latent_dirichlet_allocation_point.bound_
        latent_dirichlet_allocation_y.append(y)


    k_means_index_max = np.argmax(k_means_y)
    k_means_index_max = k_means_x[k_means_index_max]


    hierarchical_agglomerative_index_max = np.argmax(hierarchical_agglomerative_y)
    hierarchical_agglomerative_index_max = hierarchical_agglomerative_x[hierarchical_agglomerative_index_max]

    lda_index_max = np.argmax(latent_dirichlet_allocation_y)
    lda_index_max = latent_dirichlet_allocation_x[lda_index_max]

    return (k_means_index_max, hierarchical_agglomerative_index_max, lda_index_max)


if __name__ == "__main__":
    first_graph("command")
    second_graph("command")
