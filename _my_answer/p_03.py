import pprint
from tkinter import TOP
from typing import List
import numpy as np

# 上位K件
TOP_K = 3

# あるユーザuのアイテムの評価(各行)の行列
Du = np.array([
               [5, 3, +1],
               [6, 2, +1],
               [4, 1, +1],
               [8, 5, -1],
               [2, 4, -1],
               [3, 6, -1],
               [7, 6, -1],
               [4, 2, np.nan],
               [5, 1, np.nan],
               [8, 6, np.nan],
               [3, 4, np.nan],
               [4, 7, np.nan],
               [4, 4, np.nan],
])
I = np.arange(Du.shape[0])
x = Du[:,:-1]
ru = Du[:,-1]

Iu = I[~np.isnan(ru)]
Iup = I[ru==+1]
Iun = I[ru==-1]
Iu_not = np.setdiff1d(I, Iu)

my_01 = 'x[Iu+] = \n{}'.format(Du[Iup,0:2])
# my_01 = 'x[Iu+] = \n{}'.format(x[Iup])

my_02 = 'sum(x[Iu+]) = {}'.format(x[Iup].sum(axis=0))

pu = x[Iup].sum(axis=0)/x[Iup].shape[0]

my_03 = 'pu = {}'.format(pu)

def cos(pu : np.ndarray , xi: np.ndarray) -> float:
    """
    コサイン類似度関数：ユーザプロファイルpuとアイテムiの特徴ベクトルxiのコサイン類似度を返す。

    Parameters
    ----------
    pu : ndarray
        ユーザuのユーザプロファイル
    xi : ndarray
        アイテムiの特徴ベクトル

    Returns
    -------
    float
        コサイン類似度
    """
    num = pu@xi
    #print('num = {}'.format(num)) # 04
    den_u = (pu@pu)**(1/2)
    #print('den_u = {:.3f}'.format(den_u)) # 05
    den_i = (xi@xi)**(1/2)
    #print('den_i = {:.3f}'.format(den_i)) # 06
    
    cosine = num / (den_u * den_i)
    return cosine

u = 0
i = 7
_my_03_01 = 'cos(p{}, x{}) = {:.3f}'.format(u, i, cos(pu, x[i]))
u = 0
i = 11
_my_03_02 = 'cos(p{}, x{}) = {:.3f}'.format(u, i, cos(pu, x[i]))

my_03 = _my_03_01 + "\n" + _my_03_02

def score(u:int, i:int) -> float:
    """
    スコア関数：ユーザuのアイテムiに対するスコアを返す。

    Parameters
    ----------
    u : int
        ユーザuのID（ダミー）
    i : int
        アイテムiのID

    Returns
    -------
    float
        スコア
    """
    return cos(pu, x[i])

def order(u:int, I:np.ndarray) -> List:
    """
    順序付け関数：アイテム集合Iにおいて、ユーザu向けの推薦リストを返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    I : ndarray
        アイテム集合

    Returns
    -------
    list
        タプル(アイテムID: スコア)を要素にした推薦リスト
    """
    scores = {i:score(u,i) for i in I}
    #print('scores = ')
    #pprint.pprint(scores)
    rec_list = sorted( 
                    scores.items(),
                    key = lambda x:x[1],
                    reverse = True
                    )[:TOP_K]
    return rec_list

my_07 = ""

u = 0
rec_list = order(u, Iu_not)
my_07 += 'rec_list = '
for i, scr in rec_list:
    my_07 += '{}: {:.3f}'.format(i, scr)

if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
            if count == 4:
                count = 7
    except KeyError:
        pass
