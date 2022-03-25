import numpy as np

if False:
    ans_du = """
    [[ 5.  3.  1.]
    [ 6.  2.  1.]
    [ 4.  1.  1.]
    [ 8.  5. -1.]
    [ 2.  4. -1.]
    [ 3.  6. -1.]
    [ 7.  6. -1.]
    [ 4.  2. nan]
    [ 5.  1. nan]
    [ 8.  6. nan]
    [ 3.  4. nan]
    [ 4.  7. nan]
    [ 4.  4. nan]]
    """
    print(ans_du.replace(". ",". ,").replace("\n",",\n").replace("nan","np.nan"))

Du = np.array(
    [
        [ 5. , 3. , 1.],
        [ 6. , 2. , 1.],
        [ 4. , 1. , 1.],
        [ 8. , 5. ,-1.],
        [ 2. , 4. ,-1.],
        [ 3. , 6. ,-1.],
        [ 7. , 6. ,-1.],
        [ 4. , 2. ,np.nan],
        [ 5. , 1. ,np.nan],
        [ 8. , 6. ,np.nan],
        [ 3. , 4. ,np.nan],
        [ 4. , 7. ,np.nan],
        [ 4. , 4. ,np.nan]
    ]
)

my01 = 'Du = \n{}'.format(Du)

Du_shape = Du.shape

my02 = 'Duの形状 = {}'.format(Du_shape)

du_culumns = Du.shape[0]

my03 = 'Duの行数 = {}'.format(du_culumns)

my04 = 'Duの行数 = {}'.format(Du.shape[1])

my05 = 'Duの全要素数 = {}'.format(Du.size)

I = np.arange(0,13)

my06 = 'I = {}'.format(I)

x = Du[:,0:2]

my07 = 'x = \n{}'.format(x)

i = 0

my08 = 'x{} = {}'.format(i,x[i])

ru = Du[:,2]

my09 = 'ru = {}'.format(ru)

my10 = 'ruの形状 = {}'.format(ru.shape)

my11 = 'ruの全要素数 = {}'.format(ru.size)

i = 2
j = 5

my12 = 'ru{}からru{}までの評価値 = {}'.format(i, j-1, ru[i:j])

my13 = 'ruの逆順 = {}'.format(ru[::-1])

i = 0

my14 = 'ru{} = {}'.format(i, ru[i])

my15 = 'ユーザuが未評価 = {}'.format(np.isnan(ru))

my16 = 'ユーザuが評価済み = {}'.format(~np.isnan(ru))

Iu = I[~np.isnan(ru)]

my17 = 'Iu = {}'.format(Iu)

Iup = I[ru==1]

my18 = 'Iu+ = {}'.format(Iup)

Iun = I[ru==-1]

my19 = 'Iu- = {}'.format(Iun)

Iu_not = I[np.isnan(ru)]

my20 = 'Iu_not = {}'.format(Iu_not)

DuL = Du[~np.isnan(ru)]

my21 = 'DuL = \n{}'.format(DuL)

my22 = '|DuL| = {}'.format(len(DuL))

my23 = '|DuL+| = {}'.format(len(DuL[DuL[:,2]>0]))

my24 = '|DuL-| = {}'.format(len(DuL[DuL[:,2]<0]))

DuU = Du[np.isnan(ru)]

my25 = 'DuU = \n{}'.format(DuU)

my26 = '|DuU| = {}'.format(len(DuU))

if __name__ == "__main__":

    conv_str = lambda x: "0"+str(x) if x < 10 else str(x)
    
    try:
        count=1
        while(True):
            print(conv_str(count)+",",globals()[f"my{conv_str(count)}"])
            count+=1
    except KeyError:
        pass
