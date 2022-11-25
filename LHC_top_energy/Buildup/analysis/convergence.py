import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import json

def get_total_nel(sim):
    sim_folder = "/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/Buildup/simulations/"
    folder = sim_folder + sim
    obj = scipy.io.loadmat(folder + "/Pyecltest.mat")
    t = obj["t"][0]
    nel = obj["Nel_timep"][0]
    el_probes = obj['el_dens_at_probes']
    return t, nel, el_probes

ref_sim = "LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48"
ecloud_type = ref_sim.split("_")[2]
index = ref_sim.split("_")[3]
ecloud_type = ecloud_type.lower()
ir = ecloud_type[-1]

with open("/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/eclouds_LHCIT_v1.json", "r") as fid:
    eclouds_info = json.load(fid)

ecloud_info = eclouds_info[f"ecloud.{ecloud_type}.ir{ir}.{index}"]
t_off = ecloud_info["t_offset_s"]
y_filling = np.array(2*(3*(48*[1]+8*[0])+32*[0]),dtype=int)
t_filling = np.arange(0, len(y_filling))*25.e-9
mask = y_filling > 0


t_ref, nel_ref, el_probes_ref = get_total_nel(ref_sim)
t_n60k, nel_n60k, el_probes_n60k = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt1.0e-11")
t_n60k_Dt20, nel_n60k_Dt20, el_probes_n60k_Dt20 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt2.0e-11")
t_n60k_Dt2p5, nel_n60k_Dt2p5, el_probes_n60k_Dt2p5 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt2.5e-12")
t_n60k_Dt5, nel_n60k_Dt5, el_probes_n60k_Dt5 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt5.0e-12")
t_n60k_Dt5_dhb5, nel_n60k_Dt5_dhb5, el_probes_n60k_Dt5_dhb5 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.5e-3")
t_n60k_Dt5_dhb5_dhcsc1, nel_n60k_Dt5_dhb5_dhcsc1, el_probes_n60k_Dt5_dhb5_dhcsc1 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.1e-3")
t_n60k_Dt5_dhb5_dhcsc3, nel_n60k_Dt5_dhb5_dhcsc3, el_probes_n60k_Dt5_dhb5_dhcsc3 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N60000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.3e-3")
t_n100k_Dt5_dhb5_dhcsc1, nel_n100k_Dt5_dhb5_dhcsc1, el_probes_n100k_Dt5_dhb5_dhcsc1 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.1e-3")
t_n100k_Dt5_dhb5_dhcsc1_dtsc10, nel_n100k_Dt5_dhb5_dhcsc1_dtsc10, el_probes_n100k_Dt5_dhb5_dhcsc1_dtsc10 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.1e-3_Dtsc_1.0e-10")
t_n100k_Dt5_dhb5_dhcsc1_dtsc30, nel_n100k_Dt5_dhb5_dhcsc1_dtsc30, el_probes_n100k_Dt5_dhb5_dhcsc1_dtsc30 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.1e-3_Dtsc_3.0e-10")
t_n100k_Dt5_dhb5_dhcsc1_dtsc5, nel_n100k_Dt5_dhb5_dhcsc1_dtsc5, el_probes_n100k_Dt5_dhb5_dhcsc1_dtsc5 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc0.1e-3_Dtsc_5.0e-11")
t_n100k_Dt5_dhb5_dhcsc2_dtsc50, nel_n100k_Dt5_dhb5_dhcsc2_dtsc50, el_probes_n100k_Dt5_dhb5_dhcsc2_dtsc50 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc2.0e-04_Dtsc_0.5e-9")
t_n100k_Dt5_dhb5_dhcsc05_dtsc50, nel_n100k_Dt5_dhb5_dhcsc05_dtsc50, el_probes_n100k_Dt5_dhb5_dhcsc05_dtsc50 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc5.0e-05_Dtsc_0.5e-9")
t_n100k_Dt5_dhb5_dhcsc01_dtsc50, nel_n100k_Dt5_dhb5_dhcsc01_dtsc50, el_probes_n100k_Dt5_dhb5_dhcsc01_dtsc50 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc1.0e-05_Dtsc_0.5e-9")
t_n100k_Dt5_dhb5_dhcsc03_dtsc50, nel_n100k_Dt5_dhb5_dhcsc03_dtsc50, el_probes_n100k_Dt5_dhb5_dhcsc03_dtsc50 = get_total_nel("LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_3x48_N100000_Dt5.0e-12_Dhb0.5e-4_Dhcsc3.0e-05_Dtsc_0.5e-9")

# beam1 = 
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(t_ref, nel_ref, 'k', label="Dt=1.0e-11, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=35k")
ax1.plot(t_n60k, nel_n60k,"--", label="Dt=1.0e-11, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax1.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax1.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax1.legend()
ax1.set_ylim(-1e9, 7e9)

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(t_n60k_Dt2p5, nel_n60k_Dt2p5, label="Dt= 2.5e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax2.plot(t_n60k_Dt5, nel_n60k_Dt5, label="Dt= 5.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax2.plot(t_n60k, nel_n60k,"k", label="Dt=10.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax2.plot(t_n60k_Dt20, nel_n60k_Dt20, label="Dt=20.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax2.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax2.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax2.legend()
ax2.set_ylim(-1e9, 7e9)

fig3 = plt.figure(3)
ax3 = fig3.add_subplot(111)
ax3.plot(t_n60k_Dt5, nel_n60k_Dt5, label="Dt= 5.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax3.plot(t_n60k_Dt5_dhb5, nel_n60k_Dt5_dhb5, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax3.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax3.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax3.legend()
ax3.set_ylim(-1e9, 7e9)

fig4 = plt.figure(4)
ax4 = fig4.add_subplot(111)
#ax4.plot(t_n60k_Dt5, nel_n60k_Dt5, label="Dt= 5.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax4.plot(t_n60k_Dt5_dhb5_dhcsc1, nel_n60k_Dt5_dhb5_dhcsc1, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.1e-3, Nmax=60k")
ax4.plot(t_n60k_Dt5_dhb5_dhcsc3, nel_n60k_Dt5_dhb5_dhcsc3, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.3e-3, Nmax=60k")
ax4.plot(t_n60k_Dt5_dhb5, nel_n60k_Dt5_dhb5, 'k', label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax4.plot(t_n100k_Dt5_dhb5_dhcsc1, nel_n100k_Dt5_dhb5_dhcsc1, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.1e-3, Nmax=100k")
ax4.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax4.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax4.legend()
ax4.set_ylim(-1e9, 7e9)

fig5 = plt.figure(5)
ax5 = fig5.add_subplot(111)
#ax4.plot(t_n60k_Dt5, nel_n60k_Dt5, label="Dt= 5.0e-12, Dh_b=1.5e-4, Dh_sc=0.5e-3, Nmax=60k")
ax5.plot(t_n100k_Dt5_dhb5_dhcsc1, nel_n100k_Dt5_dhb5_dhcsc1, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.1e-3, Dt_sc =  5e-10, Nmax=100k")
ax5.plot(t_n100k_Dt5_dhb5_dhcsc1_dtsc30, nel_n100k_Dt5_dhb5_dhcsc1_dtsc30, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-3, Dt_sc =  3e-10, Nmax=60k")
ax5.plot(t_n100k_Dt5_dhb5_dhcsc1_dtsc10, nel_n100k_Dt5_dhb5_dhcsc1_dtsc10, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-3, Dt_sc =  1e-10, Nmax=60k")
ax5.plot(t_n100k_Dt5_dhb5_dhcsc1_dtsc5, nel_n100k_Dt5_dhb5_dhcsc1_dtsc5, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-3, Dt_sc =0.5e-10, Nmax=60k")
ax5.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax5.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax5.legend()
ax5.set_ylim(-1e9, 7e9)

t_n100k_Dt5_dhb5_dhcsc05_dtsc50

fig6 = plt.figure(6)
ax6 = fig6.add_subplot(111)
ax6.plot(t_n100k_Dt5_dhb5_dhcsc2_dtsc50, nel_n100k_Dt5_dhb5_dhcsc2_dtsc50, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=2.0e-4, Dt_sc =  5e-10, Nmax=100k")
ax6.plot(t_n100k_Dt5_dhb5_dhcsc1, nel_n100k_Dt5_dhb5_dhcsc1, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=1.0e-4, Dt_sc =  5e-10, Nmax=100k")
ax6.plot(t_n100k_Dt5_dhb5_dhcsc05_dtsc50, nel_n100k_Dt5_dhb5_dhcsc05_dtsc50, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.5e-4, Dt_sc =  5e-10, Nmax=100k")
ax6.plot(t_n100k_Dt5_dhb5_dhcsc03_dtsc50, nel_n100k_Dt5_dhb5_dhcsc03_dtsc50, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.3e-4, Dt_sc =  5e-10, Nmax=100k")
ax6.plot(t_n100k_Dt5_dhb5_dhcsc01_dtsc50, nel_n100k_Dt5_dhb5_dhcsc01_dtsc50, label="Dt= 5.0e-12, Dh_b=0.5e-4, Dh_sc=0.1e-4, Dt_sc =  5e-10, Nmax=100k")
ax6.plot(t_filling[mask], y_filling[mask]*(0.6e9)-0.9e9, 'bo')
ax6.plot(t_filling[mask]+t_off, y_filling[mask]*(0.2e9)-0.9e9, 'ro')
ax6.legend()
ax6.set_ylim(-1e9, 7e9)


plt.show()