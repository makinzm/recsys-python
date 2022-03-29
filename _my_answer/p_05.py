import pprint
import numpy as np
np.set_printoptions(precision=3)

# 近傍ユーザ数
K_USERS = 3
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

def pearson1(u, v):
    """
    評価値行列Rにおけるユーザuとユーザvのピアソンの相関係数を返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    v : int
        ユーザvのID

    Returns
    -------
    float
        ピアソンの相関係数
    """
    Iuv = np.intersect1d(Iu[u], Iu[v])
    global my_01, my_02, my_03
    num = np.sum([R2[u][i]*R2[v][i] for i in Iuv])
    my_01 = 'num = {}'.format(num)
    den_u = np.sqrt(np.sum([R2[u][i]**2 for i in Iuv]))
    my_02 = 'den_u = {:.3f}'.format(den_u)
    den_v = np.sqrt(np.sum([R2[v][i]**2 for i in Iuv]))
    my_03 = 'den_v = {:.3f}'.format(den_v)
    
    prsn = num / (den_u * den_v)
    return prsn

u = 0
v = 1
prsn = pearson1(u, v)
my_03 +="\n" + 'pearson1({}, {}) = {:.3f}'.format(u, v, prsn)

def pearson2(u, v):
    """
    平均中心化評価値行列R2におけるユーザuとユーザvのピアソンの相関係数を返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    v : int
        ユーザvのID

    Returns
    -------
    float
        ピアソンの相関係数
    """
    global my_04, my_05, my_06
    Iuv = np.intersect1d(Iu[u], Iu[v])
    
    num = np.sum([R2[u][i]*R2[v][i] for i in Iuv])
    my_04 = 'num = {}'.format(num)
    den_u = np.sqrt(np.sum([R2[u][i]**2 for i in Iuv]))
    my_05 = 'den_u = {:.3f}'.format(den_u)
    den_v = np.sqrt(np.sum([R2[v][i]**2 for i in Iuv]))
    my_06 = 'den_v = {:.3f}'.format(den_v)

    prsn = num / (den_u * den_v)
    return prsn

u = 0
v = 1
prsn = pearson2(u, v)
my_06 +="\n" + 'pearson1({}, {}) = {:.3f}'.format(u, v, prsn)

def sim(u, v):
    """
    ユーザ類似度関数：ユーザuとユーザvのユーザ類似度を返す。

    Parameters
    ----------
    u : int
        ユーザuのID
    v : int
        ユーザvのID

    Returns
    -------
    float
        ユーザ類似度
    """
    return pearson2(u, v)

S = np.array([[sim(u,v) for v in U] for u in U])

my_07 = "S ="
for i in range(len(S)):
    my_07 += "\n"+'{}'.format(list(map(lambda x: "{:.3f}".format(x),S[i])))

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

Uu = {u: {v: S[u,v] for v in U if u!=v} for u in U}

my_08 = "Uu=" + print_dict(Uu)

Uu = {u:
        dict(
            sorted(v.items(),
            key = lambda x: x[1], 
            reverse=True)[:K_USERS]
            ) for u,v in Uu.items()
        }

my_08 += "\nUu=" + print_dict(Uu)

Uu = {u:
        dict(
            [
                [uu,uv] for uu,uv in v.items()
                if uv > THETA
            ]
        ) for u,v in Uu.items()
    }

my_09 = "Uu=" + print_dict(Uu)

Uu = {u: np.array(list(Uu[u].keys())) for u in U}

my_09 += "\nUu=" + str(Uu)

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
    global my_10
    Uui = np.intersect1d(Ui[i], Uu[u])
    my_10 += '\nU{}{} = {}'.format(u, i, Uui)

    if Uui.size <= 0: return ru_mean[u]
    else: rui_pred = ru_mean[u] + \
         S[u,Uui] @ R2[Uui,i] \
             /np.sum(np.abs(S[u,Uui]))
    
    return rui_pred

my_10 = ""

u = 0
i = 0
my_11 = '\nr{}{} = {:.3f}'.format(u, i, predict(u, i))
u = 0
i = 5
my_11 += '\nr{}{} = {:.3f}'.format(u, i, predict(u, i))

R3 = np.array(
    [
        [
            R[u,i] if (not np.isnan(R[u,i])) else predict(u,i) for i in I 
        ]
        for u in U
    ]
)

my_12 = 'R\'\' = \n{}'.format(R3)

if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
    except KeyError:
        pass
