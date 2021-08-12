import pandas as pd
import mojimoji
import matplotlib.pyplot as plt

# データの読み込み
MDC = pd.read_csv("to_csv_out.csv", index_col=0, encoding="cp932")
# 件数==0の列と病院以外をdrop
MDC = MDC.query("0<件数<=30000")
MDC = MDC[~MDC["施設名"].str.contains("年度")]
# 全半角の表記統一
MDC["施設名"] = MDC["施設名"].apply(mojimoji.zen_to_han, kana=False)
MDC = MDC.sort_values(["施設名", "年度"])
# indexを振り直す
MDC.reset_index(inplace=True, drop=True)
#   print(MDC)
MDC.to_csv("MDC.csv", encoding="cp932")

# 各MDCの推移(実数・割合)をグラフ化
fig = plt.figure(figsize=(14.4, 4.8))
ax1 = fig.add_subplot(131, title="MDC01")
ax2 = fig.add_subplot(132, title="MDC05")
ax3 = fig.add_subplot(133, title="MDC06")
fig.savefig("sample.png")

for i in range(2008, 2020):
    per = []
    MDC_total = sum((MDC["年度"] == i) * MDC["件数"])
    for j in range(1, 19):
        num = str(j).rjust(2, "0")
        MDC_j = sum((MDC["年度"] == i) * MDC["MDC" + num])
        per.append(round(MDC_j * 100 / MDC_total, 2))
    print(per)

# Todo: 前の行と施設名が一致しない行を起点とし、そうでない次の行で値がどう変化するかを予測する。
