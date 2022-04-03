import numpy as np

# テストデータ
R = np.array([
              [np.nan, 4,      np.nan, np.nan, np.nan, np.nan, 2,      np.nan, np.nan, np.nan],
              [np.nan, np.nan, np.nan, np.nan, 2,      np.nan, np.nan, np.nan, 5,      np.nan],
              [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 3,      np.nan, np.nan],
])
U = np.arange(R.shape[0])
I = np.arange(R.shape[1])

# 推薦システムAによる予測評価値
RA = np.array([
               [np.nan, 2,      np.nan, np.nan, np.nan, np.nan, 2,      np.nan, np.nan, np.nan],
               [np.nan, np.nan, np.nan, np.nan, 2,      np.nan, np.nan, np.nan, 3,      np.nan],
               [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 3,      np.nan, np.nan],
])

# 推薦システムBによる予測評価値
RB = np.array([
               [np.nan, 3,      np.nan, np.nan, np.nan, np.nan, 1,      np.nan, np.nan, np.nan],
               [np.nan, np.nan, np.nan, np.nan, 3,      np.nan, np.nan, np.nan, 4,      np.nan],
               [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 4,      np.nan, np.nan],
])

MAE_A = np.nansum(np.abs(RA-R))/np.count_nonzero(~np.isnan(RA))
print('MAE_{} = {:.3f}'.format('A', MAE_A))
MAE_B = np.nansum(np.abs(RB-R))/np.count_nonzero(~np.isnan(RB))
print('MAE_{} = {:.3f}'.format('B', MAE_B))

MSE_A = np.nansum((RA-R)**2)/np.count_nonzero(~np.isnan(RA))
print('MSE_{} = {:.3f}'.format('A', MSE_A))
MSE_B = np.nansum((RB-R)**2)/np.count_nonzero(~np.isnan(RB))
print('MSE_{} = {:.3f}'.format('B', MSE_B))

RMSE_A = np.sqrt(MSE_A)
print('RMSE_{} = {:.3f}'.format('A', RMSE_A))
RMSE_B = np.sqrt(MSE_B)
print('RMSE_{} = {:.3f}'.format('B', RMSE_B))

# NMAE

# I think this value is given with data
R_MAX = np.nanmax(np.concatenate([R,RA,RB]))
R_MIN = np.nanmin(np.concatenate([R,RA,RB]))

NMAE_A = MAE_A/(R_MAX-R_MIN)
print('NMAE_{} = {:.3f}'.format('A', NMAE_A))
NMAE_B = MAE_B/(R_MAX-R_MIN)
print('NMAE_{} = {:.3f}'.format('B', NMAE_B))

# NRMSE
NRMSE_A = RMSE_A/(R_MAX-R_MIN)
print('NRMSE_{} = {:.3f}'.format('A', NRMSE_A))
NRMSE_B = RMSE_B/(R_MAX-R_MIN)
print('NRMSE_{} = {:.3f}'.format('B', NRMSE_B))

