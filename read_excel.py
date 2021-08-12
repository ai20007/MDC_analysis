import pandas as pd

# 列名の指定
columns = ["施設名", "年度"]
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
    # 年度列の追加
    df.insert(1, "年度", year)
    # 列名の変更
    df.columns = columns
    # 不要行の削除
    df = df[1:]
    # 施設名の空白文字の削除
    df["施設名"] = df["施設名"].str.replace("　", "")
    df["施設名"] = df["施設名"].str.replace(" ", "")
    # 病院==""の行を削除
    df = df.dropna(subset=["施設名"])
    # MDC別・年別の実数値に変換
    for i in range(1, 19):
        mdc = "MDC" + str(i).rjust(2, "0")
        df[mdc] = df[mdc] * df["件数"]
    # 全体列の削除(ここじゃないとうまく動かない)
    return df.drop("全体", axis=1)


# df全体をdfsとする
dfs = pd.DataFrame()

# 06, 07年のデータは全件数がない＋形式が異なるので扱えない？
for i in range(2008, 2020):
    # 年ごとのデータをDF化
    df = read_excel(i)
    # dfsにdfをまとめて保管
    dfs = pd.concat([dfs, df])

# 年度→施設名でソート
dfs = dfs.sort_values(["施設名", "年度"])
# indexを振り直す
dfs.reset_index(inplace=True, drop=True)
# .csvに保存
dfs.to_csv("to_csv_out.csv", encoding="cp932")
