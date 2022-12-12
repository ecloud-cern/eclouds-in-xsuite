import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.constants import c

import scipy.io as sio
from cmcrameri import cm

mqxa_1_offset = 26.15
mqxb_a2_offset = 34.8
mqxb_b2_offset = 41.3
mqxa_3_offset = 50.15

mqxa_L = 6.37
mqxb_L = 5.5

ip5_s = 6664.5684327563

eclouds = json.load(open("../../eclouds_LHCIT_v1.json","r"))
heatloads_135 = json.load(open(f"LHCIT_heatloads_SEY1.35_1.20e11ppb.json","r"))
heatloads_130 = json.load(open(f"LHCIT_heatloads_SEY1.30_1.20e11ppb.json","r"))
heatloads_125 = json.load(open(f"LHCIT_heatloads_SEY1.25_1.20e11ppb.json","r"))
heatloads_120 = json.load(open(f"LHCIT_heatloads_SEY1.20_1.20e11ppb.json","r"))
heatloads_115 = json.load(open(f"LHCIT_heatloads_SEY1.15_1.20e11ppb.json","r"))
heatloads_110 = json.load(open(f"LHCIT_heatloads_SEY1.10_1.20e11ppb.json","r"))
heatloads_105 = json.load(open(f"LHCIT_heatloads_SEY1.05_1.20e11ppb.json","r"))

heatload_135 = []
heatload_130 = []
heatload_125 = []
heatload_120 = []
heatload_115 = []
heatload_110 = []
heatload_105 = []
s = []
for key in eclouds.keys():
    if "r5." in key:
        s.append(eclouds[key]["s"])
        heatload_135.append(heatloads_135[key])
        heatload_130.append(heatloads_130[key])
        heatload_125.append(heatloads_125[key])
        heatload_120.append(heatloads_120[key])
        heatload_115.append(heatloads_115[key])
        heatload_110.append(heatloads_110[key])
        heatload_105.append(heatloads_105[key])

aso = np.argsort(s)

s = np.array(s)[aso]
heatload_135 = np.array(heatload_135)[aso]
heatload_130 = np.array(heatload_130)[aso]
heatload_125 = np.array(heatload_125)[aso]
heatload_120 = np.array(heatload_120)[aso]
heatload_115 = np.array(heatload_115)[aso]
heatload_110 = np.array(heatload_110)[aso]
heatload_105 = np.array(heatload_105)[aso]

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot(s - ip5_s, heatload_135, "o", label="SEY=1.35")
ax.plot(s - ip5_s, heatload_130, "o", label="SEY=1.30")
ax.plot(s - ip5_s, heatload_125, "o", label="SEY=1.25")

ax.set_xlabel("s [m]")
ax.set_ylabel("Number of electrons [e$^{-}$/m]")

ax.fill_between([ mqxa_1_offset - mqxa_L/2., mqxa_1_offset + mqxa_L/2.], [0.8e10,0.8e10], [1e10,1e10], color="k", alpha=0.5)
ax.fill_between([ mqxb_a2_offset - mqxb_L/2., mqxb_a2_offset + mqxb_L/2.], [0.8e10,0.8e10], [1e10,1e10], color="k", alpha=0.5)
ax.fill_between([ mqxb_b2_offset - mqxb_L/2., mqxb_b2_offset + mqxb_L/2.], [0.8e10,0.8e10], [1e10,1e10], color="k", alpha=0.5)
ax.fill_between([ mqxa_3_offset - mqxa_L/2., mqxa_3_offset + mqxa_L/2.], [0.8e10,0.8e10], [1e10,1e10], color="k", alpha=0.5)
ax.set_xlim(20,55)
ax.set_ylim(0,1.e10)

for ii in range(20):
    ax.axvline(0.5*ii*25e-9*c,ls="--", c='r')

ax.legend(loc="upper left")

sey_list = np.array([1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35])
s_list = s - ip5_s
XX, YY = np.meshgrid(s_list, sey_list, indexing="ij")

HL2D = np.zeros([len(heatload_125), len(sey_list)])
HL2D[:,0] = heatload_105
HL2D[:,1] = heatload_110
HL2D[:,2] = heatload_115
HL2D[:,3] = heatload_120
HL2D[:,4] = heatload_125
HL2D[:,5] = heatload_130
HL2D[:,6] = heatload_135

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
mpl = ax2.pcolormesh(XX, YY, HL2D/1.e10, shading="nearest", vmin=0, vmax=1, cmap=cm.bilbao)
cb = plt.colorbar(mpl)
cb.set_label("Number of electrons [$10^{10}$ e$^{-}$/m]")

ax2.set_xlabel("s [m]")
ax2.set_ylabel("Secondary emission yield")

ax2.fill_between([ mqxa_1_offset - mqxa_L/2., mqxa_1_offset + mqxa_L/2.],   [1.55, 1.55], [1.70], color="k", alpha=0.5)
ax2.fill_between([ mqxb_a2_offset - mqxb_L/2., mqxb_a2_offset + mqxb_L/2.], [1.55, 1.55], [1.70], color="k", alpha=0.5)
ax2.fill_between([ mqxb_b2_offset - mqxb_L/2., mqxb_b2_offset + mqxb_L/2.], [1.55, 1.55], [1.70], color="k", alpha=0.5)
ax2.fill_between([ mqxa_3_offset - mqxa_L/2., mqxa_3_offset + mqxa_L/2.],   [1.55, 1.55], [1.70], color="k", alpha=0.5)
ax2.set_xlim(20,55)
ax2.set_ylim(1.00, 1.70)




plt.show()


