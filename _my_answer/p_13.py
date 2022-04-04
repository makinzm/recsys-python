import math
import numpy as np
np.set_printoptions(precision=3)

# 上位K件
TOP_K = 5
# 対数の底
ALPHA = 2

# テストデータ
R = np.array([
              [5, 4,      3, np.nan, 5, 4,      2,      2,      np.nan, np.nan],
              [3, 3,      3, 3,      2, np.nan, 4,      np.nan, 5,      np.nan],
              [4, np.nan, 3, 5,      4, 3,      np.nan, 3,      np.nan, np.nan],
])
U = np.arange(R.shape[0])
I = np.arange(R.shape[1])
Iu = [I[~np.isnan(R)[u,:]] for u in U]

# 推薦システムAによる推薦リスト
RA = np.array([
               [1,      np.nan, 3,      np.nan, 4,      2,      5,      np.nan, np.nan, np.nan],
               [4,      1,      np.nan, 3,      np.nan, np.nan, 5,      np.nan, 2,      np.nan],
               [np.nan, np.nan, 5,      3,      4,      2,      np.nan, 1,      np.nan, np.nan],
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
    like = R[u,Iu[u]]>=4
    recommended = RS[u,Iu[u]]<=K
    TP = np.count_nonzero(np.logical_and(like, recommended))
    FN = np.count_nonzero(np.logical_and(like, ~recommended))
    FP = np.count_nonzero(np.logical_and(~like, recommended))
    TN = np.count_nonzero(np.logical_and(~like, ~recommended))
    return TP, FN, FP, TN

u = 0
like = R>=4
print('like = \n{}'.format(like))
# 好きなアイテム : R==5
ku = [RA[u,R[u]==5][0] for u in U]
print('ku = {}'.format(ku))
MRR = 1/len(ku)*np.sum(list(map(lambda x : 1/x, ku)))
print('MRR = {:.3f}'.format(MRR))

# 各順位における適合率
precisions = []
for u in U:
    precisions_u = []
    for k in range(1, Iu[u].size+1):
        TP, FN, FP, TN = confusion_matrix(u, RA, k)
        precision_uk = TP / (TP + FP)
        precisions_u.append(precision_uk)
    precisions.append(precisions_u)
print('precisions = \n{}'.format(precisions))

ranked_R = np.array([R[u,np.argsort(RA[u])] for u in U])
print('ranked_R = \n{}'.format(ranked_R))
ranked_like = ranked_R>=4
print('ranked_like = \n{}'.format(ranked_like))
rel = np.vectorize(lambda x: 1 if x else 0)(ranked_like)
print('rel = \n{}'.format(rel))
"""
# relやprecisionsが既に綺麗な順番に並んでいるため以下のコードは誤り
APu = [
    1/np.sum(rel[u][RA[u]<=TOP_K])*\
        rel[u][RA[u]<=TOP_K]@np.array(precisions[u])[
                ((RA[u]<=TOP_K) & (~np.isnan(R[u])))[~np.isnan(R[u])]
            ]
    for u in U
]
"""
APu = np.array([
    1/np.sum(rel[u][:TOP_K])*\
        rel[u][:TOP_K]@np.array(precisions[u])[:TOP_K]
    for u in U
])
print('APu = {}'.format(APu))
MAP = APu.mean()
print('MAP = {:.3f}'.format(MAP))

Iu_rec = [I[~np.isnan(RA[u])] for u in U]

DCGu = np.array([
    np.sum(
        [
            R[u][i]/(max(1, np.log(RA[u][i])/np.log(ALPHA))) 
            for i in Iu[u]
            if RA[u][i]<=TOP_K
        ]
    )
    for u in U
])
print('DCGu = {}'.format(DCGu))
RI = np.argsort(np.argsort(np.vectorize(lambda x: 100 if np.isnan(x) else -x)(R),axis=1), axis=1)+1
print('RI = \n{}'.format(RI))
Iu_recI = np.array([I[RI[u]<=TOP_K] for u in U])
print('Iu_recI = \n{}'.format(Iu_recI))
IDCGu = np.array([np.sum(
        [R[u][i]/(max(1, np.log(RI[u][i])/np.log(ALPHA))) 
            for i in Iu_recI[u]])
    for u in U
])
print('IDCGu = {}'.format(IDCGu))
nDCGu = np.divide(DCGu,IDCGu, where = IDCGu!=0)
print('nDCGu = {}'.format(nDCGu))
nDCG = np.mean(nDCGu)
print('nDCG = {:.3f}'.format(nDCG))
