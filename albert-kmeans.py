# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
import numpy as np
from albert_zh.extract_feature import BertVector

MAX_SEQ_LEN = 4
train_file_path = 'data/test_refined_word'
target_file_path = 'data/test_classified_word'
# 利用ALBERT提取文本特征
bert_model = BertVector(pooling_strategy="NONE", max_seq_len=MAX_SEQ_LEN)
f = lambda text: bert_model.encode([text])["encodes"][0]


def read_data(filePath):
    f_to_read = open(filePath,'r')
    x = []
    while True:
        line = f_to_read.readline()
        if not line:
            break
        line = line.split('\t')[0]
        x.append(line)
    return x
    pass



def input_data(filePath):
    words = read_data(filePath)
    # ALBERT ERCODING
    print("start ALBERT encding")
    x = np.array([f(word) for word in words])
    print("end ALBERT encoding")

    return x,words
    pass
def train_model():
    X,words = input_data(train_file_path)
    X = X.reshape((X.shape[0], -1))
    kmeans = KMeans(n_clusters=7, random_state=0).fit(X)
    y = kmeans.labels_.tolist()
    f_to_write = open(target_file_path,'w')
    for j in range(7):
        for i in range(len(X)):
            if y[i]==j:
                f_to_write.write(words[i]+'\t'+str(y[i])+'\n')
    f_to_write.close()
    pass

if __name__ == '__main__':
    train_model()