from petbox import dca
from data import rate as data_q, time as data_t
import numpy as np
from scipy.interpolate import make_interp_spline as make_bspline, BSpline
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.style.use('seaborn-white')
plt.rcParams['font.size'] = 16


# Setup time series for Forecasts and calculate cumulative production of data

# We have this function handy
t = dca.get_time(n=1001)

# Calculate cumulative volume array of data
data_N = np.cumsum(data_q * np.r_[data_t[0], np.diff(data_t)])

# Calculate diagnostic functions D, beta, and b
data_D = -dca.bourdet(data_q, data_t, L=0.35, xlog=False, ylog=True)
data_beta = data_D * data_t
data_b = dca.bourdet(1 / data_D, data_t, L=0.25, xlog=False, ylog=False)


bspline_N: BSpline = make_bspline(np.r_[-1, data_t], np.r_[0, data_N], k=1)
bspline_q = bspline_N.derivative()

resample_t_1 = np.arange(0, 2000 + 100, 100, dtype=np.float64)
resample_N_0 = bspline_N(resample_t_1)
bspline_N_1: BSpline = make_bspline(np.r_[-1, resample_t_1], np.r_[0, resample_N_0], k=1)
bspline_q_1 = bspline_N_1.derivative()
resample_q_1 = bspline_q_1(resample_t_1)
resample_N_1 = bspline_N_1(resample_t_1)

resample_t_2 = np.arange(0, 2000 + 1, 1, dtype=np.float64)
resample_q_2 = bspline_q_1(resample_t_2)
resample_N_2 = bspline_N_1(resample_t_2)


# thm = dca.THM(qi=750, Di=.8, bi=2, bf=.5, telf=28)
# q_thm = thm.rate(t)
# N_thm = thm.cum(t)
# D_thm = thm.D(t)
# b_thm = thm.b(t)
# beta_thm = thm.beta(t)
# N_thm *= data_N[-1] / thm.cum(data_t[-1])


# Rate vs Time
fig = plt.figure(figsize=(15, 7.5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(data_t, data_q, 'o', mfc='w', label='Data')
ax1.plot(resample_t_2, resample_q_2, ls='--', label='BSpline Resample (100 Day Avg)')

ax1.set(xscale='linear', yscale='linear')#, ylim=(1e0, 1e4), xlim=(0, 2000))
ax1.set(ylabel='Rate, BPD', xlabel='Time, Days')
# ax1.set_aspect(1)
ax1.grid()
ax1.legend()

# Cumulative Volume vs Time
ax2.plot(data_t, data_N, 'o', mfc='w', label='Data')
ax2.plot(resample_t_2, resample_N_2, ls='--', label='BSpline Resample (100 Day Avg)')

ax2.set(xscale='linear', yscale='linear')#, ylim=(1e2, 1e6), xlim=(0, 2000))
ax2.set(ylabel='Cumulative Volume, MBbl', xlabel='Time, Days')
# ax2.set_aspect(1)
ax2.grid()
ax2.legend()

plt.show()
