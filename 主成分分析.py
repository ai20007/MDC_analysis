import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# DataFrameの作成、列名の英訳
df = pd.read_csv("/Users/20007/Desktop/MDC_analysis/sanpuzu/01234/zentai.csv", encoding="cp932")
df_copy = df.iloc[:, 1:-1]
df_copy.rename(
    columns={'全件数': 'All', '男性': 'Male', '女性': 'Female', '0～2歳': '0~2', '3～5歳': '3~5',
             '6～15歳': '6~15', '16～20歳': '16~20', '21～40歳': '21~40', '41～60歳': '41~60',
             '61～79歳': '61~79', '80歳以上': '80~', '治癒・軽快': '+2', '寛解': '+1', '不変': '0',
             '増悪': '-1', '死亡': '-2', '在院日数(平均)': 'days'}, inplace=True)

# plotting.scatter_matrix(df.iloc[:, 1:], figsize=(8, 8), alpha=0.5)
# plt.show()

# 各列の標準化
dfs = df_copy.iloc[:, 1:].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
print(dfs.head())

# 主成分分析
pca = PCA()
pca.fit(dfs)
feature = pca.transform(dfs)

# 寄与率導出
print(pd.DataFrame(feature, columns=["PC{}".format(x + 1) for x in range(len(dfs.columns))]).head())

# 累積寄与率導出・描画
plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
plt.plot([0] + list(np.cumsum(pca.explained_variance_ratio_)), "-o")
plt.xlabel("Number of principal components")
plt.ylabel("Cumulative contribution rate")
plt.grid()
# plt.savefig("累積寄与率.png")
# plt.show()

# 固有値導出
print(pd.DataFrame(pca.explained_variance_ratio_,
                   index=["PC{}".format(x + 1) for x in range(len(dfs.columns))]))

# 固有ベクトル導出
print(pd.DataFrame(pca.components_, columns=df_copy.columns[1:],
                   index=["PC{}".format(x + 1) for x in range(len(dfs.columns))]))

# 第1~2(6)主成分における観測変数の寄与度を描画
plt.figure(figsize=(6, 6))
for x, y, name in zip(pca.components_[0], pca.components_[1], df_copy.columns[1:]):
    plt.text(x, y, name)
plt.scatter(pca.components_[0], pca.components_[1], alpha=0.8)
plt.grid()
plt.xlabel("PC1")
plt.ylabel("PC2")
# plt.savefig("主成分分析12.png")
# plt.show()

# plt.figure(figsize=(6, 6))
# for x, y, name in zip(pca.components_[2], pca.components_[3], df_copy.columns[1:]):
#     plt.text(x, y, name)
# plt.scatter(pca.components_[2], pca.components_[3], alpha=0.8)
# plt.grid()
# plt.xlabel("PC3")
# plt.ylabel("PC4")
# plt.savefig("主成分分析34.png")
# plt.show()

# plt.figure(figsize=(6, 6))
# for x, y, name in zip(pca.components_[4], pca.components_[5], df_copy.columns[1:]):
#     plt.text(x, y, name)
# plt.scatter(pca.components_[4], pca.components_[5], alpha=0.8)
# plt.grid()
# plt.xlabel("PC5")
# plt.ylabel("PC6")
# plt.savefig("主成分分析56.png")
# plt.show()

# 第1,2主成分で取り直したときの散布図描画
df_new = pca.inverse_transform(feature)
plt.figure(figsize=(6, 6))
plt.scatter(dfs.iloc[:, 0], dfs.iloc[:, 1], alpha=0.2)
plt.scatter(df_new[:, 0], df_new[:, 1], alpha=0.8)
plt.axis("equal")
# plt.savefig("主成分分析後12.png")
# plt.show()

# 取り直したものに対してクラスタリング
sc = preprocessing.StandardScaler()
sc.fit(df_new)
X_norm = sc.transform(df_new)
cls = KMeans(n_clusters=3, verbose=True, random_state=0).fit_predict(X_norm)
cls_ = KMeans(n_clusters=3, verbose=True, random_state=0)
result = cls_.fit(X_norm)
plt.scatter(X_norm[:, 0], X_norm[:, 1], c=result.labels_)
plt.scatter(result.cluster_centers_[:, 0], result.cluster_centers_[:, 1], s=250, marker='*',
            c='red')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()
plt.savefig("主成分分析後クラスタリング.png")

# 相関係数の導出
PC1 = list(X_norm[:, 0])
PC2 = list(X_norm[:, 1])
s1 = pd.Series(PC1)
s2 = pd.Series(PC2)
res = s1.corr(s2)
print("相関係数:", res)

# 黄色クラス(2)の疾病を表示
ans = list(np.where(cls == 2))
for i in ans:
    print(df["分類名称"][i])
