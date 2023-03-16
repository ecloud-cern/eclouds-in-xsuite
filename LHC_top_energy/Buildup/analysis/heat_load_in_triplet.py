import matplotlib.pyplot as plt
import numpy as np
import json

import scipy.io as sio

def get_nel(sey=1.35, ppb=1.20, ecloud_type="Q1R5", ecloud_index=0):
    root_folder = "/eos/project/e/ecloud-simulations/kparasch/LHC_Triplets/Buildup/run3_bet30cm_160urad_1.2e11ppb_2.0um/"
    folder = root_folder + f"simulations_SEY{sey:.2f}/LHC6.8TeV_v1_{ecloud_type}_{ecloud_index}_sey{sey:.2f}_{ppb:.2f}e11ppb/" 
    ob = sio.loadmat(folder + "Pyecltest.mat")
    i0 = np.argmin(np.abs(ob['t'][0] - 326*25e-9))
    i1 = np.argmin(np.abs(ob['t'][0] - 327*25e-9))
    nel = np.max(ob['Nel_timep'][0][i0:i1])
    return nel


# for ii in range(64):
#     print(get_nel(ecloud_type="Q1R5", ecloud_index=ii))

eclouds = json.load(open("../../eclouds_LHCIT_v1.json","r"))

sey=1.05
heatloads = {}
for key in eclouds.keys():
    _, ecloud_type, sector, index = key.upper().split('.')
    hl = get_nel(sey=sey, ecloud_type=ecloud_type, ecloud_index=index)
    heatloads[key] = hl
    if "r5" in key:
        print(key, hl)

with open(f"LHCIT_heatloads_SEY{sey:.2f}_1.20e11ppb.json","w") as outfile:
    json.dump(heatloads, outfile, indent=4)


