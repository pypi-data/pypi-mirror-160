#!/usr/bin/env python
############################
# 20190314
#
# This script is designed to run over many injections
#
############################

import sys,os,json,ast,random
import subprocess,time
import numpy as np
import configparser
import lal
import rapid_pe.lalsimutils
from argparse import ArgumentParser
#from ligo.gracedb.rest import GraceDb
from modules import *

from ligo import segments
from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

@lsctables.use_in
class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass

from config import Config
cfgname = sys.argv[1]
config = Config.load(cfgname)
script_directory = os.path.dirname(os.path.realpath(__file__))

injections = None
read_inj_index = 0
if ".txt" in config.injections_filename:
    injections = convert_injections_txt_to_objects(config.injections_filename)
    #If it's a text file I generated, you can read the inj index from inj.alpha6
    read_inj_index = 1
else:
    xmldoc = ligolw_utils.load_filename(config.injections_filename, verbose=True,contenthandler=LIGOLWContentHandler)
    injections = lsctables.SimInspiralTable.get_table(xmldoc)    

verbose=1

def main():

    inj_index = 0
    n_submitted = 0
    for inj in injections:
        if read_inj_index:
            #Note: this is only true for the inj files I generated with generate_injections
            #Here the index is set to the index in the original injections file
            inj_index = inj.alpha6

#        from lalinference.rapid_pe import xmlutils, amrlib, lalsimutils
#        print inj_index,amrlib.transform_m1m2_mceta(inj.mass1,inj.mass2)
#        inj_index += 1
#        continue

#        if inj_index != 23:
#            inj_index += 1
#            continue

        event_info = config.common_event_info.copy()

        #If the cache file input includes the expression $INJINDEX$ it will be replaced by the inj index
        if config.use_skymap:
            if "$INJINDEX$" in event_info["skymap_file"]:
                event_info["skymap_file"] = event_info["skymap_file"].replace("$INJINDEX$",str(int(inj_index)))
            if not os.path.isfile(event_info["skymap_file"]):
                sys.exit("ERROR: you've requested use_skymap but the skymap file you've specified doesn't exist:",event_info["skymap_file"])
        if "$INJINDEX$" in event_info["cache_file"]:
            event_info["cache_file"] = event_info["cache_file"].replace("$INJINDEX$",str(int(inj_index)))
        if not os.path.isfile(event_info["cache_file"]):
            print(("ERROR: cache file doesn't exist",event_info["cache_file"]))
            continue

        event_info["output_event_ID"] = "inj_"+str(inj_index)
        output_event_directory = event_info["output_event_ID"]
        output_dir = script_directory+"/"+config.output_parent_directory+"/"+output_event_directory+"/"
        if not os.path.isdir(output_dir):
            os.system("mkdir -p "+output_dir)
        elif os.path.isfile(output_dir+"/event_all_iterations.dag"):
            #skip this inejction if it has already been submitted
            continue


        
        event_info["event_time"] = construct_event_time_string(inj.geocent_end_time,inj.geocent_end_time_ns)
        intr_prms= {"mass1":inj.mass1,"mass2":inj.mass2,"spin1z":inj.spin1z,"spin2z":inj.spin2z}
        intr_prms = check_switch_m1m2s1s2(intr_prms)

        #Save all the true injected values for pp plots or other tests later
        event_info["injection_param"] = "[mass1="+str(intr_prms["mass1"])+",mass2="+str(intr_prms["mass2"])+",spin1z="+str(intr_prms["spin1z"])+",spin2z="+str(intr_prms["spin2z"])+",longitude="+str(inj.longitude)+",latitude="+str(inj.latitude)+",distance="+str(inj.distance)+",inclination="+str(inj.inclination)+",phase="+str(inj.phi0)+",polarization="+str(inj.psi0)+"]"

        #this random variation doesnt consider overlap between templates, shouldn't be used
        #if randomly_vary_Mcnstart:
        #    intr_prms = get_random_varied_Mcnstart(intr_prms)

        event_info["intrinsic_param"] = "["
        first_ip = 1
        for ip in config.intrinsic_param_to_search:
            print("ip",ip,type(config.intrinsic_param_to_search),config.intrinsic_param_to_search)
            event_info["intrinsic_param"] += ip+"="+str(intr_prms[ip]) if first_ip else ","+ip+"="+str(intr_prms[ip])
            first_ip = 0
        event_info["intrinsic_param"] += "]"
#        event_info["intrinsic_param"] = "[mass1="+str(intr_prms["mass1"])+",mass2="+str(intr_prms["mass2"])+"]"

        #We want to know how much each part of this process takes, so we keep a record of the time
        event_info["wrapper_script_start_time"] = time.time()

        #Determine which approximant should be used based on the total mass
        # the threshold is from the gstlal O2 template bank threshold: https://arxiv.org/pdf/1812.05121.pdf
        if float(intr_prms["mass1"])+float(intr_prms["mass2"]) > 10.0:
            #Note: pp-plots injections used SEOBNRv4, NOT SEOBNRv4_ROM
            event_info["approximant"] = "SEOBNRv4"
        else:
#            print ("WARNING: using SEOBNRv4 for BNS********* for testing only")
            #all approximants checked with BNS
            event_info["approximant"] = "TaylorF2"
            #event_info["approximant"] = "TaylorF2"
        #If this is a spinning search, use SpinTaylorT4 instead
            #        event_info["approximant"] = "SpinTaylorT4"


        #Already have the psd, cache file and channels specified in common event info
        if config.submit_only_at_exact_signal_position:
            #Only submit one integrate job at the exact signal position
            cmd = "python "+script_directory+"/create_submit_at_exact_signal_position.py "+cfgname+" '"+json.dumps(event_info)+"'"
            run_cmd(cmd)
        else:
            #Create the initial grid for this event 
            exe_generate_initial_grid = "python "+script_directory+"/generate_initial_grid_based_of_gstlal_O2_overlaps.py"
            if verbose:
                print((exe_generate_initial_grid+" "+cfgname+" '"+json.dumps(event_info)+"'"))

            exit_status = os.system(exe_generate_initial_grid+" "+cfgname+" '"+json.dumps(event_info)+"'")
            if exit_status != 0:
                print((exe_generate_initial_grid+" "+cfgname+" '"+json.dumps(event_info)+"'"))
                sys.exit("ERROR: non zero exit status"+str(exit_status))    

            intrinsic_grid_name_base = "intrinsic_grid"
            event_info["initial_grid_xml"] = intrinsic_grid_name_base+"_iteration_0.xml.gz"
            event_info["initial_grid_hdf"] = intrinsic_grid_name_base+"_all_iterations.hdf"

            #Run create_submit_dag
            cmd = "python "+script_directory+"/create_submit_dag_one_event.py "+cfgname+" '"+json.dumps(event_info)+"'"
            if verbose:
                print(cmd)
            exit_status = os.system(cmd)
            if exit_status != 0:
                print(cmd)
                sys.exit("ERROR: non zero exit status"+str(exit_status))    

        print("Events submitted.",inj_index)
        n_submitted += 1
        if not n_submitted%10:
            os.system("sleep 30")
#        if inj_index > 0:
#            print "Event info"
#            print event_info
#        sys.exit()
        if not read_inj_index:
            inj_index += 1
    return


def get_random_varied_Mcnstart(intr_prm):
    copy = intr_prm.copy()

    mc,eta = get_mchirp_eta(intr_prm["mass1"],intr_prm["mass2"])
    mc += random.uniform(-0.001,0.001)*mc
    eta = eta + random.uniform(-0.001,0.001)*eta
    while eta > 0.25:
        eta = eta + random.uniform(-0.001,0.0)*eta

    m1,m2 = get_m1m2_from_mceta(mc,eta)

##%    #vary m1 and m2 by max 1%, make sure m1 > m2
##%    m1 = intr_prm["mass1"] + random.uniform(-0.01,0.01)*intr_prm["mass1"]
##%    m2 = intr_prm["mass2"] + random.uniform(-0.01,0.01)*intr_prm["mass2"]
##%    while m2 > m1:
##%        m2 = intr_prm["mass2"] + random.uniform(-0.011,0.01)*intr_prm["mass2"]
##%
    copy["mass1"] = m1
    copy["mass2"] = m2
##%
    return copy


if __name__ == '__main__':
    main()
