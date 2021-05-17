import pandas as pd
import time

origin_time = time.time()
# 列名の指定
columns = ["施設名"]
for i in range(1, 19):
    columns.append("MDC" + str(i).rjust(2, "0"))
columns += ["全体", "件数"]


def read_excel(year):
    # エクセルからのデータの読み込み
    df = pd.read_excel(
        "C:/Users/20007/Desktop/MDC_analysis/施設ごとのMDC別データ/" + str(year) + ".xlsx",
        index_col=None)

    # 前処理
    # 不要列の削除
    delete_df = df.filter(items=["病院類型", "告示番号", "通番"])
    delete_columns = delete_df.columns
    df = df.drop(delete_columns, axis=1)
    # 列名の変更
    df.columns = columns
    # 不要行の削除
    df = df[1:]
    # 施設名の空白文字の削除
    df["施設名"] = df["施設名"].str.replace("　", "")
    df["施設名"] = df["施設名"].str.replace(" ", "")
    # MDC別・年別の実数値に変換
    for i in range(1, 19):
        mdc = "MDC" + str(i).rjust(2, "0")
        df[mdc] = df[mdc] * df["件数"]

    # Fixme: Dropの統一(簡素化のため)
    return df.drop("全体", axis=1)


# df全体をdfsとする
dfs = []

# 病院一覧をsetで持つ
hospitals = set()

# 06, 07年のデータは全件数がない＋形式が異なるので扱えない？
for i in range(2008, 2020):
    # 年ごとのデータをDF化
    df = read_excel(i)
    df = df.dropna(subset=["施設名"])
    # dfsにdfをまとめて保管
    dfs.append(df)
    # 病院一覧を更新
    hospitals = set(df["施設名"]) | hospitals
    # 経過時間管理
    t = time.time()
    print(i, str(len(df)) + "", "経過時間: " + str(t - origin_time) + " s")


# 病院一覧をリスト化
original_hospitals = [i for i in list(hospitals) if i != "Nan"]
length = len(original_hospitals)
hospitals = sorted(original_hospitals * 12)
# 各病院に対応する年度をリスト化
years = [i for i in range(2008, 2020)] * length
array = [hospitals, years]
# マルチインデックスの作成
# Todo: csvに一度保存してから改めてマルチインデックスを作成したほうが早い？
tuple = list(zip(*array))
index = pd.MultiIndex.from_tuples(tuple, names=["hospital", "year"])
# 空のdf作成
Multi_df = pd.DataFrame(index=index, columns=columns)
# 列の整理
delete_Multi_df = Multi_df.filter(items=["施設名", "全体"])
delete_columns = delete_Multi_df.columns
Multi_df = Multi_df.drop(delete_columns, axis=1)
# 一度全て0置換
Multi_df.fillna(0, inplace=True)
print(Multi_df)

# 一行ずつ置換
# df.loc[count] = pandas.DataFrame(amounts).T.loc[<column>]

for i in range(length):
    for j in range(2008, 2020):
        # print(Multi_df.loc[(original_hospitals[i], j), :])
        # print(dfs[j-2008][dfs[j-2008]["施設名"] == original_hospitals[i]])
        # Multi_df.loc[(original_hospitals[i], j), :] = (dfs[j-2008]["施設名"] == original_hospitals[i])
        # print(Multi_df.loc[(original_hospitals[i], j), :])
        # print(dfs[j-2008])
        pass

# Todo: 回帰分析後に機械学習モデルを作成し、予測
# Todo: 各疾患別のファイル読み込み
# MDC01: 神経系疾患
# MDC05: 循環器系疾患
# MDC06: 消化器系疾患、肝臓・胆道・膵臓疾患
