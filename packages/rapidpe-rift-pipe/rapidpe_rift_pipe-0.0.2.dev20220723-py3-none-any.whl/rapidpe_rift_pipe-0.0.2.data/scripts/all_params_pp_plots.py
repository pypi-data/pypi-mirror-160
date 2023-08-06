import numpy as np
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats

filename1='data_intrinsic_f2y2016_attempt24_test1.txt'
quantiles1, yaxis_values_m1, yaxis_values_m2, yaxis_values_mchirp, yaxis_values_eta= np.loadtxt(filename1, skiprows=1, unpack=True)
filename2='data_extrinsic_f2y2016_HLV_attempt24_v10_test1.txt'
quantiles2,yaxis_values_distance,yaxis_values_latitude,yaxis_values_longitude,yaxis_values_inclination,yaxis_values_phase,yaxis_values_polarization= np.loadtxt(filename2, skiprows=1, unpack=True)

#this part is copied from https://git.ligo.org/lscsoft/bilby/blob/master/bilby/core/result.py
confidence_interval=[0.68, 0.95, 0.997]
confidence_interval_alpha=0.1
x_values = np.linspace(0, 1, 1001)
N=len(quantiles1)
if isinstance(confidence_interval, float):
    confidence_interval = [confidence_interval]
if isinstance(confidence_interval_alpha, float):
    confidence_interval_alpha = [confidence_interval_alpha] * len(confidence_interval)
for ci, alpha in zip(confidence_interval,confidence_interval_alpha):
    edge_of_bound = (1. - ci) / 2.
    lower = scipy.stats.binom.ppf(1 - edge_of_bound, N, x_values) / N
    upper = scipy.stats.binom.ppf(edge_of_bound, N, x_values) / N
    lower[0] = 0
    upper[0] = 0
    plt.fill_between(x_values, lower, upper, alpha=alpha, color='k')

plt.plot(quantiles2,yaxis_values_longitude,color="red",label="longitude")
plt.plot(quantiles2,yaxis_values_latitude,color="orange",label="latitude")
plt.plot(quantiles2,yaxis_values_phase,color="yellow",label="phase")
plt.plot(quantiles2,yaxis_values_inclination,color="green",label="inclination")
plt.plot(quantiles2,yaxis_values_polarization,color="blue",label="polarization")
plt.plot(quantiles2,yaxis_values_distance,color="purple",label="distance")
plt.plot(quantiles1,yaxis_values_mchirp,color="pink",label="chirp mass")
plt.plot(quantiles1,yaxis_values_eta,color="cyan",label="eta")
plt.plot(quantiles1,yaxis_values_m1,color="gray",label="mass 1")
plt.plot(quantiles1,yaxis_values_m2,color="brown",label="mass 2")



#plt.plot(quantiles1,yaxis_values_m1,color="gray",label="mass 1")
#plt.plot(quantiles1,yaxis_values_m2,color="orange",label="mass 2")
#plt.plot(quantiles1,yaxis_values_mchirp,color="pink",label="chirp mass")
#plt.plot(quantiles1,yaxis_values_eta,color="green",label="eta")
#plt.plot(quantiles2,yaxis_values_distance,color="brown",label="distance")
#plt.plot(quantiles2,yaxis_values_latitude,color="purple",label="latitude")
#plt.plot(quantiles2,yaxis_values_longitude,color="red",label="longitude")
#plt.plot(quantiles2,yaxis_values_inclination,color="cyan",label="inclination")
#plt.plot(quantiles2,yaxis_values_phase,color="yellow",label="phase")
#plt.plot(quantiles2,yaxis_values_polarization,color="blue",label="polarization")
plt.plot(quantiles1,quantiles1,"-k",linestyle='dashed')
#plt.rcParams["font.family"] = "Times New Roman"
mpl.rc('font',family='Times New Roman')
font = mpl.font_manager.FontProperties(family='Times New Roman',size=12)
plt.legend(loc="upper left",prop=font)
plt.xlabel("Quantiles")
plt.ylabel("CDF")
#plt.axes().set_aspect('equal')
plt.grid()
plt.savefig('pp_plot_intrinsic_and_extrinsic_f2y2016_attempt24_test1.png',dpi=300)

