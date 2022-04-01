
import numpy as np
import numpy.linalg as LA
np.set_printoptions(precision=3)

# 縮約後の次元数
DIM = 2

Du = np.array([
               [5, 3, 3, +1],
               [6, 2, 5, +1],
               [4, 1, 5, +1],
               [8, 5, 9, -1],
               [2, 4, 2, -1],
               [3, 6, 5, -1],
               [7, 6, 8, -1],
               [4, 2, 3, np.nan],
               [5, 1, 8, np.nan],
               [8, 6, 6, np.nan],
               [3, 4, 2, np.nan],
               [4, 7, 5, np.nan],
               [4, 4, 4, np.nan],
])
I = np.arange(Du.shape[0])
x = Du[:,:-1]
ru = Du[:,-1]

xk_mean = np.mean(x, axis=0)
my_01 = 'xk_mean = {}'.format(xk_mean)

s2 = np.var(x, axis=0)
my_02 = 's^2 = {}'.format(s2)

x2 = np.divide(x - xk_mean, np.sqrt(s2), where = s2!=0)
my_03 = 'x\' = \n{}'.format(x2)

k = 0
l = 1
skl = np.cov(x2[:,k],x2[:,l],bias=True)[0,1]
my_04 = 's{}{} = {:.3f}'.format(k, l, skl)

S = np.cov(x2.T, bias=True)
my_05 = 'S = \n{}'.format(S)

lmd, v = np.linalg.eig(S)
my_06 = 'λ = {}'.format(lmd)
my_06 += '\nv = \n{}'.format(v)

# 問9を見越すとindicesを求めておいた方が良い

indices = np.argsort(lmd)[::-1] # [3(0), 1(1), 2(2)] -> [1(1), 2(2), 3(0)] のため [1, 2, 0]が出力
my_07 = 'indices = {}'.format(indices)

lmd = lmd[indices]
my_08 = 'λ = {}'.format(lmd)
my_08 += '\nλ = {}'.format(np.sort(lmd)[::-1])

v = v[:,indices]
my_09 = 'v = \n{}'.format(v)

"""

You should referred to this page : 
    https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html

    " v[:,i] is the eigenvector corresponding to the eigenvalue w[i]. "

"""

v = v[:,:DIM]
my_10 = 'v = \n{}'.format(v)

i = 0
k = 0
xik3 = x2[i]@v[:,k]
my_11 = 'x{}{}\'\' = {:.3f}'.format(i, k, xik3)

x3 = x2@v
my_12 = 'x\'\' = \n{}'.format(x3)

# Satisfies positive definiteness due to covariance matrix
k = 0
pk = lmd[k]/np.sum(lmd)
my_13 = '第{}主成分の寄与率 = {:.3f}'.format(k+1, pk)

k = 2
ck = np.sum(lmd[:k]/np.sum(lmd))
my_14 = '第{}主成分までの累積寄与率 = {:.3f}'.format(k, ck)

Du2 = np.hstack((x3, ru.reshape(-1,1)))
my_15 = 'R\' = \n{}'.format(Du2)


if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my_{conv_str(count)}"])
            count+=1
    except KeyError:
        pass
