import numpy as np
from scipy.constants import c
import shapely.geometry as sg
import shapely.ops as so

__version__ = "1.0"

Q1_slices = 64
Q2A_slices = 64
Q2B_slices = 64
Q3_slices = 64
DR12_slices = 32
DR2_slices = 16
DR23_slices = 32
DR3_slices = 16
DFBX_slices = 32

mqxa_1_offset = 26.15
mqxb_a2_offset = 34.8
mqxb_b2_offset = 41.3
mqxa_3_offset = 50.15
dfbx_offset = 56.427

mqxa_L = 6.37
mqxb_L = 5.5
dfbx_L = 3.09

Q1_length = mqxa_L
Q2A_length = mqxb_L
Q2B_length = mqxb_L
Q3_length = mqxa_L
DR12_length = 2.715
DR2_length = 1.
DR23_length = 2.915
DR3_length = 1.547
DFBX_length = dfbx_L

ip1_s = 19994.1624
ip5_s = 6664.5684327563
IP_s = {"1": ip1_s, "5" : ip5_s}

length = {
           "Q1L5": Q1_length,
           "Q1R5": Q1_length,
           "Q1L1": Q1_length,
           "Q1R1": Q1_length,
           "Q2AL5" : Q2A_length,
           "Q2AR5" : Q2A_length,
           "Q2AL1" : Q2A_length,
           "Q2AR1" : Q2A_length,
           "Q2BL5" : Q2B_length,
           "Q2BR5" : Q2B_length,
           "Q2BL1" : Q2B_length,
           "Q2BR1" : Q2B_length,
           "Q3L5" : Q3_length,
           "Q3R5" : Q3_length,
           "Q3L1" : Q3_length,
           "Q3R1" : Q3_length,
           "DR12L5" : DR12_length,
           "DR12R5" : DR12_length,
           "DR12L1" : DR12_length,
           "DR12R1" : DR12_length,
           "DR2L5" : DR2_length,
           "DR2R5" : DR2_length,
           "DR2L1" : DR2_length,
           "DR2R1" : DR2_length,
           "DR23L5" : DR23_length,
           "DR23R5" : DR23_length,
           "DR23L1" : DR23_length,
           "DR23R1" : DR23_length,
           "DR3L5" : DR3_length,
           "DR3R5" : DR3_length,
           "DR3L1" : DR3_length,
           "DR3R1" : DR3_length,
           "DFBXL5" : DFBX_length,
           "DFBXR5" : DFBX_length,
           "DFBXL1" : DFBX_length,
           "DFBXR1" : DFBX_length,
          }
start_s = {
           "Q1L5": ip5_s - 29.335,
           "DR12L5" : ip5_s - 32.05,
           "Q2AL5" : ip5_s - 37.55,
           "DR2L5" : ip5_s - 38.55,
           "Q2BL5" : ip5_s - 44.05,
           "DR23L5" : ip5_s - 46.965,
           "Q3L5" : ip5_s - 53.335,
           "DR3L5" : ip5_s - 54.882,
           "DFBXL5" : ip5_s - 57.972,
           ######################
           "Q1R5": ip5_s + 22.965,
           "DR12R5" : ip5_s + 29.335,
           "Q2AR5" : ip5_s + 32.05,
           "DR2R5" : ip5_s + 37.55,
           "Q2BR5" : ip5_s + 38.55,
           "DR23R5" : ip5_s + 44.05,
           "Q3R5" : ip5_s + 46.965,
           "DR3R5" : ip5_s + 53.335,
           "DFBXR5" : ip5_s + 54.882,
           ######################
           "Q1L1": ip1_s - 29.335,
           "DR12L1" : ip1_s - 32.05,
           "Q2AL1" : ip1_s - 37.55,
           "DR2L1" : ip1_s - 38.55,
           "Q2BL1" : ip1_s - 44.05,
           "DR23L1" : ip1_s - 46.965,
           "Q3L1" : ip1_s - 53.335,
           "DR3L1" : ip1_s - 54.882,
           "DFBXL1" : ip1_s - 57.972,
           ######################
           "Q1R1": ip1_s + 22.965,
           "DR12R1" : ip1_s + 29.335,
           "Q2AR1" : ip1_s + 32.05,
           "DR2R1" : ip1_s + 37.55,
           "Q2BR1" : ip1_s + 38.55,
           "DR23R1" : ip1_s + 44.05,
           "Q3R1" : ip1_s + 46.965,
           "DR3R1" : ip1_s + 53.335,
           "DFBXR1" : ip1_s + 54.882,
}
end_s = {
           "Q1L5": ip5_s - 22.965,
           "DR12L5" : ip5_s - 29.335,
           "Q2AL5" : ip5_s - 32.05,
           "DR2L5" : ip5_s - 37.55,
           "Q2BL5" : ip5_s - 38.55,
           "DR23L5" : ip5_s - 44.05,
           "Q3L5" : ip5_s - 46.965,
           "DR3L5" : ip5_s - 53.335,
           "DFBXL5" : ip5_s - 54.882,
           ######################
           "Q1R5": ip5_s + 29.335,
           "DR12R5" : ip5_s + 32.05,
           "Q2AR5" : ip5_s + 37.55,
           "DR2R5" : ip5_s + 38.55,
           "Q2BR5" : ip5_s + 44.05,
           "DR23R5" : ip5_s + 46.965,
           "Q3R5" : ip5_s + 53.335,
           "DR3R5" : ip5_s + 54.882,
           "DFBXR5" : ip5_s + 57.972,
           ######################
           "Q1L1": ip1_s - 22.965,
           "DR12L1" : ip1_s - 29.335,
           "Q2AL1" : ip1_s - 32.05,
           "DR2L1" : ip1_s - 37.55,
           "Q2BL1" : ip1_s - 38.55,
           "DR23L1" : ip1_s - 44.05,
           "Q3L1" : ip1_s - 46.965,
           "DR3L1" : ip1_s - 53.335,
           "DFBXL1" : ip1_s - 54.882,
           ######################
           "Q1R1": ip1_s + 29.335,
           "DR12R1" : ip1_s + 32.05,
           "Q2AR1" : ip1_s + 37.55,
           "DR2R1" : ip1_s + 38.55,
           "Q2BR1" : ip1_s + 44.05,
           "DR23R1" : ip1_s + 46.965,
           "Q3R1" : ip1_s + 53.335,
           "DR3R1" : ip1_s + 54.882,
           "DFBXR1" : ip1_s + 57.972,
}
slicing = {
           "Q1L5": Q1_slices,
           "Q1R5": Q1_slices,
           "Q1L1": Q1_slices,
           "Q1R1": Q1_slices,
           "Q2AL5" : Q2A_slices,
           "Q2AR5" : Q2A_slices,
           "Q2AL1" : Q2A_slices,
           "Q2AR1" : Q2A_slices,
           "Q2BL5" : Q2B_slices,
           "Q2BR5" : Q2B_slices,
           "Q2BL1" : Q2B_slices,
           "Q2BR1" : Q2B_slices,
           "Q3L5" : Q3_slices,
           "Q3R5" : Q3_slices,
           "Q3L1" : Q3_slices,
           "Q3R1" : Q3_slices,
           "DR12L5" : DR12_slices,
           "DR12R5" : DR12_slices,
           "DR12L1" : DR12_slices,
           "DR12R1" : DR12_slices,
           "DR2L5" : DR2_slices,
           "DR2R5" : DR2_slices,
           "DR2L1" : DR2_slices,
           "DR2R1" : DR2_slices,
           "DR23L5" : DR23_slices,
           "DR23R5" : DR23_slices,
           "DR23L1" : DR23_slices,
           "DR23R1" : DR23_slices,
           "DR3L5" : DR3_slices,
           "DR3R5" : DR3_slices,
           "DR3L1" : DR3_slices,
           "DR3R1" : DR3_slices,
           "DFBXL5" : DFBX_slices,
           "DFBXR5" : DFBX_slices,
           "DFBXL1" : DFBX_slices,
           "DFBXR1" : DFBX_slices,
          }

beamscreen = {
           "Q1L5": "bs010",
           "Q1R5": "bs010",
           "Q1L1": "bs003",
           "Q1R1": "bs003",
           "Q2AL5" : "bs012",
           "Q2AR5" : "bs012",
           "Q2AL1" : "bs005",
           "Q2AR1" : "bs005",
           "Q2BL5" : "bs012",
           "Q2BR5" : "bs012",
           "Q2BL1" : "bs005",
           "Q2BR1" : "bs005",
           "Q3L5" : "bs012",
           "Q3R5" : "bs012",
           "Q3L1" : "bs005",
           "Q3R1" : "bs005",
           "DR12L5" : "bs010",
           "DR12R5" : "bs010",
           "DR12L1" : "bs003",
           "DR12R1" : "bs003",
           "DR2L5" : "bs012",
           "DR2R5" : "bs012",
           "DR2L1" : "bs005",
           "DR2R1" : "bs005",
           "DR23L5" : "bs012",
           "DR23R5" : "bs012",
           "DR23L1" : "bs005",
           "DR23R1" : "bs005",
           "DR3L5" : "bs012",
           "DR3R5" : "bs012",
           "DR3L1" : "bs005",
           "DR3R1" : "bs005",
           "DFBXL5" : "bs014",
           "DFBXR5" : "bs014",
           "DFBXL1" : "bs007",
           "DFBXR1" : "bs007",
          }


class Bgrad_class:
    def __init__(self, line):

        p0 = line.particle_ref.p0c / c
        mqx_names = ["mqxa.1r5..1", "mqxb.a2r5..1", "mqxb.b2r5..1", "mqxa.3r5..1",
                     "mqxa.1l5..1", "mqxb.a2l5..1", "mqxb.b2l5..1", "mqxa.3l5..1",
                     "mqxa.1r1..1", "mqxb.a2r1..1", "mqxb.b2r1..1", "mqxa.3r1..1",
                     "mqxa.1l1..1", "mqxb.a2l1..1", "mqxb.b2l1..1", "mqxa.3l1..1"]

        self.mqx_Bgrad = {}
        for name, el in zip(line.element_names, line.elements):
            if name in mqx_names:
                mqx = el.to_dict()
                k1 = mqx["knl"][1]/mqx["length"]
                Bgrad = k1 * p0
                key = name.split('..')[0]
                self.mqx_Bgrad[key] = float(Bgrad)
        print(self.mqx_Bgrad)
        
    def get_Bgrad(self, s):

        mqxa_1_offset_start = mqxa_1_offset - mqxa_L/2.
        mqxa_1_offset_end = mqxa_1_offset + mqxa_L/2.
        mqxb_a2_offset_start = mqxb_a2_offset - mqxb_L/2.
        mqxb_a2_offset_end = mqxb_a2_offset + mqxb_L/2.
        mqxb_b2_offset_start = mqxb_b2_offset - mqxb_L/2.
        mqxb_b2_offset_end = mqxb_b2_offset + mqxb_L/2.
        mqxa_3_offset_start = mqxa_3_offset - mqxa_L/2.
        mqxa_3_offset_end = mqxa_3_offset + mqxa_L/2.

        if ip1_s - mqxa_3_offset_end < s and s < ip1_s - mqxa_3_offset_start:
            mqx = "mqxa.3l1"
        elif ip1_s - mqxb_b2_offset_end < s and s < ip1_s - mqxb_b2_offset_start:
            mqx = "mqxb.b2l1"
        elif ip1_s - mqxb_a2_offset_end < s and s < ip1_s - mqxb_a2_offset_start:
            mqx = "mqxb.a2l1"
        elif ip1_s - mqxa_1_offset_end < s and s < ip1_s - mqxa_1_offset_start:
            mqx = "mqxa.1l1"
        elif ip1_s + mqxa_1_offset_start < s and s < ip1_s + mqxa_1_offset_end:
            mqx = "mqxa.1r1"
        elif ip1_s + mqxb_a2_offset_start < s and s < ip1_s + mqxb_a2_offset_end:
            mqx = "mqxb.a2r1"
        elif ip1_s + mqxb_b2_offset_start < s and s < ip1_s + mqxb_b2_offset_end:
            mqx = "mqxb.b2r1"
        elif ip1_s + mqxa_3_offset_start < s and s < ip1_s + mqxa_3_offset_end:
            mqx = "mqxa.3r1"
        elif ip5_s - mqxa_3_offset_end < s and s < ip5_s - mqxa_3_offset_start:
            mqx = "mqxa.3l5"
        elif ip5_s - mqxb_b2_offset_end < s and s < ip5_s - mqxb_b2_offset_start:
            mqx = "mqxb.b2l5"
        elif ip5_s - mqxb_a2_offset_end < s and s < ip5_s - mqxb_a2_offset_start:
            mqx = "mqxb.a2l5"
        elif ip5_s - mqxa_1_offset_end < s and s < ip5_s - mqxa_1_offset_start:
            mqx = "mqxa.1l5"
        elif ip5_s + mqxa_1_offset_start < s and s < ip5_s + mqxa_1_offset_end:
            mqx = "mqxa.1r5"
        elif ip5_s + mqxb_a2_offset_start < s and s < ip5_s + mqxb_a2_offset_end:
            mqx = "mqxb.a2r5"
        elif ip5_s + mqxb_b2_offset_start < s and s < ip5_s + mqxb_b2_offset_end:
            mqx = "mqxb.b2r5"
        elif ip5_s + mqxa_3_offset_start < s and s < ip5_s + mqxa_3_offset_end:
            mqx = "mqxa.3r5"
        else:
            return 0
        return self.mqx_Bgrad[mqx]



def get_rectcircle(halfwidth, halfheight, radius):
    
    p1 = sg.Point(0,0).buffer(radius)
    aperture = so.clip_by_rect(p1, -halfwidth, -halfheight, halfwidth, halfheight)
    coords = np.array(list(aperture.exterior.coords))
    return coords[::-1][:-1]

mqxa_1_offset = 26.15
mqxb_a2_offset = 34.8
mqxb_b2_offset = 41.3
mqxa_3_offset = 50.15

def plot_triplets(ax=None):
    ax.fill_between([ip5_s - dfbx_offset - dfbx_L/2., ip5_s - dfbx_offset + dfbx_L/2.], [-500,-500], [9000,9000], color="g", alpha=0.5)
    ax.fill_between([ip5_s - mqxa_3_offset - mqxa_L/2., ip5_s - mqxa_3_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s - mqxb_b2_offset - mqxb_L/2., ip5_s - mqxb_b2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s - mqxb_a2_offset - mqxb_L/2., ip5_s - mqxb_a2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s - mqxa_1_offset - mqxa_L/2., ip5_s - mqxa_1_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s + mqxa_1_offset - mqxa_L/2., ip5_s + mqxa_1_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s + mqxb_a2_offset - mqxb_L/2., ip5_s + mqxb_a2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s + mqxb_b2_offset - mqxb_L/2., ip5_s + mqxb_b2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s + mqxa_3_offset - mqxa_L/2., ip5_s + mqxa_3_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip5_s + dfbx_offset - dfbx_L/2., ip5_s + dfbx_offset + dfbx_L/2.], [-500,-500], [9000,9000], color="g", alpha=0.5)
    ax.fill_between([ip1_s - dfbx_offset - dfbx_L/2., ip1_s - dfbx_offset + dfbx_L/2.], [-500,-500], [9000,9000], color="g", alpha=0.5)
    ax.fill_between([ip1_s - mqxa_3_offset - mqxa_L/2., ip1_s - mqxa_3_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s - mqxb_b2_offset - mqxb_L/2., ip1_s - mqxb_b2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s - mqxb_a2_offset - mqxb_L/2., ip1_s - mqxb_a2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s - mqxa_1_offset - mqxa_L/2., ip1_s - mqxa_1_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s + mqxa_1_offset - mqxa_L/2., ip1_s + mqxa_1_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s + mqxb_a2_offset - mqxb_L/2., ip1_s + mqxb_a2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s + mqxb_b2_offset - mqxb_L/2., ip1_s + mqxb_b2_offset + mqxb_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s + mqxa_3_offset - mqxa_L/2., ip1_s + mqxa_3_offset + mqxa_L/2.], [-500,-500], [9000,9000], color="b", alpha=0.5)
    ax.fill_between([ip1_s + dfbx_offset - dfbx_L/2., ip1_s + dfbx_offset + dfbx_L/2.], [-500,-500], [9000,9000], color="g", alpha=0.5)