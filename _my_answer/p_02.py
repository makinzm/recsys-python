import numpy as np
np.set_printoptions(precision=3)

if False:
    strR = """R = 
[[nan  4.  3.  1.  2. nan]
 [ 5.  5.  4. nan  3.  3.]
 [ 4. nan  5.  3.  2. nan]
 [nan  3. nan  2.  1.  1.]
 [ 2.  1.  2.  4. nan  3.]]"""
    
    print(strR.replace(". ",". ,").replace("\n",",\n").replace("nan  ","np.nan ,").replace("nan]","np.nan ]"))

R = np.array(
    [
        [np.nan ,4. , 3. , 1. , 2. ,np.nan ],
        [ 5. , 5. , 4. ,np.nan ,3. , 3.],
        [ 4. ,np.nan ,5. , 3. , 2. ,np.nan ],
        [np.nan ,3. ,np.nan ,2. , 1. , 1.],
        [ 2. , 1. , 2. , 4. ,np.nan ,3.]
    ]
)

my_01 = 'R = \n{}'.format(R)

U = np.arange(R.shape[0])

my_02 = 'U = {}'.format(U)

I = np.arange(R.shape[1])

my_03 = 'I = {}'.format(I)

my_04 = '|U| = {}'.format(np.size(U))

my_05 = '|I| = {}'.format(np.size(I))

u = 0
i = 1
my_06 = 'r{}{} = {}'.format(u, i, R[u][i])

my_07 = 'Rの全要素数 = {}'.format(R.size)

my_08 = '観測値 = \n{}'.format(~np.isnan(R))

my_09 = '|R| = {}'.format(np.sum(~np.isnan(R)))

sparsity = 1 - np.sum(~np.isnan(R))/(R.shape[0]*R.shape[1])

my_10 = 'sparsity = {:.3f}'.format(sparsity)

u = 1
my_11 = 'I{} = {}'.format(u, I[~np.isnan(R[u])])

Iu = [I[~np.isnan(R[u])] for u in U]
str_Iu = "".join(
        list(
            map(
                lambda x: "array(["+", ".join(list(map(str,x)))+")]\n",
                Iu
                )
            )
        )
my_12 = f'Iu = \n{str_Iu[:-1]}'

u = 0
v = 1
Iuv = np.intersect1d(Iu[u], Iu[v])

my_13 = 'I{}{} = {}'.format(u, v, Iuv)

i = 0

my_14 = 'U{} = {}'.format(i, U[~np.isnan(R[:,i])])

Ui = [U[~np.isnan(R[:,i])] for i in I]

str_Ui = "".join(
        list(
            map(
                lambda x: "array(["+", ".join(list(map(str,x)))+")]\n",
                Ui
                )
            )
        )
my_15 = f'Iu = \n{str_Ui[:-1]}'

i = 0
j = 4
Uij = np.intersect1d(Ui[i],Ui[j])
my_16 = 'U{}{} = {}'.format(i, j, Uij)

my_17 = 'R全体の平均評価値 = {:.3f}'.format(np.nanmean(R,axis=None))

ri_mean = np.nanmean(R,axis=0) # 0のためユーザーによる平均を取る
my_18 = 'ri_mean = {}'.format(ri_mean)

ru_mean = np.nanmean(R,axis=1)
my_19 = 'ru_mean = {}'.format(ru_mean)

my_20 = 'ru_mean = \n{}'.format(ru_mean.reshape(-1,1))

R2 = R - ru_mean.reshape(-1,1)
# confirm R.shape and ru_mean.shape

my_21 = 'R\' = \n{}'.format(R2)

if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
    except KeyError:
        pass
