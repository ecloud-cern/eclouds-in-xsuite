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
sey_list = np.array([1.05,1.10, 1.15, 1.20, 1.25, 1.30, 1.35])[::-1]
heatload_dict = {sey: json.load(open(f"LHCIT_heatloads_SEY{sey:.2f}_1.20e11ppb.json","r")) for sey in sey_list}

heatloads = {sey : [] for sey in heatload_dict.keys()}

s = []
for key in eclouds.keys():
    if "r5." in key and "l5." not in key:
        s.append(eclouds[key]["s"])
        for sey in heatload_dict.keys():
            heatloads[sey].append(heatload_dict[sey][key])

aso = np.argsort(s)

s = np.array(s)[aso]
for sey in heatload_dict.keys():
    heatloads[sey] = np.array(heatloads[sey])[aso]

fig = plt.figure(1,figsize=[12,5])
ax = fig.add_subplot(111)
for sey in heatload_dict.keys():
    ax.plot(s - ip5_s, heatloads[sey], ".-", label=f"SEY={sey:.2f}")

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

ax.legend(bbox_to_anchor=(1.1, 1.05),  loc='upper left', prop={'size':14})
fig.tight_layout()


s_list = s - ip5_s
XX, YY = np.meshgrid(s_list, sey_list, indexing="ij")

HL2D = np.zeros([len(s), len(sey_list)])
for ii, sey in enumerate(heatload_dict.keys()):
    HL2D[:, ii] = heatloads[sey]

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


