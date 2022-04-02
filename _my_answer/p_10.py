import pprint
import numpy as np

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

def G(DL):
    """
    訓練データDLのジニ係数を返す。
    
    Parameters
    ----------
    DL : ndarray
        訓練データDL

    Returns
    -------
    float
        ジニ係数
        ただし、DLに事例が含まれていないときは0
    """
    if DL.shape[0] == 0: return 0
    r = DL[:,-1]
    pp = np.sum(r == 1)/r.shape[0]
    pn = np.sum(r == -1)/r.shape[0]
    gini = 1 - (pp**2 + pn**2)
    return gini

print('G(DuL) = {:.3f}'.format(G(DuL)))

def G_partitioned(DL0, DL1):
    """
    訓練データをDL0とDL1に分割したときのジニ係数を返す。
    
    Parameters
    ----------
    DL0 : ndarray
        訓練データDL0
    DL1 : ndarray
        訓練データDL1

    Returns
    -------
    float
        ジニ係数
    """
    gini = (DL0.shape[0]*G(DL0)+DL1.shape[0]*G(DL1)) \
            / (DL0.shape[0] + DL1.shape[0])
    return gini

# 特徴量kを含まない訓練事例集合
k = 0
DuL0 = DuL[DuL[:,k]==0]
print('DuL0 = \n{}'.format(DuL0))
# 特徴量kを含む訓練事例集合
DuL1 = DuL[DuL[:,k]==1]
# 特徴量kを基準に分割したときのジニ係数
print('DuL1 = \n{}'.format(DuL1))
print('G(DuL → [DuL0, DuL1]) = {:.3f}'.format(G_partitioned(DuL0, DuL1)))

def get_ginis(DL):
    """
    訓練データDLを各特徴量で分割したときの(特徴量のインデックス: ジニ係数)をペアにした辞書を返す。
    
    Parameters
    ----------
    DL : ndarray
        訓練データDL

    Returns
    -------
    dict
        (特徴量のインデックス: ジニ係数)をペアにした辞書
    """
    ginis = {}
    for k in range(0, x.shape[1]):
        DL0 = DL[DL[:,k]==0]
        DL1 = DL[DL[:,k]==1]
        ginis[k] = G_partitioned(DL0, DL1)
    return ginis

# レベル0（根ノード）の選択基準
ginis = get_ginis(DuL)
print('ginis = ')
pprint.pprint(ginis)
k0 = min(ginis.items(), key = lambda x: x[1])[0]
print('k0 = {}'.format(k0))
DuL0 = DuL[DuL[:,k0]==0]
DuL1 = DuL[DuL[:,k0]==1]
print('DuL0 = \n{}'.format(DuL0))
print('DuL1 = \n{}'.format(DuL1))

# レベル1a（レベル1の左端ノード）の選択基準
k1a = min(get_ginis(DuL0).items(), key = lambda x: x[1])[0]
print('k1a = {}'.format(k1a))
DuL00 = DuL0[DuL0[:,k1a] == 0]
DuL01 = DuL0[DuL0[:,k1a] == 1]
print('DuL00 = \n{}'.format(DuL00))
print('DuL01 = \n{}'.format(DuL01))

# レベル2a（レベル2の左端ノード）の選択基準
k2a = min(get_ginis(DuL00).items(), key = lambda x: x[1])[0]
print('k2a = {}'.format(k2a))
DuL000 = DuL00[DuL00[:,k2a] == 0]
DuL001 = DuL00[DuL00[:,k2a] == 1]
print('DuL000 = \n{}'.format(DuL000))
print('DuL001 = \n{}'.format(DuL001))


def train(DL, key=0):
    """
    学習関数：訓練データDLから決定木を学習する。
    
    Parameters
    ----------
    DL : ndarray
        訓練データDL
    key : int
        キー値
    """
    if len(DL) <= 0:
        return
    elif np.count_nonzero(DL[:,-1]==-1) <= 0:
        dtree[key] = '+1'
        return
    elif np.count_nonzero(DL[:,-1]==+1) <= 0:
        dtree[key] = '-1'
        return
        
    ginis = get_ginis(DL)
    k = min(ginis, key=ginis.get)
    dtree[key] = k
    DL0 = DL[DL[:,k] == 0]
    DL1 = DL[DL[:,k] == 1]
    train(DL0, key * 2 + 1) # 0は左
    train(DL1, key * 2 + 2) # 1は右


def predict(u, i, key=0):
    """
    予測関数：ユーザuのアイテムiに対する予測評価値を返す。
    
    Parameters
    ----------
    u : int
        ユーザuのID（ダミー）
    i : int
        アイテムiのID
    key : int
        キー値

    Returns
    -------
    int
        ユーザuのアイテムiに対する予測評価値
    """
    if type(dtree[key]) == str: return int(dtree[key])
    k = dtree[key]
    if x[i,k] == 0:
        return predict(u, i, key * 2 + 1)
    elif x[i,k] == 1:
        return predict(u, i, key * 2 + 2)
    
dtree = {} 
# key : (node number) , value : (dimension or predict)
train(DuL)
print('dtree = {}'.format(dtree))

u = 0
print(xU)
ruU_pred = {i:predict(u,i) for i in I[np.isnan(ru)]}
print('ruU_pred = {}'.format(ruU_pred))
