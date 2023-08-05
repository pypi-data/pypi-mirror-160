#Authors: Caitlin Rose and Vinaya Valsan 
import os
import numpy as np
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import ast
import re
import glob
from scipy.stats import norm
import scipy.stats
from glue.ligolw import utils, table, lsctables, ligolw
lsctables.use_in(ligolw.LIGOLWContentHandler)
#from lal import PI, MTSUN_SI
from necessary_function import *

### S190828l
m1_lal = 24.1*1.3
m2_lal = 10.2*1.3
m1_gst = 30.383705
m2_gst = 12.924967

mchirp_lal, eta_lal = mchirp_from_mass1_mass2(m1_lal,m2_lal), eta_from_mass1_mass2(m1_lal,m2_lal)
mchirp_gst, eta_gst = mchirp_from_mass1_mass2(m1_gst,m2_gst), eta_from_mass1_mass2(m1_gst,m2_gst)

run_dir = "/home/caitlin.rose/my_rapidPE_work/quickstart/O3runs/output/O3_lowlatency_S190828l_test6/20210826_gstlal_20190828_G348519/"

results_dir=run_dir+"/results/"

number_of_iter = 2
mass1=np.array([])
mass2=np.array([])
margll=np.array([])
sigma_mchirp=np.array([])
sigma_eta=np.array([])
for iter_no in range(number_of_iter):
	
	# Grid level = 0
	Mass1_0=[]
	Mass2_0=[]
	Margll_0=[]
	xml_files=glob.glob(results_dir+"ILE_iteration_"+str(iter_no)+"-MASS_SET_*0.xml.gz")
	for xml_file in xml_files:
	    xmldoc = utils.load_filename(xml_file, contenthandler=ligolw.LIGOLWContentHandler)
	    new_tbl = lsctables.SnglInspiralTable.get_table(xmldoc)
	    for row in new_tbl:
	        Mass1_0.append(row.mass1)
	        Mass2_0.append(row.mass2)
	        Margll_0.append(row.snr)
	Mass1_0=np.asarray(Mass1_0)
	Mass2_0=np.asarray(Mass2_0)
	Mchirp_0 = mchirp_from_mass1_mass2(Mass1_0, Mass2_0)
	Eta_0 = eta_from_mass1_mass2(Mass1_0, Mass2_0)
	sorted_mchirp=sorted(np.unique(Mchirp_0))
	diff_array_mchirp=np.diff(sorted_mchirp)
	selected_diff_mchirp=[diff for diff in diff_array_mchirp if diff > 1e-5]
	sigma_mchirp_0=min(selected_diff_mchirp)*np.ones(len(Mchirp_0))
	sorted_eta=sorted(np.unique(Eta_0))
	diff_array_eta=np.diff(sorted_eta)
	selected_diff_eta=[diff for diff in diff_array_eta if diff > 1e-5]
	sigma_eta_0=min(selected_diff_eta)*np.ones(len(Eta_0))
	print('sig',min(selected_diff_mchirp),min(selected_diff_eta))
	sigma_mchirp = np.concatenate([sigma_mchirp,sigma_mchirp_0])
	sigma_eta = np.concatenate([sigma_eta,sigma_eta_0])
	mass1 = np.concatenate([mass1,Mass1_0])
	mass2 = np.concatenate([mass2,Mass2_0])
	margll = np.concatenate([margll,Margll_0])



sigma_mchirp = np.array(sigma_mchirp)
sigma_eta = np.array(sigma_eta)
mass1=np.array(mass1)
mass2=np.array(mass2)
mchirp=mchirp_from_mass1_mass2(mass1,mass2)
eta=eta_from_mass1_mass2(mass1,mass2)
margll=np.asarray(margll)
margL = np.exp(margll)
margL=margL/(np.amax(margL))
max_margL_ind = np.argmax(margL)
max_mchirp, max_eta, max_mass1, max_mass2 = mchirp[max_margL_ind], eta[max_margL_ind], mass1[max_margL_ind], mass2[max_margL_ind]

mchirp_samples=np.asarray([])
eta_samples=np.asarray([])
N=500000
for i in range(len(mchirp)):
    random_mchirp=[]
    random_eta=[]
    random_mchirp=np.random.normal(loc=mchirp[i],scale=sigma_mchirp[i],size=int(N*margL[i]))
    random_eta=np.random.normal(loc=eta[i],scale=sigma_eta[i],size=int(N*margL[i]))
    mchirp_samples = np.append(mchirp_samples,random_mchirp)
    eta_samples =np.append(eta_samples,random_eta)
m1_samples, m2_samples = mass1_from_mchirp_eta(mchirp_samples,eta_samples), mass2_from_mchirp_eta(mchirp_samples,eta_samples)
indice = np.where((~np.isnan(m1_samples)) & (~np.isnan(m2_samples)))
m1_samples = m1_samples[indice[0]]
m2_samples = m2_samples[indice[0]]
mchirp_samples = mchirp_samples[indice[0]]
eta_samples = eta_samples[indice[0]]
#m1_m2_prior = np.ones(len(m1_samples))/len(m1_samples)
#mchirp_eta_prior = prior_mchirp_eta(mchirp_samples,eta_samples)
#for i in range(len(m1_samples)):
#        if m1_samples[i]>1.6 or m1_samples[i]<1.2  or m2_samples[i]>1.6 or m2_samples[i]<1.2:
#                m1_m2_prior[i] = 0.
#                mchirp_eta_prior[i] = 0.
M1=np.asarray(m1_samples)
M2=np.asarray(m2_samples)
Mchirp=np.asarray(mchirp_samples)
Eta=np.asarray(eta_samples)
#mchirp_plot=np.unique(np.round(np.sort(mchirp),4))
#eta_plot=np.unique(np.round(np.sort(eta),3))
#mass1_plot=np.unique(np.round(np.sort(mass1),2))
#mass2_plot=np.unique(np.round(np.sort(mass2),2))




fig, axs = plt.subplots(2, 2,figsize=(15, 10))
axs[0,0].hist(M1,bins=100,histtype='step',color = 'b',density=True)#,label = 'posterio samples')
axs[0,0].axvline(x=m1_lal,color="red",label="lal")
axs[0,0].axvline(x=m1_gst,color="green",label="gstlal")
axs[0,0].legend(loc="upper right",prop={'size': 9})
#axs[0,0].set_xlim(1.2,1.6)
#axs[0,0].tick_params(axis='both', which='minor', labelsize=12)
axs[0,0].set_xlabel(r'$M_1(M_{\odot})$',fontsize=14)
axs[0,0].set_ylabel('Posterior Probability',fontsize=14)
axs[0,0].xaxis.set_tick_params(labelsize=12)
#axs[0,0].yaxis.set_visible(False)
axs[0,0].yaxis.set_ticks([])

axs[0,1].hist(M2,bins=100,histtype='step',color = 'b',density=True)#,label = 'posterio samples')
axs[0,1].axvline(x=m2_lal,color="red",label="lal")
axs[0,1].axvline(x=m2_gst,color="green",label="gstlal")
axs[0,1].legend(loc="upper left",prop={'size': 9})
axs[0,1].set_xlabel(r'$M_2(M_{\odot})$',fontsize=14)
axs[0,1].set_ylabel('Posterior Probability',fontsize=14)
axs[0,1].xaxis.set_tick_params(labelsize=12)
#axs[0,1].yaxis.set_visible(False)
axs[0,1].yaxis.set_ticks([])
#axs[0,1].set_xlim(1.2,1.6)

axs[1,0].hist(Mchirp,bins=100,histtype='step',color = 'b',density=True)#,label = 'posterio samples')
axs[1,0].axvline(x=mchirp_lal,color="red",label="lal")
axs[1,0].axvline(x=mchirp_gst,color="green",label="gstlal")
axs[1,0].legend(loc="upper left",prop={'size': 9})
axs[1,0].set_xlabel(r'$\mathcal{M}_c(M_{\odot})$',fontsize=14)
axs[1,0].set_ylabel('Posterior Probability',fontsize=14)
axs[1,0].xaxis.set_tick_params(labelsize=12)
#axs[1,0].yaxis.set_visible(False)
axs[1,0].yaxis.set_ticks([])
#axs[1,0].xaxis.set_major_formatter(FormatStrFormatter('%1.4f'))

axs[1,1].hist(Eta,bins=100,histtype='step',color = 'b',density=True)#,label = 'posterio samples')
axs[1,1].axvline(x=eta_lal,color="red",label="lal")
axs[1,1].axvline(x=eta_gst,color="green",label="gstlal")
axs[1,1].legend(loc="upper left",prop={'size': 9})
axs[1,1].set_xlabel(r'$\eta(M_{\odot})$',fontsize=14)
axs[1,1].set_ylabel('Posterior Probability',fontsize=14)
axs[1,1].xaxis.set_tick_params(labelsize=12)
#axs[1,1].yaxis.set_visible(False)
axs[1,1].yaxis.set_ticks([])
os.system('mkdir -p '+run_dir+'/posterior_plots/')
plt.savefig(run_dir+'/posterior_plots/intrinsic_posterior_plots_m1_m2_mc_eta_gridrefine'+'_iter_'+str(number_of_iter)+'.png')
