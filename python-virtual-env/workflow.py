from elasticsearch import Elasticsearch

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

from sklearn.metrics import silhouette_score

import numpy as np
import requests
import json
import logging

es_host = "localhost"
es_port = 9200
es_index = "internship_jsons"
es_type = "json"

## --- ELASTICSEARCH OPERATIONS --- ##
#total records in corpus
def count():
    logging.debug(f"Calculating total number of records for index {es_index}")
    res = requests.get(f"http://{es_host}:{es_port}/{es_index}/{es_type}/_count?q=*")
    ncorpus = json.loads(res.text)["count"]
    logging.debug(f"Found {ncorpus} records")
    return ncorpus

#search by query
def search(query):
    logging.debug(f"Connecting to Elastic Search")
    es = Elasticsearch([{'host': es_host, 'port': es_port}])
    body = {
        "query": {
            "simple_query_string": {
                "query": query
            }
        }
    }
    logging.debug(f"Running query {query}")
    res = es.search(index=es_index, size=1000, body=body)
    hits = res['hits']['hits']
    logging.debug(f"Found {len(hits)} records")

    jsons = []
    for hit in hits:
        jsons.append(hit['_source']['data'])
    return jsons

# --- JSON Preprocessing -- #
def preprocess(jsons):
    frequencies = {}
    contents = []
    for js in jsons:
        lemmas = [f"{token['lemma']}_{token['pos']}" for token in js['tokens'] if token["pos"] in ['NOUN','PROPN','ADJ','VERB']]
        lemmas = [lemma for lemma in lemmas if len(lemma) > 1 and not lemma.isnumeric()]
        lemmas = [lemma.lower().replace(' ', "_") for lemma in lemmas if lemma.lower() not in stopwords.words("english")]
        for lemma in lemmas:
            f = frequencies.get(lemma) or 0
            frequencies[lemma] = f + 1
        contents.append(" ".join(lemmas))
    return contents, frequencies

# --- TF-IDF --- #
def tfidf(contents):
    vec = TfidfVectorizer()
    vec.fit(contents)
    features = vec.transform(contents)
    return features, list(vec.vocabulary_.keys())

def tfidfVocab(features, vocab):
    tfidfs = {}
    rows = features.shape[0]
    cols = features.shape[1]
    features = features.toarray()
    max = 0.0
    for col in range(0,cols):
        _tfidf = 0.0
        for row in range(0,rows):
            _tfidf = _tfidf + features[row][col]
        score = _tfidf / rows
        if score > max:
            max = score
        tfidfs[vocab[col]] = score
    for k,v in tfidfs.items():
        tfidfs[k] = v / max
    return tfidfs

# --- NON-NEGATIVE MATRIX FACTORIZATION --- #
def _NMF(features):
    nmf = NMF(n_components=20, solver="mu")
    W = nmf.fit_transform(features)
    H = nmf.components_
    return W,H

# --- Clustering -- #
def get_best_clusterings(nmf, min_clusters=2, max_clusters=10):
    logging.info("Running k-means best clusters number")
    k_means_x = []
    k_means_y = []
    for i in range(min_clusters, max_clusters):
        kmeans_point = KMeans(n_clusters=i).fit(nmf)
        preds = kmeans_point.fit_predict(nmf)
        x = i  # x-value = Number of clusters
        k_means_x.append(x)
        y = silhouette_score(nmf, preds)  # y-value = Silhouette Score
        k_means_y.append(y)

    logging.info("Running HAC best clusters number")
    hierarchical_agglomerative_x = []
    hierarchical_agglomerative_y = []
    for i in range(min_clusters, max_clusters):
        hierarchical_agglomerative_point = AgglomerativeClustering(n_clusters=i).fit(nmf)
        preds = hierarchical_agglomerative_point.fit_predict(nmf)
        x = i  # x-value = Number of clusters
        hierarchical_agglomerative_x.append(x)
        y = silhouette_score(nmf, preds)  # y-value = Silhouette Score
        hierarchical_agglomerative_y.append(y)

    logging.info("Running LDA best clusters number")
    latent_dirichlet_allocation_x = []
    latent_dirichlet_allocation_y = []
    for i in range(min_clusters, max_clusters):
        latent_dirichlet_allocation_point = LatentDirichletAllocation(n_components=i).fit(nmf)  # Create LDA
        x = i  # x-value = Number of components or topics
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

def run_kmeans(data, n_clusters):
    logging.info(f"Running K-Means with {n_clusters} clusters")
    k_means = KMeans(n_clusters=n_clusters).fit_predict(data)
    return k_means

def run_hac(data, n_clusters):
    logging.info(f"Running HAC {n_clusters} clusters")
    hac = AgglomerativeClustering(n_clusters=n_clusters).fit_predict(data)
    return hac

def run_lda(data, n_clusters):
    logging.info(f"Running LDA with {n_clusters} clusters")
    kmeans_helper = KMeans(n_clusters=n_clusters)
    lda_point = LatentDirichletAllocation(n_components=n_clusters).fit_transform(X=data)  # Create lda and fit transform it into out_lda using nmf as the dataset
    lda = kmeans_helper.fit_predict(lda_point)
    return lda

# --- VIZ --- #
def viz(data):
    random_state = 0
    pca = PCA(n_components=2, random_state=random_state)
    reduced_features = pca.fit_transform(data)
    return reduced_features

def render(vocab, features_xy, frequencies, tfidfs, kmeans, hac, lda):
    output = []
    for i in range(0,len(vocab)):
        lemma = vocab[i]
        f = frequencies.get(lemma)
        tfidf = tfidfs.get(lemma)
        if tfidf is not None and f is not None and f > 2 and tfidf > 0.05:
            output.append({
                "lemma": lemma,
                "frequency": f,
                "score": tfidf,
                "x": features_xy[i][0],
                "y": features_xy[i][1],
                "kmeans": kmeans[i],
                "hac": hac[i],
                "lda": lda[i]
            })
    return output

# --- WORKFLOW --- #
def workflow(query):
    ncorpus = count()
    jsons = search(query)
    contents, frequencies = preprocess(jsons)
    features, vocab = tfidf(contents)
    tfidfs = tfidfVocab(features, vocab)
    W,H = _NMF(features)
    H = np.transpose(H)
    best_kmeans, best_hac, best_lda = get_best_clusterings(H, int(ncorpus/40), int(ncorpus/40) + 5)
    kmeans = run_kmeans(H, best_kmeans)
    hac = run_hac(H, best_hac)
    lda = run_lda(H, best_lda)
    features_xy = viz(H)
    output = render(vocab, features_xy, frequencies, tfidfs, kmeans, hac, lda)
    logging.info("Process over")
    return {
        "ncorpus": ncorpus,
        "nserp": len(jsons),
        "data": output
    }
