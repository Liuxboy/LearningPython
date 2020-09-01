#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:

import multiprocessing
import threading
import json, sys
import pymongo
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


class SimilarityThread(threading.Thread):
    def __init__(self, threadID, data_array, totalSize, similarity_collection, startIndex):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data_array = data_array
        self.totalSize = totalSize
        self.similarity_collection = similarity_collection
        self.startIndex = startIndex

    def run(self):
        clacluateSimilarity(self.data_array, self.totalSize, self.similarity_collection, self.startIndex)


def clacluateDistance(txt1, txt2):
    return euclidean_distances(txt1, txt2)[0][0]


def clacluateSimilarity(data_array, totalSize, similarity_collection, startIndex):
    vectorizer = CountVectorizer()
    for idx in range(startIndex, totalSize):
        h = data_array[idx]
    for idx1 in range((idx + 1), totalSize):
        h1 = data_array[idx1]
    hSimilarity = {}
    hSimilarity['idOrigin'] = h['id']
    hSimilarity['idTarget'] = h1['id']
    corpus = []
    corpus.append(h['text'])
    corpus.append(h1['text'])
    features = vectorizer.fit_transform(corpus).todense()
    distance = clacluateDistance(features[0], features[1])
    hSimilarity['distance'] = distance
    print(hSimilarity)
    if distance < 4:
        print("Distance ====> %d " % distance)
    similarity_collection.insert_one(hSimilarity)


def processTextSimilarity(totalSize, data_array, similarity_collection):
    num_cores = multiprocessing.cpu_count()
    print(":::num cores ==> %d " % num_cores)
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
    threadID = 1
    threads = []
    rootIndex = round(totalSize / 4)
    startIndex = 0
    for tName in threadList:
        thread = SimilarityThread(threadID, data_array, startIndex + rootIndex, similarity_collection, startIndex)
        thread.start()
        startIndex += rootIndex
        threads.append(thread)
        threadID += 1
    # Wait for all threads to complete
    for t in threads:
        t.join()


def main():
    print('****** Text Similarity::start ******')
    connection = pymongo.MongoClient("mongodb://localhost")
    db = connection.kalamokomnoor
    article = db.article
    article_similarity = db.article_similarity
    data_array = article.find({}).sort("id", pymongo.ASCENDING)
    totalSize = article.count_documents({})
    print('###### :: totalSize : %d ' % totalSize)
    processTextSimilarity(totalSize, data_array, article_similarity)
    print('****** Text Similarity::Ending ******')


if __name__ == '__main__':
    main()
