import os
import json
import re
import math
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def TFIDF(list_of_json):
    ps = PorterStemmer()
    num_of_doc = len(list_of_json)
    words = []
    for j in list_of_json:
        info = j['content']
        tokenized_info = re.findall(r'\w+', info)
        for word in tokenized_info:
            word = ps.stem(word)
            if word not in words and word not in stopwords.words('english'):
                words.append(word)

    M = np.zeros((num_of_doc + 1, len(words) + 1), dtype = object)
    M[0][0] = " "
    for n in range(num_of_doc):
        title = list_of_json[n]['title-of-article']
        M[n+1][0] = title
    for n in range(len(words)):
        word = words[n]
        M[0][n+1] = word

    for n in range(num_of_doc):
        title_axis_value = n + 1
        list_of_words = re.findall(r'\w+', list_of_json[n]['content'])
        for word in list_of_words:
            word = ps.stem(word)
            if word not in stopwords.words('english'):
                for i in range(len(M[0])):
                    if M[0][i] == word:
                        word_axis_value = i
                        break
                M[title_axis_value][word_axis_value] += 1
    
    M2 = np.copy(M)
    
    N = len(M) - 1
    for i in range(len(M)):
        if i != 0:
            for j in range(len(M[i])):
                if j != 0:
                    tf = M[i][j]
                    df = 0
                    for doc in range(len(M)):
                        if doc != 0 and M[doc][j] > 0:
                            df += 1
                    M2[i][j] = tf*math.log(N/df)
    return M2

def get_associated_documents(tfidf, word):
    ps = PorterStemmer()
    word = ps.stem(word)
    if word not in tfidf[0]:
        return 0

    word_index = np.where(tfidf[0] == word)
    values = tfidf[:,word_index]
    if np.all((values == 0.0)):
        return 0
    
    documents = []
    for elem in range(len(values)):
        if elem != 0:
            if tfidf[elem][word_index] != 0:
                documents.append((tfidf[elem][0], tfidf[elem][word_index]))
    
    return documents

if __name__ == "__main__":
    jsons = []
    directory = (r"C:\Users\Francesco\internship_test")
    for j in os.listdir(directory):
        new_directory = os.path.join(directory, j)
        f = open(new_directory, encoding = "utf-8")
        info = f.read()
        d = json.loads(info)
        jsons.append(d)
    tfidf = TFIDF(jsons)
    get_associated_documents(tfidf, "command")
