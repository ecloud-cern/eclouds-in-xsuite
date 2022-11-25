import os
import json
import shutil
import numpy as np
import pickle as pickle
import replaceline as rl

tag_prefix = 'LHC6.8TeV_v1'

tobecopied = ["job.job", "beam1.beam", "beam2.beam", "machine_parameters.input", 
              "secondary_emission_parameters.input", "simulation_parameters.input"]

current_dir = os.path.realpath(__file__)
config_dir = os.path.dirname(current_dir) + "/"
study_folder =  current_dir.split("/config")[0]

scan_folder = study_folder + "/simulations"

with open(config_dir + "/../../eclouds_LHCIT_v1.json","r") as fid:
    eclouds_info = json.load(fid)
#eclouds_info = {"ecloud.q1l5.ir5.63" : eclouds_info["ecloud.q1l5.ir5.63"]}
eclouds_info = {"ecloud.q1r5.ir5.0" : eclouds_info["ecloud.q1r5.ir5.0"]}

fact_beam = 1.2e11
# del_max_vect = np.arange(1.0, 1.61, 0.1)
del_max = 1.35
Dt = 5e-12
energy_eV = 6800e9

#debug
#shutil.rmtree(scan_folder)

os.makedirs(scan_folder, exist_ok=True)
os.makedirs(scan_folder+'/progress', exist_ok=True)

bunchlen = 0.09
prog_num = 0

for key in eclouds_info.keys():
    ecloud = eclouds_info[key]
    beamscreen = ecloud["beamscreen"]
    filename_chm = f"LHC_{beamscreen.upper()}.mat"
    chamber = "../../Beam_chambers/" + filename_chm
    ecloud_type = key.split(".")[1]
    ecloud_index = key.split(".")[3]
    
    prog_num +=1

    # current_sim_ident = f"{tag_prefix}_{ecloud_type.upper()}_{ecloud_index}_sey{del_max:.2f}_{fact_beam/1e11:.2f}e11ppb_3x48_N100000_Dt{Dt:.1e}_Dhb0.5e-4_Dhcsc{Dh_sc:.1e}_Dtsc_0.5e-9"
    # current_sim_ident = f"{tag_prefix}_{ecloud_type.upper()}_{ecloud_index}_sey{del_max:.2f}_{fact_beam/1e11:.2f}e11ppb_3x48_N100000_Dt{Dt:.1e}_Dhb0.5e-4_Dhcsc0.1e-3"
    current_sim_ident = f"{tag_prefix}_{ecloud_type.upper()}_{ecloud_index}_sey{del_max:.2f}_{fact_beam/1e11:.2f}e11ppb"

    current_sim_folder = scan_folder+'/'+current_sim_ident
    os.mkdir(current_sim_folder)
    sim_tag = tag_prefix+'%05d'%prog_num
    print(sim_tag, current_sim_ident)
    
    rl.replaceline_and_save(fname = config_dir + "secondary_emission_parameters.input",
                            findln = "del_max =", newline = f"del_max = {del_max:f}\n")
    
    
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "energy_eV =", newline = f"energy_eV = {energy_eV:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "energy_eV =", newline = f"energy_eV = {energy_eV:e}\n")

    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "fact_beam =", newline = f"fact_beam = {fact_beam:e}\n")
    rl.replaceline_and_save(fname = config_dir + 'beam2.beam',
                            findln = "fact_beam =", newline = f"fact_beam = {fact_beam:e}\n")

    rl.replaceline_and_save(fname = config_dir + "machine_parameters.input",
                            findln = "filename_chm =", newline = f"filename_chm = '{filename_chm}'\n")

    Bgrad = ecloud["Bgrad"]
    rl.replaceline_and_save(fname = config_dir + "machine_parameters.input",
                            findln = "B_multip =", newline = f"B_multip = [0., {Bgrad:e}]\n")
    rl.replaceline_and_save(fname = config_dir + "machine_parameters.input",
                            findln = "B_skew =", newline = f"B_skew = [0., 0.]\n")

    x_b1 = ecloud["x_b1"]
    y_b1 = ecloud["y_b1"]
    sigx_b1 = ecloud["sigx_b1"]
    sigy_b1 = ecloud["sigy_b1"]
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "x_beam_pos =", newline = f"x_beam_pos = {x_b1:e}\n")			
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "y_beam_pos =", newline = f"y_beam_pos = {y_b1:e}\n")			
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "t_offs =", newline = "t_offs = 2.5e-9\n")		
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "sigmax =", newline = f"sigmax = {sigx_b1:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "sigmay =", newline = f"sigmay = {sigy_b1:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam1.beam",
                            findln = "sigmaz =", newline = f"sigmaz = {bunchlen:e}\n")

    x_b2 = ecloud["x_b2"]
    y_b2 = ecloud["y_b2"]
    sigx_b2 = ecloud["sigx_b2"]
    sigy_b2 = ecloud["sigy_b2"]
    t_offset_s = ecloud["t_offset_s"]
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "x_beam_pos =", newline = f"x_beam_pos = {x_b2:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "y_beam_pos =", newline = f"y_beam_pos = {y_b2:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "t_offs =", newline = f"t_offs = 2.5e-9 + ({t_offset_s:e})\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "sigmax =", newline = f"sigmax = {sigx_b2:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "sigmay =", newline = f"sigmay = {sigy_b2:e}\n")
    rl.replaceline_and_save(fname = config_dir + "beam2.beam",
                            findln = "sigmaz =", newline = f"sigmaz = {bunchlen:e}\n")

    edens_probes =f"el_density_probes = [{{'x' : {x_b1:e}, 'y': {y_b1:e}, 'r_obs': 1e-3}},{{'x' : {x_b2:e}, 'y': {y_b2:2}, 'r_obs': 1e-3}}]\n"
    rl.replaceline_and_save(fname = config_dir + "simulation_parameters.input",
                            findln = "el_density_probes =", newline = edens_probes)

    rl.replaceline_and_save(fname = config_dir + "simulation_parameters.input",
                            findln = "logfile_path =", newline = "logfile_path = "+"'"+ current_sim_folder+"/logfile.txt"+"'\n")
    rl.replaceline_and_save(fname = config_dir + "simulation_parameters.input",
                            findln = "progress_path =", newline = "progress_path = "+"'" + scan_folder+"/progress/" +sim_tag+"'\n")
    rl.replaceline_and_save(fname = config_dir + "simulation_parameters.input",
                            findln = "stopfile =", newline = "stopfile = '"+scan_folder+"/progress/stop'\n")
    rl.replaceline_and_save(fname = config_dir + 'job.job',
                            findln = 'CURRDIR=/',
                            newline = 'CURRDIR='+current_sim_folder)

    shutil.copy(config_dir + chamber, current_sim_folder)
    
    for ff in tobecopied:
        shutil.copy(config_dir + "/" + ff, current_sim_folder)
#    os.system('cp -r %s %s'%(tobecopied, current_sim_folder))

## for ii,device in enumerate(multipoles):
##     
##     mag_curr = device+'poles'
## 
##     for i in xrange(len(multip_dict[mag_curr]['name'])):
##         name_curr = multip_dict[mag_curr]['name'][i]    
##         s = len(multip_dict[mag_curr]['slice'])
##         
##         for del_max in del_max_vect:
##                  
##                 
##     
##     
##         
## os.chmod(study_folder+'/run',0755)
## 
## 
## import htcondor_config as htcc
## htcc.htcondor_config(scan_folder, time_requirement_days=2.)

