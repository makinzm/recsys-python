import numpy as np

# テストデータ
R = np.array([
              [5, 4,      3, np.nan, 5, 4,      2,      2,      np.nan, np.nan],
])
U = np.arange(R.shape[0])
I = np.arange(R.shape[1])
Iu = [I[~np.isnan(R)[u,:]] for u in U]

# 推薦システムAによる推薦リスト
RA = np.array([
               [1, 6, 3, np.nan, 4, 2, 5, 7, np.nan, np.nan],
])

# 推薦システムBによる推薦リスト
RB = np.array([
               [4, 3, 1, np.nan, 6, 7, 2, 5, np.nan, np.nan],
])

def confusion_matrix(u, RS, K):
    """
    ユーザu向け推薦リストRSの上位K件における混同行列の各値を返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    RS : ndarray
        推薦リストRS
    K : int
        上位K件

    Returns
    -------
    int
        TP
    int
        FN
    int
        FP
    int
        TN
    """
    like = np.array(R[~np.isnan(R)]>=4)
    print('like = {}'.format(like))
    recommended = np.array(RS[~np.isnan(RS)]<=K)
    print('recommended@{} = {}'.format(K, recommended))
    TP = np.count_nonzero(like & recommended)
    print('TP@{} = {}'.format(K, TP))
    FN = np.count_nonzero(like & ~recommended)
    print('FN@{} = {}'.format(K, FN))
    FP = np.count_nonzero(~like & recommended)
    print('FP@{} = {}'.format(K, FP))
    TN = np.count_nonzero(~like & ~recommended)
    print('TN@{} = {}'.format(K, TN))
    return TP, FN, FP, TN

u = 0
K = 3
TP, FN, FP, TN = confusion_matrix(u, RA, K)
print('混同行列 = \n{}'.format(np.array([[TP, FN], [FP, TN]])))

# 真のラベルの中に含まれる真の予測の割合 : おおきいほど良い
TPR = TP*K/(TP*K + FN*K)
print('TPR@{} = {:.3f}'.format(K, TPR))
# 偽のラベルの中に含まれる真の予測の割合 : 小さいほどよい
FPR = FP*K/(FP*K + TN*K)
print('FPR@{} = {:.3f}'.format(K, FPR))

# 真の予測の中に含まれる真のラベルの割合 : 大きいほどよい
precision = TP*K/(TP*K + FP*K)
print('precision@{} = {:.3f}'.format(K, precision))
# 真のラベルの中に含まれる真の予測の割合 : 大きいほどよい
recall = TP*K/(TP*K + FN*K)
print('recall@{} = {:.3f}'.format(K, recall))
# 適合率と再現率の調和平均
F1 = 2*precision*recall/(precision + recall)
print('F1@{} = {:.3f}'.format(K, F1))

