import numpy as np
import scipy.io
import pickle
from scipy.constants import c
import json

import LHC_IT

def prep_slices(beams=None, ecloud_type="Q1L5"):
    assert beams is not None

    n_slices = LHC_IT.slicing[ecloud_type]
    beamscreen = LHC_IT.beamscreen[ecloud_type]
    s_start = LHC_IT.start_s[ecloud_type]
    s_end = LHC_IT.end_s[ecloud_type]
    s_edges = np.linspace(s_start, s_end, n_slices + 1)

    s_positions = (s_edges[1:] + s_edges[:-1])/2.


    # reverse to have index 0 closest to IP
    if "L" in ecloud_type:
        s_positions = s_positions[::-1]    
    IP = ecloud_type[-1]

    eclouds = {}
    for ii, s in enumerate(s_positions):
        name = f"ecloud.{ecloud_type.lower()}.ir{IP}.{ii}"
        eclouds[name] = {
                         "length" : LHC_IT.length[ecloud_type]/n_slices,
                         "s" : s,
                         "x_b1" : float(beams["x_b1"](s)),
                         "y_b1" : float(beams["y_b1"](s)),
                         "sigx_b1" : float(beams["sigx_b1"](s)),
                         "sigy_b1" : float(beams["sigy_b1"](s)),
                         "betx_b1" : float(beams["betx_b1"](s)),
                         "bety_b1" : float(beams["bety_b1"](s)),
                         "x_b2" : float(beams["x_b2"](s)),
                         "y_b2" : float(beams["y_b2"](s)),
                         "sigx_b2" : float(beams["sigx_b2"](s)),
                         "sigy_b2" : float(beams["sigy_b2"](s)),
                         "betx_b2" : float(beams["betx_b2"](s)),
                         "bety_b2" : float(beams["bety_b2"](s)),
                         "Bgrad" : float(beams["Bgrad_cl"].get_Bgrad(s)),
                         "t_offset_s" : - 2 * (s - LHC_IT.IP_s[IP]) / c,
                         "beamscreen" : beamscreen
                        }
    return eclouds

beams = pickle.load(open("beam_params.pkl","rb"))

eclouds_info = {}
ecloud_types = list(LHC_IT.length.keys())
for ecloud_type in ecloud_types:
    eclouds_info.update(prep_slices(ecloud_type=ecloud_type, beams=beams))

with open(f"eclouds_LHCIT_v1.json","w") as outfile:
    json.dump(eclouds_info, outfile, indent=4)


names = ["LHC_BS010.mat", "LHC_BS012.mat", "LHC_BS003.mat", "LHC_BS005.mat"]
halfwidths = [0.0192, 0.0241, 0.0241, 0.029]
halfheights = [0.0241, 0.029, 0.0192, 0.0241]
radii = [0.0241, 0.029, 0.0241, 0.029]

for fname, halfwidth, halfheight, radius in zip(names, halfwidths, halfheights, radii):
    bs_coords = LHC_IT.get_rectcircle(halfwidth=halfwidth, halfheight=halfheight, radius=radius)
    bs_dict = {"Vx": bs_coords[:,0], "Vy" : bs_coords[:,1], 
              "x_sem_ellip_insc": halfwidth, "y_sem_ellip_insc" : halfheight}
    scipy.io.savemat("Beam_chambers/" + fname, bs_dict, oned_as="row")