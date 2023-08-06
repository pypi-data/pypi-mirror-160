#!python
############################
# 20190227
#
# This script is designed to be triggered automatically for an lvalert trigger
#
# It gets the relevant data, based on the event-time. 
# Then it passes all relevant information to the create_submit_dag
# The cfg name is hardcoded, it has to be because the lvalert can only run a script as is, no input arguments
#
# NOTE: this is setup for superevent triggers, where it takes the "preferred event" info
#
############################
#author  Sinead Walsh
#edit: Vinaya Valsan
#python lvalert_submit_rapidpe_m1m2_O3_edit.py --superid S190828l --cfg config_rapidpe.ini
#
import sys,os,json,ast,time
import subprocess,datetime
import numpy as np
import configparser
import lal
from rapid_pe import lalsimutils
from argparse import ArgumentParser
from ligo.gracedb.rest import GraceDb
from modules import *
from configparser import ConfigParser
cfg = ConfigParser()
cfg.optionxform = str

parser = ArgumentParser()

parser.add_argument('--superid', default=None, type=str)
parser.add_argument('--graceid', default=None, type=str)
parser.add_argument('--cfg',default="ini_files/Example_m1m2_O3online_rerun.ini", type=str)
parser.add_argument('--m1', default=None, type=float,help="Optional:set m1 to a diff value than given by gracedb")
parser.add_argument('--m2', default=None, type=float,help="Optional:set m2 to a diff value than given by gracedb")
parser.add_argument('--append_event_id',default="", type=str,help="Optional: append a string to the output dir to distinguish it from prev runs with this event. Recommendation: give _xyz as input, not just xyz")
parser.add_argument('--force_lowlat_data',action='store_true', help="Optional: force script to use 1 second low latency data, even if this is not an automatic lvalert")

args = parser.parse_args()

script_directory = os.path.dirname(os.path.realpath(__file__))
#The cfg needs to be a full path
if not args.cfg[:1] == "/":
    args.cfg = script_directory+"/"+args.cfg
#print args.cfg
#sys.exit()

#print ("cfg file:",args.cfg)
cfg.read(args.cfg)

if cfg.getint("General","event_parameters_in_config_file") == 1:
    sys.exit("ERROR: this cfg file expects the event params to by in the cfg file, instead of passed from here")

output_parent_directory= cfg.get("General","output_parent_directory") 
use_skymap= cfg.get("General","use_skymap")  if cfg.has_option("General","use_skymap") else 0 
fmin_template = cfg.getfloat("LikelihoodIntegration","fmin-template")
email_address_for_job_complete_notice = cfg.get("General","email_address_for_job_complete_notice") if cfg.has_option("General","email_address_for_job_complete_notice") else ""
intrinsic_param_to_search = ast.literal_eval(correct_list_string_formatting(cfg.get("General","intrinsic_param_to_search"))) if cfg.has_option("General","intrinsic_param_to_search") else ["mass1","mass2"]

client = GraceDb('https://gracedb.ligo.org/api/')
#pycbc was removed from the list of allowed pipelines because we can't use the psd uploaded for pycbc events
allowed_pipelines = ["gstlal","spiir","MBTAOnline"]

verbose=True

#graceID used for testing
#args.graceid = "G296853"
#args.graceid = "G327903"
#args.graceid = "G327902"
#args.graceid = "S190328af"

def main():

    #Get event info from trigger. For testing, a default event is read if no trigger is given as input.
    event = None
    submitter=""
    packet = ""
    lvalert=False
    if args.superid:
        sevent= client.superevent(args.superid).json()
        args.graceid=sevent['preferred_event']

    if args.graceid is None and  args.superid is None: #This means it's a lvalert trigger        
        packet = json.loads(sys.stdin.read())
        lvalert=True
        #Check if FAR is worth following up
        if str(packet["alert_type"]) != "new" or packet["object"]["far"]  > 5e-7:
#            if str(packet["alert_type"]) != "log":
            print(("Not interesting:"+packet['uid']+" "+packet["alert_type"]+" "+str(packet["object"]["far"])))
            sys.exit()
        else:
            print(("Interesting event:"+packet['uid']+" "+packet["alert_type"]+" "+str(packet["object"]["far"])))
#            sys.exit()


        if email_address_for_job_complete_notice != "":
            email_cmd = "echo 'Lvalert "+str(packet)+"' | mail -s 'rapidPE:"+output_parent_directory+"' "+email_address_for_job_complete_notice+"\n"
            os.system(email_cmd)

        args.graceid = get_graceid_after_superevent_check(packet['uid'],packet=packet)

    else:
        args.graceid = get_graceid_after_superevent_check(args.graceid)
    
    event = client.event(args.graceid).json()
    insp_type = event["extra_attributes"]
    pipeline = event["pipeline"]

    print(("event info",event))

    # Take the information from the first detector. Template parameters are required to be the same across templates for gstlal
    coinc = insp_type["CoincInspiral"]

    #Get the data files for this event
    #for now ignoring Virgo and any single detector triggers
    ifos = coinc["ifos"]

    #gather event info in format needed for following scripts
    params = insp_type["SingleInspiral"][0]
    event_info = {}
    #add a date to this
    date = str(datetime.date.today()).replace('-','')
    creation_date = event["created"]
    creation_date = str(creation_date.split(" ")[0].replace("-",""))
    event_info["output_event_ID"] = date+"_"+pipeline+"_"+creation_date+"_"+args.graceid+args.append_event_id
    event_info["event_time"] = construct_event_time_string(params["end_time"],params["end_time_ns"])
    event_info["intrinsic_param"] = "["
    first_ip = 1
    for ip in intrinsic_param_to_search:
        print("ip",ip,type(intrinsic_param_to_search),intrinsic_param_to_search)
        event_info["intrinsic_param"] += ip+"="+str(params[ip]) if first_ip else ","+ip+"="+str(params[ip])
        first_ip = 0
    event_info["intrinsic_param"] += "]"
    if args.m1 is not None and args.m2 is not None:
        print ("*** Warning: spin ignored when masses given as args")
        event_info["intrinsic_param"] = "[mass1="+str(args.m1)+",mass2="+str(args.m2)+"]"
        event_info["output_event_ID"] = event_info["output_event_ID"]+"_m1"+str(int(args.m1))+"_m2"+str(int(args.m2))

    #We want to know how much each part of this process takes, so we keep a record of the time                                                              
    event_info["wrapper_script_start_time"] = time.time()
    #Determine which approximant should be used based on the total mass
    # the threshold is from the gstlal O2 template bank threshold: https://arxiv.org/pdf/1812.05121.pdf
    #NRHybridSurrogate up to q=8, should work with everything. review finishing now. Ask seb?
    #At very high mass, waveform generator will fail. No inspiral phase at very high mass. Waveform generator requires you to start at inspiral phase.
    if float(params["mass1"])+float(params["mass2"]) > 10.0:
        event_info["approximant"] = "SEOBNRv4_ROM" #v4 vs v4_ROM
    else:
        event_info["approximant"] = "TaylorT2"
#        event_info["approximant"] = "TaylorF2" #highest speed. 
        if "spin1z" in intrinsic_param_to_search:
        #If this is a spinning search, use SpinTaylorT4 instead
            event_info["approximant"] = "SpinTaylorT4"

    output_event_directory = event_info["output_event_ID"]
    output_dir = script_directory+"/"+output_parent_directory+"/"+output_event_directory+"/"
    if not os.path.isdir(output_dir):
        os.system("mkdir -p "+output_dir)
    if packet != "":
        os.system("echo '"+str(packet)+"' > "+output_dir+"/lvalert_packet.txt")


    #the PSD file name is set here, but it's written later because sometimes it takes a while for the file to upload
    psd_filename = output_dir+"/psd.xml.gz"
    skymap_filename = output_dir+"/bayestar.fits"
    os.chdir(output_dir)

    #Now, based on the event_time, find the frame files you want.
    channel_str = "["
    psd_file_str = "["
    for insp in insp_type["SingleInspiral"]:
        #Ignore V1 if both L1 and H1 available
        #if not insp["ifo"] in ["H1","L1"]:# and "H1" in ifos and "L1" in ifos:
        #    print ("Ignoring V1")
        #    continue

        channel = insp["channel"]
        ifo = insp["ifo"]
        #channel = "GDS-CALIB_STRAIN" if not ifo == "V1" else insp["channel"]
        channel_str += ifo+"="+channel+","
        psd_file_str += ifo+"="+psd_filename+","
        if verbose:
            print(ifo)
        #Copied from Richards code https://git.ligo.org/richard-oshaughnessy/research-projects-RIT/blob/temp-RIT-Tides-port_master-GPUIntegration/MonteCarloMarginalizeCode/Code/helper_LDG_Events.py
        # Estimate signal duration
        t_event = insp["end_time"] 
        P=lalsimutils.ChooseWaveformParams()
        P.m1 = insp["mass1"]*lal.MSUN_SI
        P.m2=insp["mass2"]*lal.MSUN_SI
        P.fmin = fmin_template
        P.tref = t_event
        t_duration  = np.max([ coinc["minimum_duration"], lalsimutils.estimateWaveformDuration(P)])
        print("DONE Estimate duration",t_duration,coinc["minimum_duration"], lalsimutils.estimateWaveformDuration(P))
        t_before = np.max([4,t_duration])*1.2+30  # buffer for inverse spectrum truncation
        data_start_time = int(t_event - int(t_before))
        data_end_time = int(t_event + int(500)) 

#        data_type = ifo+"_llhoft" if lvalert or "V1" in ifos and not ("H1" in ifos and "L1" in ifos) else ifo+"_HOFT_C00"
        #data_type = ifo+"_llhoft" if lvalert or args.force_lowlat_data else ifo+"_HOFT_C00"
        data_type = ifo+"Online" if ifo=="V1" else ifo+"_HOFT_C00"
        dcmd = "python -m gwdatafind -u file -o "+ifo[0]+" -t "+data_type+" -s "+str(data_start_time)+" -e "+str(data_end_time)+" > "+ifo[0]+"_raw.cache"
        if verbose:
            print(dcmd)
        exit_status = os.system(dcmd)
        if exit_status != 0:
            print(dcmd)
            sys.exit("ERROR: non zero exit status"+str(exit_status))    

    #path2cache always assumes data is in output_dir, so that path needs to be removed before passing output to data.cache
    text_for_sed_removal = "localhost"+output_dir.replace("/","\/")+"file:\/"
    os.system("cat *_raw.cache | lalapps_path2cache | sed 's/"+text_for_sed_removal+"//g' > data.cache")

    #Check if the data.cache file is empty
    if os.stat("data.cache").st_size == 0:
        if lvalert and (email_address_for_job_complete_notice != ""):
            email_cmd = "echo 'Failed Lvalert, no data at trigger time "+str(gid)+"' | mail -s 'rapidPE:"+output_parent_directory+"' "+email_address_for_job_complete_notice+"\n"
            os.system(email_cmd)
        sys.exit("ERROR: There is no data at the time when this triggered, how can that happen")


    #put together cache file
    event_info["cache_file"] = output_dir+"/data.cache"
    event_info["psd_file"] =  psd_file_str[:-1]+"]"    
    event_info["channel_name"] = channel_str[:-1]+"]"    

    #Create the initial grid for this event 
    exe_generate_initial_grid = "python "+script_directory+"/generate_initial_grid_based_of_gstlal_O2_overlaps.py"
    if verbose:
        print((exe_generate_initial_grid+" "+args.cfg+" '"+json.dumps(event_info)+"'"))

    exit_status = os.system(exe_generate_initial_grid+" "+args.cfg+" '"+json.dumps(event_info)+"'")
    if exit_status != 0:
        print((exe_generate_initial_grid+" "+args.cfg+" '"+json.dumps(event_info)+"'"))
        sys.exit("ERROR: non zero exit status"+str(exit_status))    

    intrinsic_grid_name_base = "intrinsic_grid"
    event_info["initial_grid_xml"] = intrinsic_grid_name_base+"_iteration_0.xml.gz"
    event_info["initial_grid_hdf"] = intrinsic_grid_name_base+"_all_iterations.hdf"

    #Get the psd file and write locally
    #This is done after the intrinsic grid generation because sometimes the file takes time to upload
    psdfileobj = open(psd_filename, 'wb')
    r = client.files(args.graceid, 'psd.xml.gz')
    psdfileobj.write(r.read())
    psdfileobj.close()

    if use_skymap:
        skymapfileobj = open(skymap_filename, 'wb')
        if args.superid:
            r = client.files(args.superid, 'bayestar.fits.gz')
        else:
            r = client.files(args.graceid, 'bayestar.multiorder.fits')
        skymapfileobj.write(r.read())
        skymapfileobj.close()
        event_info["skymap_file"] =  skymap_filename



    #Run create_submit_dag
    cmd = "python "+script_directory+"/create_submit_dag_one_event.py "+args.cfg+" '"+json.dumps(event_info)+"'"
    if verbose:
        print(cmd)
    exit_status = os.system(cmd)
    if exit_status != 0:
        print(cmd)
        sys.exit("ERROR: non zero exit status"+str(exit_status))    
    elif email_address_for_job_complete_notice != "":
        email_cmd = "echo 'Sent for dag submission "+json.dumps(event_info)+"' | mail -s 'rapidPE:"+output_parent_directory+"' "+email_address_for_job_complete_notice+"\n"
        os.system(email_cmd)


    return

def get_graceid_after_superevent_check(gid,packet=None):
    '''
    If the event is a superevent get the graceDB ID from the preferred event
    If the preferred event is a CWB event (i.e. it doesn't have m1 m2 end_time), get a gstlal ID (highest snr gstlal).
    If there's no gstlal ID, choose another CBC ID by highest snr. If it's only a CWB event, ignore
    '''
    other_gids = None
    if "S" in gid:
        if packet is None:
            sevent = client.superevent(gid).json()
            #Set the args.graceid to the preferred event id
            gid = sevent["preferred_event"]
            other_gids = sevent["gw_events"]
        else:
            #Set the args.graceid to the preferred event id
            gid = packet["object"]["preferred_event"]
            other_gids = packet["object"]["gw_events"]

    event = client.event(gid).json()
    pipeline = event["pipeline"]    
    #CWB is unmodelled, it doesn't have a m1m2s1s2 to start with. we want to use a modelled gracedb event
    if not pipeline in allowed_pipelines:
        if other_gids is None:
            sys.exit("ERROR: can't submit rapidPE for non-cbc events. They're unmodelled, i.e. no intrinsic point to start with. pipeline=",pipeline)
        elif len(other_gids) == 1:
            gid = -1
        else:
            #Get the pipelines and snrs for each graceDB ID, choose one.
            cbcgid=prev_snr = -1
            for tmpid in other_gids:
                if not tmpid == gid:
                    event = client.event(tmpid).json()
                    if not event["pipeline"] in allowed_pipelines:
                        continue
                    else:
                        snr = event["snr"]
                        if snr > prev_snr:
                            cbcgid= tmpid
                            prev_snr = snr
            gid = cbcgid

    if gid == -1:
        #If this is an lvalert, want to send an email explaining there was an interesting event but it wasn't pursued
        if not packet is None:
            email_cmd = "echo 'Unmodelled Lvalert, no cbc entries available, ignoring.  "+str(gid)+"' | mail -s 'rapidPE:"+output_parent_directory+"' "+email_address_for_job_complete_notice+"\n"
            os.system(email_cmd)

        sys.exit("ERROR: Only non-cbc event(s) for this (super)event. Can't submit rapidpe. gids="+str(other_gids))
    else:
        return gid

        

        





if __name__ == '__main__':
    main()
