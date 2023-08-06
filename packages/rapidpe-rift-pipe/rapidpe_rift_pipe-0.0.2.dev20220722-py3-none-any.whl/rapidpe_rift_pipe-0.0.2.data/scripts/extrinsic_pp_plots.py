import numpy as np 
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats
import glob, re, ast
from glue.ligolw import utils, table, lsctables, ligolw
lsctables.use_in(ligolw.LIGOLWContentHandler)

def chirpdist_to_lumdist(chirpdist,m1,m2):
    mchirp_bns=(1.4*1.4)**(3./5.)/(1.4+1.4)**(1./5.)
    mchirp=(m1*m2)**(3./5.)/(m1+m2)**(1./5.)
    lumdist=chirpdist*(mchirp/mchirp_bns)**(5./6.)
    return(lumdist)
def lumdist_to_chirpdist(lumdist,mchirp):
    mchirp_bns=(1.4*1.4)**(3./5.)/(1.4+1.4)**(1./5.)
    
    chirpdist=lumdist*(mchirp/mchirp_bns)**(-5./6.)
    return(chirpdist)

lumdist_to_chirpdist_func  =  np.vectorize(lumdist_to_chirpdist)

def m1_func(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.+np.sqrt(1.-4.*eta)))
def m2_func(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.-np.sqrt(1.-4.*eta)))

def mchirp_Func(m1,m2):
    return(((m1*m2)**(3./5.))*((m1+m2)**(-1./5.)))
mchirp_func = np.vectorize(mchirp_Func)

def eta_func(m1,m2):
    return((m1*m2)*((m1+m2)**(-2.)))

def mass_prior_func(m1,m2):
    mchirp = mchirp_func(m1,m2)
    eta = eta_func(m1,m2)
    return(np.abs(mchirp*np.power(eta,-6./5.)*(1./np.sqrt(1.-4.*eta)))/(0.4**2.))

mass_prior = np.vectorize(mass_prior_func)
def lum_d_prior_func(lum_d,mchirp):
    # uniform in chirp_distance as a function of lum_distance
    mfunc=(mchirp_func(1.4,1.4)/mchirp)**(15/6)
    ch_d = lumdist_to_chirpdist(lum_d,mchirp)
    if ch_d>ch_max or ch_d<ch_min:
        p=0.
    else:
        p= 3.*lum_d**2.*mfunc/(ch_max**3.-ch_min**3.)
    return p

lum_d_prior = np.vectorize(lum_d_prior_func)

psi_prior=1./np.pi
phi_prior=1./(2.*np.pi)
def theta_prior(theta):
    return np.sin(theta)/2.
ra_prior=1./(2.*np.pi)

def dec_prior(dec):
    return np.cos(dec)/2.

ch_min,ch_max=109.0, 435.0

input_dir = "/home/vinaya.valsan/rapidPE/inj_data/automated_rapidpe_submission/output/f2y2016_HLV_attempt24/"
inj_dirs=glob.glob(input_dir+"inj_*")
yaxis_values_distance=[]
yaxis_values_latitude=[]
yaxis_values_longitude=[]
yaxis_values_inclination=[]
yaxis_values_phase=[]
yaxis_values_polarization=[]

for inj_dir in inj_dirs:
    print(inj_dir)
    results_dir=inj_dir+"/results/"
    samples_xml_file= glob.glob(results_dir+"*.samples.xml.gz")

    event_info=open(inj_dir+"/event_info_dict.txt","r")
    contents = event_info.read()
    dictionary = ast.literal_eval(contents)
    mass_inj = dictionary["intrinsic_param"]
    mass1_inj = re.search('mass1=(.+?)"',mass_inj)
    mass1_inj = mass1_inj.group(1)
    mass1_inj = float(mass1_inj)
    mass2_inj = re.search('mass2=(.+?)"',mass_inj)
    mass2_inj = mass2_inj.group(1)
    mass2_inj = float(mass2_inj)
    inj_param = dictionary["injection_param"]
    chirpdistance_inj = re.search('distance=(.+?)"',inj_param)
    chirpdistance_inj = float(chirpdistance_inj.group(1))
    latitude_inj = re.search('latitude=(.+?)"',inj_param)
    latitude_inj = float(latitude_inj.group(1))
    longitude_inj = re.search('longitude=(.+?)"',inj_param)
    longitude_inj = float(longitude_inj.group(1))
    inclination_inj = re.search('inclination=(.+?)"',inj_param)
    inclination_inj = float(inclination_inj.group(1))
    phase_inj = re.search('phase=(.+?)"',inj_param)
    phase_inj = float(phase_inj.group(1))
    polarization_inj = re.search('polarization=(.+?)"',inj_param)
    polarization_inj = float(polarization_inj.group(1))
    lumdistance_inj = chirpdist_to_lumdist(chirpdistance_inj,mass1_inj,mass2_inj)
   
    count_evidence=0.
    count_distance=0.
    count_latitude=0.
    count_longitude=0.
    count_inclination=0.
    count_phase=0.
    count_polarization=0.

    for i in range(len(samples_xml_file)):
        Mass1=[]
	Mass2=[]
        Distance=[]
        Latitude=[]
        Longitude=[]
        Inclination=[]
        Phase=[]
        Polarization=[]
        LogLikelihood=[]
        Prior=[]
        SamplingFunction=[]
        samples_filename=samples_xml_file[i]
        xmldoc = utils.load_filename(samples_filename, contenthandler=ligolw.LIGOLWContentHandler)
        new_tbl = lsctables.SimInspiralTable.get_table(xmldoc)
        for row in new_tbl:
            Mass1.append(row.mass1)
	    Mass2.append(row.mass2)
            Distance.append(row.distance)
            Latitude.append(row.latitude)
            Longitude.append(row.longitude)
            Inclination.append(row.inclination)
            Phase.append(row.coa_phase)
            Polarization.append(row.polarization)
            LogLikelihood.append(row.alpha1)
            Prior.append(row.alpha2)
            SamplingFunction.append(row.alpha3)
        mass1 = np.asarray(Mass1)
        mass2 = np.asarray(Mass2)
        distance=np.asarray(Distance)
        latitude=np.asarray(Latitude)
        longitude=np.asarray(Longitude)
        inclination=np.asarray(Inclination)
        phase=np.asarray(Phase)
        polarization=np.asarray(Polarization)
        likelihood=np.asarray(np.exp(LogLikelihood))
        #ini_prior=np.asarray(Prior)
        #mass1_rand=np.random.uniform(1.2,1.6,len(distance))
        #mass2_rand=np.random.uniform(1.2,1.6,len(distance))
        #mchirp = mchirp_func(mass1,mass2)
        #ch_d =  lumdist_to_chirpdist_func(distance,mchirp)
        prior=[]
        for  ii in range(len(distance)):
            mchirp = mchirp_Func(mass1[ii],mass2[ii])
            #ch_d = lumdist_to_chirpdist(distance[ii],mchirp)
            #p = mass_prior_func(mass1[ii],mass2[ii])*
	    p =  lum_d_prior_func(distance[ii],mchirp)*psi_prior*phi_prior*ra_prior*(np.sin(inclination[ii])/2.)*np.cos(latitude[ii])/2.
	    prior.append(p)
        #prior = mass_prior(mass1,mass2)*lum_d_prior(distance,mchirp)*psi_prior*phi_prior*ra_prior*(np.sin(inclination)/2.)*np.cos(latitude)/2.
        #print(len(prior),len(mchirp),len(distance)) 
        sampling_function=np.asarray(SamplingFunction)
        jacobian=1./(4.*np.pi*distance**3.)
        Fofrandoms=likelihood*prior/sampling_function
        random_F=np.random.uniform(0,np.amax(Fofrandoms),size=len(Fofrandoms))
        area_sampled=np.amax(Fofrandoms)
        for j in range(len(Fofrandoms)):
            if random_F[j]<=Fofrandoms[j]:
                count_evidence+=1.*area_sampled
                if distance[j]<=lumdistance_inj:
                    count_distance+=1.*area_sampled
                if latitude[j]<=latitude_inj:
                    count_latitude+=1.*area_sampled
                if longitude[j]<=longitude_inj:
                    count_longitude+=1.*area_sampled
                if inclination[j]<=inclination_inj:
                    count_inclination+=1.*area_sampled
                if phase[j]<=phase_inj:
                    count_phase+=1.*area_sampled
                if polarization[j]<=polarization_inj:
                    count_polarization+=1.*area_sampled
    try:
        yaxis_distance=count_distance/count_evidence
    except:
        continue
    yaxis_values_distance.append(yaxis_distance)
    yaxis_latitude=count_latitude/count_evidence
    yaxis_values_latitude.append(yaxis_latitude)
    yaxis_longitude=count_longitude/count_evidence
    yaxis_values_longitude.append(yaxis_longitude)
    yaxis_inclination=count_inclination/count_evidence
    yaxis_values_inclination.append(yaxis_inclination)
    yaxis_phase=count_phase/count_evidence
    yaxis_values_phase.append(yaxis_phase)
    yaxis_polarization=count_polarization/count_evidence
    yaxis_values_polarization.append(yaxis_polarization)
yaxis_values_distance.sort()
yaxis_values_latitude.sort()
yaxis_values_longitude.sort()
yaxis_values_inclination.sort()
yaxis_values_phase.sort()
yaxis_values_polarization.sort()
quantiles=(np.arange(len(yaxis_values_distance))+0.5)/float(len(yaxis_values_distance))
data=np.column_stack([quantiles,yaxis_values_distance,yaxis_values_latitude,yaxis_values_longitude,yaxis_values_inclination,yaxis_values_phase,yaxis_values_polarization])
np.savetxt('data_extrinsic_f2y2016_HLV_attempt24_v10_test1.txt',data,header='quantiles distance latitude longitude inclination phase polarization',fmt="%s")

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

plt.plot(quantiles,yaxis_values_distance,"-b",label="distance")
plt.plot(quantiles,yaxis_values_latitude,"-r",label="latitude")
plt.plot(quantiles,yaxis_values_longitude,"-g",label="longitude")
plt.plot(quantiles,yaxis_values_inclination,"-m",label="inclination")
plt.plot(quantiles,yaxis_values_phase,"-y",label="phase")
plt.plot(quantiles,yaxis_values_polarization,"-c",label="polarization")
plt.plot(quantiles,quantiles,"-k",linestyle='dashed')
plt.legend(loc="upper left")
plt.grid()
plt.savefig('pp_plot_extrinsic_f2y2016_HLV_attempt24_v10_test1.png')
