import matplotlib as mpl
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import sqlite3
import sys
from sklearn.cluster import KMeans

# K平均法による分類
df = pd.read_csv("/Users/20007/Desktop/MDC_analysis/sanpuzu/zentai.csv",
                 usecols=["全件数", "score"], encoding="cp932")
# データの整形
X = df[["全件数", "score"]]
sc = preprocessing.StandardScaler()
sc.fit(X)
X_norm = sc.transform(X)
# クラスタリング
# n_clusters = 4
# init = np.array([[0, 0], [0, 1], [500000, 0], [500000, 1]])
# cls = KMeans(n_clusters=n_clusters, init=init, verbose=True, random_state=0, n_jobs=-1)
cls = KMeans(n_clusters=4, verbose=True, random_state=0, n_jobs=-1)
result = cls.fit(X_norm)
# 結果を出力
plt.scatter(X_norm[:, 0], X_norm[:, 1], c=result.labels_)
plt.scatter(result.cluster_centers_[:, 0], result.cluster_centers_[:, 1], s=250, marker='*',
            c='red')
plt.show()
plt.savefig("/Users/20007/Desktop/MDC_analysis/sanpuzu/k-means.png")
plt.close("all")
