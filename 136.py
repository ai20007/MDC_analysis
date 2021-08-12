# 2008年から2019年

import glob
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd
import pandas.io.sql as psql
import sqlite3
import sys

dpath = os.path.dirname(sys.argv[0])
db = "test.db"  # 加工前DataBase
db2 = "test2.db"  # 加工後DataBase


class DBAccess():
    def __init__(self, **kwargs):
        self.conn = sqlite3.connect(os.path.join(dpath, db))
        self.c = self.conn.cursor()
        self.disconnect()

    def connect(self):
        self.conn = sqlite3.connect(os.path.join(dpath, db))
        self.c = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    # DataBaseのtable作成
    def table_create(self, df_name, table_name):
        self.connect()
        df_name.to_sql(table_name, self.conn)

    # tableデータのDataFrame化
    def table_connect(self, table_name):
        self.connect()
        df = psql.read_sql('select * from {}'.format(table_name), self.conn)
        return df


class DB2Access():
    def __init__(self, **kwargs):
        self.conn = sqlite3.connect(os.path.join(dpath, db2))
        self.c = self.conn.cursor()
        self.disconnect()

    def connect(self):
        self.conn = sqlite3.connect(os.path.join(dpath, db2))
        self.c = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    # DataBaseのtable作成
    def table_create(self, df_name, table_name):
        self.connect()
        df_name.to_sql(table_name, self.conn)
        self.disconnect()

    # tableデータのDataFrame化
    def table_connect(self, table_name):
        self.connect()
        df = psql.read_sql('select * from {}'.format(table_name), self.conn)
        return df


# classのインスタンス化
db2_acc = DB2Access()
# DCリストの定義
dc_list = ["神経系疾患", "眼科系疾患", "耳鼻咽喉科系疾患", "呼吸器系疾患",
           "循環器系疾患", "消化器系疾患、肝臓・胆道・膵臓疾患",
           "筋骨格系疾患", "皮膚・皮下組織の疾患", "乳房の疾患",
           "内分泌・栄養・代謝に関する疾患", "腎・尿路系疾患及び男性生殖器系疾患",
           "女性生殖器系疾患及び産褥期疾患・異常妊娠分娩", "血液・造血器・免疫臓器の疾患",
           "新生児疾患、先天性奇形", "小児疾患", "外傷・熱傷・中毒", "精神疾患", "その他"]
# 全体リストの定義
D = pd.DataFrame(index=[], columns=[])

for i in range(17):
    # テーブル名の指定
    df = db2_acc.table_connect(dc_list[i])
    # score列の追加
    df["score"] = (df["寛解"] * 0.1 + df["不変"] * 0.3 + df["増悪"] * 0.6) / df["全件数"]
    # 散布図の作成
    plt.figure()
    df.plot.scatter(x="全件数", y="score")
    plt.savefig("/Users/20007/Desktop/MDC_analysis/sanpuzu/" + dc_list[i] + ".png")
    plt.close("all")
    # 各軸のワースト5を列挙
    print(dc_list[i])
    print("件数ワースト5")
    print(df.nlargest(5, "全件数"))
    print("scoreワースト5")
    print(df.nlargest(5, "score"))
    # 全体リストの更新
    D = pd.concat([D, df], axis=0)

# 一旦保存
D_r = D.reset_index(drop=True)
D_r.to_csv("/Users/20007/Desktop/MDC_analysis/sanpuzu/zentai.csv", encoding = "cp932")

print(D_r)

# 散布図の作成
plt.figure()
D_r.plot.scatter(x="全件数", y="score")
plt.savefig("/Users/20007/Desktop/MDC_analysis/sanpuzu/zentai.png")
plt.close("all")

# 各軸のワースト5を列挙
print("全体")
print("件数ワースト10")
print(D_r.nlargest(10, "全件数"))
print("scoreワースト10")
print(D_r.nlargest(10, "score"))
