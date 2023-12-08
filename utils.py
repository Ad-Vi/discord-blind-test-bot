import math
import os
import csv

def create_index():
    file_path = 'index.csv'

    # Check if the file already exists
    if not os.path.exists(file_path):
        # Create the file if it does not exist
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

def tfidf(string, word):
    c = string.count(word)
    tf = c / len(string.split())
    idf = math.log(len(string.split(" ")) / c)
    return tf * idf
def normalize_tfidf(string):
    words = string.split()
    tfidf_sum = sum(tfidf(string, word) for word in words)
    normalized_tfidf = [tfidf(string, word) / tfidf_sum for word in words]
    return normalized_tfidf
def normalized_tdidf(string, word):
    return normalize_tfidf(string)[string.split().index(word)]
def compute_score(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    
    words1 = str1.split()
    words2 = str2.split()
    if len(words1) == 1:
        w1 = words1[0]
        for w2 in words2:
            if w1 == w2:
                return 1/len(words2)
    if len(words1) > len(words2):
        tmp = words1
        words1 = words2
        words2 = tmp
    count = 0
    for word in words1:
        if word in words2:
            count += normalized_tdidf(str1, word)
    return count