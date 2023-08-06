import numpy as np 
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
import ast
import re
import glob
from scipy.stats import norm
import scipy.stats
from glue.ligolw import utils, table, lsctables, ligolw
lsctables.use_in(ligolw.LIGOLWContentHandler)

#This is a script for the mass1 pp-plot with one point for each injection using monte carlo integration with gaussian-mchirp-eta sampling

input_dir =   "/home/vinaya.valsan/rapidPE/inj_data/automated_rapidpe_submission/output/f2y2016_HLV_attempt24/"

inj_dirs = glob.glob(input_dir+"inj_*")
yaxis_values_m1=[]
yaxis_values_m2=[]
yaxis_values_mchirp=[]
yaxis_values_eta=[]

#injections_file='/home/caitlin.rose/my_rapidPE_work/f2y2016data/subset_f2y2016inj/f2y2016_HLV_gstlal_inj_coinc_id.txt'
#Mass1_inj,Mass2_inj,Coinc_id=np.loadtxt(injections_file,skiprows=1,usecols=(0,1,11),unpack=True)
#Coinc_id=Coinc_id.astype(int)

def m1_func(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.+np.sqrt(1.-4.*eta)))
def m2_func(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.-np.sqrt(1.-4.*eta)))

def mchirp_func(m1,m2):
    return(((m1*m2)**(3./5.))*((m1+m2)**(-1./5.)))
def eta_func(m1,m2):
    return((m1*m2)*((m1+m2)**(-2.)))

def prior(mchirp,eta):
    return(np.abs(mchirp*np.power(eta,-6./5.)*(1./np.sqrt(1.-4.*eta)))/(0.4**2.))

for inj_dir in inj_dirs:
    print(inj_dir)
    #read from results folder directly
    Mass1=[]
    Mass2=[]
    Margll=[]
    results_dir=inj_dir+"/results/"
    xml_files=glob.glob(results_dir+"*.xml.gz")
    for xml_file in xml_files:
        if ".samples.xml.gz" in xml_file:
            continue
        try:
            xmldoc = utils.load_filename(xml_file, contenthandler=ligolw.LIGOLWContentHandler)
        except:
            continue
        new_tbl = lsctables.SnglInspiralTable.get_table(xmldoc)
        for row in new_tbl:
            Mass1.append(row.mass1)
            Mass2.append(row.mass2)
            Margll.append(row.snr)
    Mass1=np.asarray(Mass1)
    Mass2=np.asarray(Mass2)
    Mchirp=mchirp_func(Mass1,Mass2)
    Eta=eta_func(Mass1,Mass2)
    Margll=np.asarray(Margll)        

    #read injected masses from injections txt file 
    #coinc_id=int(inj_dir.replace(input_dir+'inj_',''))
    #index=np.where(Coinc_id==coinc_id)
    #mass1_inj=float(Mass1_inj[index])
    #mass2_inj=float(Mass2_inj[index])
    #mchirp_inj = mchirp_func(mass1_inj,mass2_inj)
    #eta_inj = eta_func(mass1_inj,mass2_inj)
    


    #read the injection information for mass1 and mass2 
    event_info = open(inj_dir+"/event_info_dict.txt","r")
    contents = event_info.read()
    dictionary = ast.literal_eval(contents)
    mass_inj = dictionary["intrinsic_param"]
    mass1_inj = re.search('mass1=(.+?)"',mass_inj)
    mass1_inj = mass1_inj.group(1)
    mass1_inj = float(mass1_inj)
    mass2_inj = re.search('mass2=(.+?)"',mass_inj)
    mass2_inj = mass2_inj.group(1)
    mass2_inj = float(mass2_inj)
    mchirp_inj = mchirp_func(mass1_inj,mass2_inj)
    eta_inj = eta_func(mass1_inj,mass2_inj)

    #read the Rapid PE results for the marginalized log likelihood at each grid point 
    #filename=inj_dir+'/margll0.txt'
    #filename=inj_dir+'/margll_levels.txt'
    #try:
    #    Mass1, Mass2, Mchirp, Eta, Margll = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3,8), unpack=True)
    #except:
    #    continue
    #remove grid points outside of the 1.2-1.6 mass range:
    mass1=Mass1
    mass2=Mass2
    mchirp=Mchirp
    eta=Eta
    margll=Margll
    #for i in range(len(Mchirp)):
    #    if 1.2<Mass1[i]<1.6 and 1.2<Mass2[i]<1.6:
    #        mass1.append(Mass1[i])
    #        mass2.append(Mass2[i])
    #        mchirp.append(Mchirp[i])
    #        eta.append(Eta[i])
    #        margll.append(Margll[i])
    #here I'm converting the marginalized log likelihood to the marginalized likelihood 
    margL = np.exp(margll)
    #scaling the marginalized likelihood by the maximum marginalized likelihood (cancels out because of evidence)
    try:
        margL = margL/(np.amax(margL))
    except:
        continue

    #calculate sigma (the distance between two adjacent grid points, in both mchirp and eta)
    sorted_mchirp=sorted(np.unique(Mchirp))
    diff_array_mchirp=np.diff(sorted_mchirp)
    selected_diff_mchirp=[diff for diff in diff_array_mchirp if diff > 1e-6]
    try:
        sigma_mchirp=min(selected_diff_mchirp)
    except:
        continue
    sorted_eta=sorted(np.unique(Eta))
    diff_array_eta=np.diff(sorted_eta)
    selected_diff_eta=[diff for diff in diff_array_eta if diff > 1e-6]
    try:
        sigma_eta=min(selected_diff_eta)
    except:
        continue

    count_evidence=0.
    count_m1=0.
    count_m2=0.
    count_mchirp=0.
    count_eta=0.
    #i is the index of each grid point 
    for i in range(len(mchirp)):
        Random_mchirp=[]
        Random_eta=[]
        random_mchirp=[]
        random_eta=[]
        random_Mchirp=np.random.normal(loc=mchirp[i],scale=sigma_mchirp,size=100000)
        random_Eta=np.random.normal(loc=eta[i],scale=sigma_eta,size=100000)
        #remove samples where eta>0.25 
        for k in range(len(random_Mchirp)):
            if random_Eta[k]<=0.25: 
                Random_eta.append(random_Eta[k])
                Random_mchirp.append(random_Mchirp[k])
        Random_eta=np.asarray(Random_eta)
        Random_mchirp=np.asarray(Random_mchirp)
        Random_m1=m1_func(Random_mchirp,Random_eta)
        Random_m2=m2_func(Random_mchirp,Random_eta)
        #remove samples outside of 1.2<m1<1.6 and 1.2<m2<1.6 range
        for k in range(len(Random_mchirp)):
            #if 1.2<Random_m1[k]<1.6 and 1.2<Random_m2[k]<1.6:
            if Random_m1[k]<=1.6 and Random_m2[k]<=1.6 and Random_m1[k]>=1.2 and Random_m2[k]>=1.2:
                random_mchirp.append(Random_mchirp[k])
                random_eta.append(Random_eta[k])
        random_mchirp=np.asarray(random_mchirp)
        random_eta=np.asarray(random_eta)
        if len(random_mchirp)==0:
            continue
#        random_F=np.random.uniform(0,margL[i],size=len(random_mchirp))
#        Fofrandoms=margL[i]*np.exp(((-1.)*(1./(2.*(sigma_mchirp**2.)))*((random_mchirp-mchirp[i])**2.))+((-1.)*(1./(2.*(sigma_eta**2.)))*((random_eta-eta[i])**2.)))
        Fofrandoms=margL[i]*prior(random_mchirp,random_eta)
        random_F=np.random.uniform(0,np.amax(Fofrandoms),size=len(random_mchirp))
        area_sampled=np.amax(Fofrandoms)
        #j is the index of each random sample 
        for j in range(len(random_mchirp)):
            if random_F[j]<=Fofrandoms[j]:
                count_evidence+=1.*area_sampled
                random_m1 = m1_func(random_mchirp[j],random_eta[j])
                random_m2 = m2_func(random_mchirp[j],random_eta[j])
                if random_m1<=mass1_inj:
                    count_m1+=1.*area_sampled
                if random_m2<=mass2_inj:
                    count_m2+=1.*area_sampled
                if random_mchirp[j]<=mchirp_inj:
                    count_mchirp+=1.*area_sampled
                if random_eta[j]<=eta_inj:
                    count_eta+=1.*area_sampled
    #area sampled, number of samples, etc cancel out when dividing by the evidence 
    try:
        yaxis_m1=count_m1/count_evidence
    except:
        continue
    yaxis_values_m1.append(yaxis_m1)
    yaxis_m2=count_m2/count_evidence
    yaxis_values_m2.append(yaxis_m2)
    yaxis_mchirp=count_mchirp/count_evidence
    yaxis_values_mchirp.append(yaxis_mchirp)
    yaxis_eta=count_eta/count_evidence
    yaxis_values_eta.append(yaxis_eta)
yaxis_values_m1.sort()
yaxis_values_m2.sort()
yaxis_values_mchirp.sort()
yaxis_values_eta.sort()
quantiles=(np.arange(len(yaxis_values_m1))+0.5)/float(len(yaxis_values_m1))
#dx=1./(len(inj_dirs)+1.)
#per = [dx*(i+1) for i in range(len(inj_dirs))]
#x=[norm.ppf(q,loc=0.,scale=1.) for q in per]
#re_x=[(X-min(x))/(max(x)-min(x)) for X in x]
#plt.scatter(re_x,yaxis_values)
data=np.column_stack([quantiles,yaxis_values_m1,yaxis_values_m2,yaxis_values_mchirp,yaxis_values_eta])
np.savetxt('data_intrinsic_f2y2016_attempt24_test1.txt',data,header='quantiles yaxis_m1 yaxis_m2 yaxis_mchirp yaxis_eta',fmt="%s")

#this part is copied from https://git.ligo.org/lscsoft/bilby/blob/master/bilby/core/result.py
confidence_interval=[0.68, 0.95, 0.997]
confidence_interval_alpha=0.1
x_values = np.linspace(0, 1, 1001)
N=len(quantiles)
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

plt.plot(quantiles,yaxis_values_m1,"-r",label="mass 1")
plt.plot(quantiles,yaxis_values_m2,"-b",label="mass 2")
plt.plot(quantiles,yaxis_values_mchirp,"-g",label="mchirp")
plt.plot(quantiles,yaxis_values_eta,"-y",label="eta")
plt.plot(quantiles,quantiles,"-k",linestyle='dashed')
plt.legend(loc="upper left")
plt.grid()
plt.savefig('pp_plot_intrinsic_f2y2016_attempt24_test1.png')

    
   
