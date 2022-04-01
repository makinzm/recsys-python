import warnings
import pprint
from fractions import Fraction

import numpy as np

warnings.simplefilter("ignore")


# 上位K件
TOP_K = 3
# スムージングパラメタ
ALPHA = 1
# クラス数
N = 2
# 各特徴量がとりうる値のユニーク数
M = [2, 2, 2, 2, 2, 2]
# しきい値
THETA = 0.5

Du = np.array([
               [1, 0, 0, 0, 1, 0, +1],
               [0, 1, 0, 0, 1, 0, +1],
               [1, 1, 0, 0, 1, 0, +1],
               [1, 0, 0, 1, 1, 0, +1],
               [1, 0, 0, 0, 0, 1, +1],
               [0, 1, 0, 1, 0, 1, +1],
               [0, 0, 1, 0, 1, 0, -1],
               [0, 0, 1, 1, 1, 0, -1],
               [0, 1, 0, 0, 1, 1, -1],
               [0, 0, 1, 0, 0, 1, -1],
               [1, 1, 0, 1, 1, 0, np.nan],
               [0, 0, 1, 0, 1, 1, np.nan],
               [0, 1, 1, 1, 1, 0, np.nan],
])
"""
あるuserにおける
item, 特徴+嗜好 の行列
"""

I = np.arange(Du.shape[0])
x = Du[:,:-1]
ru = Du[:,-1]

Iu = I[~np.isnan(ru)]
Iu_not = np.setdiff1d(I, Iu)
DuL = Du[Iu]
xL = x[Iu]
ruL = ru[Iu]
DuU = Du[Iu_not]
xU = x[Iu_not]

def P_prior(r, laplace_smoothing = 0):
    """
    評価値がrとなる事前確率を返す。

    Parameters
    ----------
    r : int
        評価値
    
    laplace_smoothing : int
        ラプラススムージングに関する設定
        0であると最尤推定
        1であるとスムージングを行い推定

    Returns
    -------
    Fraction
        事前確率
    """
    num = np.sum(ru == r) + laplace_smoothing * ALPHA
    den = np.sum(~np.isnan(ru)) + laplace_smoothing * ALPHA * N 
    prob = Fraction(num, den, _normalize=False)
    return prob

r = +1
print('P(R={:+}) = {}'.format(r, P_prior(r)))
r = -1
print('P(R={:+}) = {}'.format(r, P_prior(r)))

def P_cond(i, k, r, laplace_smoothing = 0):
    """
    評価値がrとなる条件下でアイテムiの特徴量kに関する条件付き確率を返す。

    Parameters
    ----------
    i : int
        アイテムiのID
    k : int
        特徴量kのインデックス
    r : int
        評価値
    laplace_smoothing : int
        ラプラススムージングに関する設定
        0であると最尤推定
        1であるとスムージングを行い推定

    Returns
    -------
    Fraction
        条件付き確率
    """
    num = np.sum((ru == r) & (x[:,k]==x[i,k])) + laplace_smoothing * ALPHA
    den = np.sum(ru == r) + laplace_smoothing * ALPHA * M[k]
    prob = Fraction(num, den, _normalize=False)
    return prob
    

i = 10
k = 0
r = +1
print('P(X{}=x{},{}|R={:+}) = {}'.format(k, i, k, r, P_cond(i, k, r)))
r = -1
print('P(X{}=x{},{}|R={:+}) = {}'.format(k, i, k, r, P_cond(i, k, r)))


def P(i, r, laplace_smoothing = 0):
    """
    アイテムiの評価値がrとなる確率を返す。

    Parameters
    ----------
    i : int
        アイテムiのID
    r : int
        評価値
    laplace_smoothing : int
        ラプラススムージングに関する設定
        0であると最尤推定
        1であるとスムージングを行い推定
    
    Returns
    -------
    Fraction
        事前確率
    list of Fraction
        各特徴量に関する条件付き確率
    float
        好き嫌いの確率
    """
    pp = P_prior(r, laplace_smoothing = laplace_smoothing)
    pk = [P_cond(i, k, r, laplace_smoothing = laplace_smoothing) for k in range(0, x.shape[1])]
    prob = pp * np.prod(list(map(float, pk)))
    """
    DeprecationWarning: 
        Fraction.__float__ returned non-float (type numpy.float64).
            The ability to return an instance of a strict subclass of float is deprecated,
             and may be removed in a future version of Python.
    """
    return pp, pk, prob

i = 10
r = +1
pp, pk, prob = P(i, r)
left = 'P(R={:+}|'.format(r) + ','.join(map(str, map(int, x[i]))) + ')'
right = str(pp) + '×' + '×'.join(map(str, pk))
print('{} = {} = {:.3f}'.format(left, right, prob))

r = -1
pp, pk, prob = P(i, r)
left = 'P(R={:+}|'.format(r) + ','.join(map(str, map(int, x[i]))) + ')'
right = str(pp) + '×' + '×'.join(map(str, pk))
print('{} = {} = {:.3f}'.format(left, right, prob))

def score(u, i, laplace_smoothing = 0):
    """
    スコア関数：ユーザuのアイテムiに対するスコアを返す。

    Parameters
    ----------
    u : int
        ユーザuのID（ダミー）
    i : int
        アイテムiのID
    laplace_smoothing : int
        ラプラススムージングに関する設定
        0であると最尤推定
        1であるとスムージングを行い推定

    Returns
    -------
    float
        スコア
    """
    tmp_1 = P(i, 1, laplace_smoothing = laplace_smoothing)[2]
    scr = tmp_1/(tmp_1 + P(i, -1, laplace_smoothing = laplace_smoothing)[2])
    return scr

u = 0
scores = {i: score(u, i, laplace_smoothing=1) for i in Iu_not}
print('scores = ')
pprint.pprint(scores)

def order(u, I, laplace_smoothing = 0):
    """
    順序付け関数：アイテム集合Iにおいて、ユーザu向けの推薦リストを返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    I : ndarray
        アイテム集合
    laplace_smoothing : int
        ラプラススムージングに関する設定
        0であると最尤推定
        1であるとスムージングを行い推定

    Returns
    -------
    list
        タプル(アイテムID: スコア)を要素にした推薦リスト
    """
    scores = {i: score(u, i, laplace_smoothing=laplace_smoothing) for i in I}
    scores = {i : v for i,v in scores.items() if v > THETA}
    rec_list = sorted(scores.items(), key=lambda x:x[1], reverse=True)[:TOP_K]
    return rec_list

u = 0
rec_list = order(u, Iu_not, laplace_smoothing=1)
print('rec_list = ')
for i, scr in rec_list:
    print('{}: {:.3f}'.format(i, scr))
