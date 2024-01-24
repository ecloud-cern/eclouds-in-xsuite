import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import json

folder = "/eos/project/e/ecloud-simulations/kparasch/LHC_Triplets/Buildup/run3_bet30cm_160urad_1.2e11ppb_2.0um/simulations_SEY1.35/" \
       + "LHC6.8TeV_v1_DR23R5_5_sey1.35_1.20e11ppb/"
# folder = "/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/Buildup/simulations/LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48/"

sim = folder.split("/")[-2]
ecloud_type = sim.split("_")[2]
index = sim.split("_")[3]
ecloud_type = ecloud_type.lower()
ir = ecloud_type[-1]

with open("/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/eclouds_LHCIT_v1.json", "r") as fid:
    eclouds_info = json.load(fid)

ecloud_info = eclouds_info[f"ecloud.{ecloud_type}.ir{ir}.{index}"]
t_off = ecloud_info["t_offset_s"]
y_filling = np.array(2*(3*(48*[1]+8*[0])+32*[0]),dtype=int)
t_filling = np.arange(0, len(y_filling))*25.e-9
mask = y_filling > 0
obj = scipy.io.loadmat(folder + "Pyecltest.mat")
t = obj["t"][0]
nel = obj["Nel_timep"][0]
el_probes = obj['el_dens_at_probes']
# beam1 = 
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(t, nel, 'k')
ax1.plot(t_filling[mask], y_filling[mask]*(5.1e9), 'bo')
ax1.plot(t_filling[mask]+t_off, y_filling[mask]*(5.1e9)-0.2e9, 'ro')

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(t[:-1], el_probes[0], 'b')
ax2.plot(t[:-1], el_probes[1], 'r')
ax2.plot(t_filling[mask], y_filling[mask]*(2.1e13), 'bo')
ax2.plot(t_filling[mask]+t_off, y_filling[mask]*(2.1e13)-0.2e13, 'ro')



plt.show()