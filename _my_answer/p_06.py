import pprint
import numpy as np
np.set_printoptions(precision=3)

# 近傍アイテム数
K_ITEMS = 3
# 閾値
THETA = 0

R = np.array([
              [np.nan, 4,      3,      1,      2,      np.nan],
              [5,      5,      4,      np.nan, 3,      3     ],
              [4,      np.nan, 5,      3,      2,      np.nan],
              [np.nan, 3,      np.nan, 2,      1,      1     ],
              [2,      1,      2,      4,      np.nan, 3     ],
])
# 行方向にユーザーがいて, 列方向にアイテムがある
# ex: 
#     - R[0, :] : 0のユーザーの好み
#     - R[:, 0] : 0のアイテムの評価
U = np.arange(R.shape[0])
I = np.arange(R.shape[1])
Ui = [U[~np.isnan(R)[:,i]] for i in I]
Iu = [I[~np.isnan(R)[u,:]] for u in U]
ru_mean = np.nanmean(R, axis=1)
R2 = R - ru_mean.reshape((ru_mean.size, 1))

def cos(i, j):
    """
    評価値行列Rにおけるアイテムiとアイテムjのコサイン類似度を返す。

    Parameters
    ----------
    i : int
        アイテムiのID
    j : int
        アイテムjのID

    Returns
    -------
    float
        コサイン類似度
    """
    Uij = np.intersect1d(Ui[i], Ui[j])
    cosine = R[Uij,i]@R[Uij,j]/ \
        (np.linalg.norm(R[Uij,i], 2)*np.linalg.norm(R[Uij,j], 2))
    return cosine

i = 0
j = 4
cosine = cos(i, j)
my_01 = 'cos({}, {}) = {:.3f}'.format(i, j, cosine)

def adjusted_cos(i, j):
    """
    評価値行列R2におけるアイテムiとアイテムjの調整コサイン類似度を返す。

    Parameters
    ----------
    i : int
        アイテムiのID
    j : int
        アイテムjのID

    Returns
    -------
    cosine : float
        調整コサイン類似度
    """
    Uij = np.intersect1d(Ui[i], Ui[j])
    
    cosine = R2[Uij,i]@R2[Uij,j]/ \
        (np.linalg.norm(R2[Uij,i], 2)*np.linalg.norm(R2[Uij,j], 2))
    return cosine

i = 0
j = 4
cosine = adjusted_cos(i, j)
my_02 = 'cos({}, {}) = {:.3f}'.format(i, j, cosine)

def sim(i, j):
    """
    アイテム類似度関数：アイテムiとアイテムjのアイテム類似度を返す。

    Parameters
    ----------
    i : int
        アイテムiのID
    j : int
        アイテムjのID

    Returns
    -------
    float
        アイテム類似度
    """
    return adjusted_cos(i, j)

S = np.array([[sim(i,j) for j in I] for i in I])
my_03 = 'S = \n{}'.format(S)


def print_dict(dic:dict,k=1,br=False)-> str:
    spaces = " "*(k-1)
    if br:
        res = spaces+"{\n"
    else:
        res = "\n"+spaces+"{\n"
    for i,v in dic.items():
        if type(v)!=dict:
            res += f"{spaces}{i}:{v:.4f}\n"
        else:
            res += f"{spaces}{i}:{print_dict(v,k=2*k,br=True)}"
    if br:
        res += spaces+"}\n"
    else:
        res += spaces+"}"
    return res


Ii = {i: {j: S[i,j] for j in I if i != j} for i in I}
my_04 = 'Ii = \n'+print_dict(Ii)
Ii = {i:
        dict(
            sorted(v.items(),
            key = lambda x: x[1], 
            reverse=True)[:K_ITEMS]
            ) for i,v in Ii.items()
        }
my_05 = 'Ii = \n'+print_dict(Ii)

Ii = {i:
        dict(
            [
                [ii,iv] for ii,iv in v.items()
                if iv > THETA
            ]
        ) for i,v in Ii.items()
    }

my_05 += '\nIi = \n'+print_dict(Ii)
# 各アイテムの類似アイテム集合をまとめた辞書
Ii = {i: np.array(list(Ii[i].keys())) for i in I}
my_05 += '\nIi = \n'+str(Ii)

my_06 = ""
def predict(u, i):
    """
    予測関数：ユーザuのアイテムiに対する予測評価値を返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    i : int
        アイテムiのID
    
    Returns
    -------
    float
        ユーザuのアイテムiに対する予測評価値
    """
    global my_06
    Iiu = np.intersect1d(Iu[u], Ii[i])
    my_06 += '\nI{}{} = {}'.format(i, u, Iiu)

    if Iiu.size <= 0: return ru_mean[u]
    else:
        rui_pred = ru_mean[u] + \
            S[i,Iiu] @ R2[u,Iiu] \
                /np.sum(np.abs(S[i,Iiu]))
    
    return rui_pred

u = 0
i = 0
my_07 = 'r{}{} = {:.3f}'.format(u, i, predict(u, i))
u = 0
i = 5
my_07 += '\nr{}{} = {:.3f}'.format(u, i, predict(u, i))


if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
    except KeyError:
        pass
