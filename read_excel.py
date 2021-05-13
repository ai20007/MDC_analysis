import pandas as pd

# 列名の指定
columns = ["施設名"]
for i in range(1, 19):
    columns.append("MDC" + str(i).rjust(2, "0"))
columns += ["全体", "件数"]
# print(columns)


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

    # print(df.head())
    # print(len(df))
    return df


# 病院一覧をsetで持つ
hospitals = set()

# 年ごとのデータをDF化
# 06, 07年のデータは全件数がない＋形式が異なるので扱えない？
for i in range(2008, 2020):
    # 病院一覧を更新
    df = read_excel(i)
    hospitals = set(df["施設名"]) | hospitals

# ”nan”を消去
hospitals.discard("nan")

print(len(hospitals))

# Todo: MDCごとに修正
# Todo: 回帰分析後に機械学習モデルを作成し、予測
# Todo: 各疾患別のファイル読み込み
# MDC01: 神経系疾患
# MDC05: 循環器系疾患
# MDC06: 消化器系疾患、肝臓・胆道・膵臓疾患
