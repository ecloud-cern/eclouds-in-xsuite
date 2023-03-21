import json
import shutil
import os
import scipy.io
from scipy.constants import c,e
import matplotlib.pyplot as plt
import numpy as np
from cmcrameri import cm

import replaceline as rl
from PyECLOUD.buildup_simulation import BuildupSimulation

import ecloud_xsuite_filemanager as exfm

mod_factor = 2
sey=1.35
with open("../../eclouds_LHCIT_v1.json","r") as fid:
    eclouds_info = json.load(fid)

ecloud = "ecloud.q1r5.ir5.0"
beam_chamber_filename = "LHC_" + eclouds_info[ecloud]["beamscreen"].upper() + ".mat"

_, ecloud_type, _, index = ecloud.split(".")
buildup_folder = "/eos/project/e/ecloud-simulations/kparasch/LHC_Triplets/" + \
                f"Buildup/run3_bet30cm_160urad_1.2e11ppb_2.0um/simulations_SEY{sey:.2f}/" + \
                f"LHC6.8TeV_v1_{ecloud_type.upper()}_{index}_sey{sey:.2f}_1.20e11ppb/"

shutil.copyfile(buildup_folder + "simulation_parameters.input", "./simulation_parameters.input")
shutil.copyfile(buildup_folder + "secondary_emission_parameters.input", "./secondary_emission_parameters.input")
shutil.copyfile(buildup_folder + "machine_parameters.input", "./machine_parameters.input")
shutil.copyfile(buildup_folder + "beam1.beam", "./beam1.beam")
shutil.copyfile(buildup_folder + "beam2.beam", "./beam2.beam")
shutil.copyfile(buildup_folder + beam_chamber_filename, "./" + beam_chamber_filename)
mp_states = []
for ii in range(20):
    shutil.copyfile(buildup_folder + f"MP_state_{ii}", f"./MP_state_{ii}")
    mp_states.append(scipy.io.loadmat(f"MP_state_{ii}"))

t_min = 2.5e-9 - 0.4 / c
t_max = 2.5e-9 + 0.4 / c
total_N_particles = sum([mp_system["N_mp"][0][0] for mp_system in mp_states])
total_N_particles *= 3. #put 10% more particles to max allowed


current_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
rl.replaceline_and_save(fname = "secondary_emission_parameters.input",
                        findln = "del_max = ", newline = "del_max = 0.\n")
print(current_dir)
rl.replaceline_and_save(fname = "simulation_parameters.input",
                        findln = "N_mp_max=", newline = f"N_mp_max={total_N_particles}\n")
rl.replaceline_and_save(fname = "simulation_parameters.input",
                        findln = "Dt_sc = ", newline = "Dt_sc = 5.e-12\n")
rl.replaceline_and_save(fname = "simulation_parameters.input",
                        findln = "logfile_path =", newline = "logfile_path = "+"'"+ current_dir + "/logfile.txt"+"'\n")
rl.replaceline_and_save(fname = "simulation_parameters.input",
                        findln = "progress_path =", newline = "progress_path = "+"'" + current_dir + "/progress"+"'\n")
rl.replaceline_and_save(fname = "simulation_parameters.input",
                        findln = "stopfile =", newline = "stopfile = '" + current_dir + "/stop'\n")

nsigma = 7.5
xc = eclouds_info[ecloud]["x_b1"]
yc = eclouds_info[ecloud]["y_b1"]
sigx = eclouds_info[ecloud]["sigx_b1"]
sigy = eclouds_info[ecloud]["sigy_b1"]

betx = eclouds_info[ecloud]["betx_b1"]
bety = eclouds_info[ecloud]["bety_b1"]

xmax = xc + nsigma*sigx
xmin = xc - nsigma*sigx
ymax = yc + nsigma*sigy
ymin = yc - nsigma*sigy

print(f"x_max = {xmax:.3e} m")
print(f"x_min = {xmin:.3e} m")
print(f"y_max = {ymax:.3e} m")
print(f"y_min = {ymin:.3e} m")

with open("simulation_parameters.input", "a") as myfile:
    myfile.write("PyPICmode = 'ShortleyWeller_WithTelescopicGrids'\n")
    myfile.write(f"target_grid = {{ ")
    myfile.write(f"'x_min_target' : {xmin:.3e}, 'x_max_target' : {xmax:.3e}, ")
    myfile.write(f"'y_min_target' : {ymin:.3e}, 'y_max_target' : {ymax:.3e}, ")
    myfile.write(f"'Dh_target' : 2.e-5}}\n")
    myfile.write(f"f_telescope = 0.5\n")
    myfile.write(f"N_nodes_discard = 10\n")
    myfile.write(f"N_min_Dh_main = 50\n")



sim = BuildupSimulation(extract_sey=False)
t_end_sim = None

sim.cloud_list[0].MP_e.init_from_dict(scipy.io.loadmat("./MP_state_0"))
prev_mp = sim.cloud_list[0].MP_e.N_mp
for ii in range(1,20):
    sim.cloud_list[0].MP_e.add_from_file(scipy.io.loadmat(f"./MP_state_{ii}"))
    now_mp = sim.cloud_list[0].MP_e.N_mp
    #print(now_mp, mp_states[ii]["N_mp"][0][0], now_mp - prev_mp)
    prev_mp = now_mp



print("Start timestep iter")

## simulation
def time_step(sim, t_end_sim=None):
    beamtim = sim.beamtim
    if t_end_sim is not None and beamtim.tt_curr is not None:
        if beamtim.tt_curr >= t_end_sim:
            print("Reached user defined t_end_sim --> Ending simulation")
            return 1
 
    beamtim.next_time_step()
 
    if sim.flag_presence_sec_beams:
        for sec_beam in sim.sec_beams_list:
            sec_beam.next_time_step()
 
    sim.sim_time_step(force_reinterp_fields_at_substeps=True, skip_MP_cleaning=True, skip_MP_regen=True)
 
    if beamtim.flag_new_bunch_pass:
        print(
            "**** Done pass_numb = %d/%d\n"
            % (beamtim.pass_numb, beamtim.N_pass_tot)
        )
    return 0


out_pinch = "pinch.h5"
exfm.dict_to_h5({"hello" : 1}, out_pinch, group='hello', readwrite_opts='w')

xg = sim.spacech_ele.xg
yg = sim.spacech_ele.yg
zg = []
XX, YY = np.meshgrid(xg,yg, indexing="ij")
fig = plt.figure(1)
ii = 0
jj = 0
t_end_sim = 5.e-9
to_plot = False
if to_plot:
    theta = np.linspace(0,2*np.pi,1000)
    xr = np.cos(theta)
    yr = np.sin(theta)
while not time_step(sim, t_end_sim=t_end_sim):
    if to_plot:
        plt.clf()
    ii += 1
    tt = sim.beamtim.tt_curr
    if tt > t_min and tt < t_max:
        if ii%mod_factor == 0.:
            print(jj, ii, -c*(tt-2.5e-9))
            zg.append(-c*(tt-2.5e-9))
            exfm.dict_to_h5({'phi' : sim.spacech_ele.phi, 'rho' : sim.spacech_ele.rho}, out_pinch, group='slices/slice%d'%jj, readwrite_opts='a')
            jj += 1
    # print(ii, sim.cloud_list[0].MP_e.N_mp)
    if to_plot:
        rho = sim.spacech_ele.rho/(-e)
        rho[rho<1e2] = 1.e2
        mpl = plt.pcolormesh(XX, YY, np.log10(rho), shading="nearest", vmin = 14, vmax = 17, cmap=cm.batlow)
        for nsig in [2,4,6]:
            plt.plot(xr*nsig*sigx+xc, yr*nsig*sigy+yc, color="grey", lw=2, alpha=0.5)
            plt.text((nsig+0.2)*sigx+xc, 0, f"{nsig}σ", color="grey", alpha=0.5)
        #mpl = plt.pcolormesh(XX, YY, rho,shading="nearest", vmin = 0, vmax = 2.e16, cmap=cm.batlow)
        #print(f"Max edensity = {np.max(sim.spacech_ele.rho/(-e)/1.e16):.2f}e16 e-/m")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        cb = plt.colorbar(mpl)
        cb.set_label("electron density")
        plt.title(f"t = {(tt-2.5e-9)/1.e-9:.3f} ns, {((tt-2.5e-9)/0.3e-9):.2f}σ")
        plt.tight_layout()
        fig.savefig(f"frames/frame_{ii:d}.png")

grid_dict = {"xg" : np.array(xg),
             "yg" : np.array(yg),
             "zg" : np.array(zg),
             "xc" : xc,
             "yc" : yc,
             "sigx" : sigx,
             "sigy" : sigy,
}
exfm.dict_to_h5(grid_dict, out_pinch, group='grid', readwrite_opts='a')
