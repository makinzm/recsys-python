import pprint
import numpy as np
np.set_printoptions(precision=3)

# 上位K件
TOP_K = 3
# 近傍アイテム数
K_ITEMS = 3
# しきい値
THETA = 0

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

def dist(xi, xj):
    """
    距離関数：アイテムiの特徴ベクトルxiとアイテムjの特徴ベクトルxjのユークリッド距離を返す。

    Parameters
    ----------
    xi : ndarray
        アイテムiの特徴ベクトル
    xj : ndarray
        アイテムjの特徴ベクトル

    Returns
    -------
    float
        ユークリッド距離
    """
    distance = np.sqrt(np.sum(list(map(lambda d: d**2,xi-xj))))
    return distance

my_01 = ""
i = 7
j = 2
my_01+='dist(x{}, x{}) = {:.3f}'.format(i, j, dist(x[i], x[j]))
i = 7
j = 3
my_01+="\n"+'dist(x{}, x{}) = {:.3f}'.format(i, j, dist(x[i], x[j]))

D = np.array([[dist(x[i],x[j]) for i in I] for j in I])

my_02 = 'D = \n{}'.format(D[np.ix_(Iu_not,Iu)])

# np.ix_ : https://numpy.org/doc/stable/reference/generated/numpy.ix_.html

Ii = np.argsort(D[:,Iu],axis=1) # 1(評価済みのアイテム)に関しての順位付けをする

my_03 = 'Ii = \n{}'.format(Ii)

Ii = Ii[:,:TOP_K]

my_04 = 'Ii = \n{}'.format(Ii)

Ii = {item:items for item,items in zip(Iu_not, Ii[Iu_not])}

my_05 = 'Ii =\n{}'.format(Ii)

def predict1(u, i):
    """
    予測関数（多数決方式）：多数決方式によりユーザuのアイテムiに対する予測評価値を返す。
    Iiの設定によっては,アイテムiが評価されていないユーザに限定されている可能性がある.

    Parameters
    ----------
    u : int
        ユーザuのID（ダミー）
    i : int
        アイテムiのID

    Returns
    -------
    float
        予測評価値
    """
    Iip = Ii[i][np.isin(Ii[i],Iup)]
    #print('I{}+ = {}'.format(i, Iip))
    Iin = Ii[i][np.isin(Ii[i],Iun)]
    #print('I{}- = {}'.format(i, Iin))

    if np.size(Iip)==np.size(Iin):
        rui = 0
    if np.size(Iip)>np.size(Iin):
        rui = 1
    if np.size(Iip)<np.size(Iin):
        rui = -1

    return rui

u = 0
i = 7
my_06 = 'predict1({}, {}) = {:.3f}'.format(u, i, predict1(u, i))+"\n"
u = 0
i = 9
my_06 += 'predict1({}, {}) = {:.3f}'.format(u, i, predict1(u, i))

def predict2(u, i):
    """
    予測関数（平均方式）：平均方式によりユーザuのアイテムiに対する評価値を予測する。

    Parameters
    ----------
    u : int
        ユーザuのID（ダミー）
    i : int
        アイテムiのID

    Returns
    -------
    Union[float,str]
        予測評価値
    """
    try:
        rui = (np.count_nonzero(np.isin(Ii[i],Iup))-np.count_nonzero(np.isin(Ii[i],Iun))) / \
            (np.count_nonzero(np.isin(Ii[i],Iup))+np.count_nonzero(np.isin(Ii[i],Iun)))
        return rui
    except ZeroDivisionError:
        return "ERROR"

u = 0
i = 7
my_09 = 'predict2({}, {}) = {:.3f}'.format(u, i, predict2(u, i))+"\n"
u = 0
i = 9
my_09 += 'predict2({}, {}) = {:.3f}'.format(u, i, predict2(u, i))

def score(u, i):
    """
    スコア関数：ユーザuのアイテムiに対するスコアを返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    i : int
        アイテムiのID

    Returns
    -------
    float
        スコア
    """
    return predict2(u, i)

def order(u, I):
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
    scores = {i: score(u, i) for i in I}
    scores = {i:s for i,s in scores.items() if s>= THETA}
    rec_list = sorted(scores.items(), key=lambda x:x[1], reverse=True)[:TOP_K]
    return rec_list

u = 0
rec_list = order(u, Iu_not)
my_10 = 'rec_list ='
for i, scr in rec_list:
    my_10 += '\n{}: {:.3f}'.format(i, scr)

if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
            if count == 7:
                count = 9
    except KeyError:
        pass
