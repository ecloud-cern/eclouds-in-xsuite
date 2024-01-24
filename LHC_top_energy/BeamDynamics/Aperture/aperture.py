import xtrack as xt
import xobjects as xo
import xpart as xp
import xfields as xf

import collimators

import pickle
import json

import numpy as np
import time

import argparse

start_running = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--filename', nargs='?', default='delete.h5', type=str)
parser.add_argument('--num_turns', nargs='?', default=100, type=int)
parser.add_argument('--num_particles', nargs='?', default=2764*1, type=int)
parser.add_argument('--sigma', nargs='?', default=7, type=float)
parser.add_argument('--zeta', nargs='?', default=0, type=float)
parser.add_argument('--pzeta', nargs='?', default=2.7e-4, type=float)
parser.add_argument('--beam', nargs='?', default=1, type=int)
parser.add_argument('--ecloud_type', nargs='?', default="q1r5", type=str)
args = parser.parse_args()

output_filename = args.filename
num_turns = args.num_turns
num_particles = args.num_particles
n_sigma = args.sigma
zeta = args.zeta
pzeta = args.pzeta
ecloud_type = args.ecloud_type
num_stores = 100
n_iter = 30
output_filename = f"DA_Beam{args.beam:d}_pzeta{pzeta:.2e}.h5"

Line_folder = "../../Lines/run3_collisions_30cm_160urad_1.2e11_2.0um_62.310_60.320_15_430_0.001/"
with open(Line_folder + f"line_b{args.beam:d}_tracking.json", "r") as fid:
    input_data = json.load(fid)
line = xt.Line.from_dict(input_data)
line.particle_ref = xp.Particles(p0c=input_data['particle_on_tracker_co']["p0c"])

with open("../../eclouds_LHCIT_v1.json", "r") as fid:
    eclouds = json.load(fid)

context = xo.ContextCpu()
collimators.collimator_setup(line, context, number_of_sigmas=5., reference_norm_emit=3.5e-6, verbose=False)

these_eclouds = [key for key in eclouds.keys() if ecloud_type in key]
neclouds = len(these_eclouds)
for ii, name in enumerate(these_eclouds):
    if ecloud_type not in name:
        continue
    s = eclouds[name]["s"]
    length = 0.
    line.insert_element(
        element=xt.Drift(length=length),
        name=name,
        at_s=s)
print("e-cloud markers installed.")


mymonitors = {}
for ii, name in enumerate(these_eclouds):
    ecloud = eclouds[name]
    monitor = xt.ParticlesMonitor(_context=context,
                                  start_at_turn=num_turns - num_stores,
                                  stop_at_turn=num_turns,
                                  num_particles=num_particles)
    mymonitors[name] = monitor 
    line.insert_element(index=name, element=monitor, name='monitor_'+name)

tracker = xt.Tracker(_context=context, line=line)
##tracker.optimize_for_tracking()

pzeta=2.7e-4
pzeta_list = list(np.linspace(0., 3.e-4, 20))
yxmin = {}
yxmax = {}
yymin = {}
yymax = {}
for key in mymonitors:
    yxmin[key] = [0 for pzeta in pzeta_list]
    yxmax[key] = [0 for pzeta in pzeta_list]
    yymin[key] = [0 for pzeta in pzeta_list]
    yymax[key] = [0 for pzeta in pzeta_list]

for ii, pzeta in enumerate(pzeta_list):
    print(f"pzeta = {pzeta:.2e}")
    for _ in range(n_iter):
        zeta=0
        x_norm  = np.random.random(num_particles)*2*n_sigma - n_sigma
        px_norm = np.random.random(num_particles)*2*n_sigma - n_sigma
        y_norm  = np.random.random(num_particles)*2*n_sigma - n_sigma
        py_norm = np.random.random(num_particles)*2*n_sigma - n_sigma
    
        particles = xp.build_particles(_context=context, tracker=tracker, 
            x_norm=x_norm, y_norm=y_norm, 
            px_norm = px_norm, py_norm = py_norm,
            nemitt_x=2e-6, nemitt_y=2e-6, 
            zeta=zeta, delta=pzeta)
    
        print("Tracking...")
        start_tracking = time.time()
        tracker.track(particles, num_turns=num_turns)
        context.synchronize()
        end_tracking = time.time()
        print(f'Tracking time:{(end_tracking-start_tracking)/60.:.4f}mins')
    

        for key in mymonitors:
            ee = eclouds[key]
            monitor = mymonitors[key]
            state = monitor.state > 0
            if np.sum(monitor.state) == 0:
                print("all lost")
                continue 
            sigrat = (3.5/2.0)**0.5
            xmax = (np.max(monitor.x[state]) - ee["x_b1"])/ee["sigx_b1"]/sigrat
            xmin = (np.min(monitor.x[state]) - ee["x_b1"])/ee["sigx_b1"]/sigrat
            ymax = (np.max(monitor.y[state]) - ee["y_b1"])/ee["sigy_b1"]/sigrat
            ymin = (np.min(monitor.y[state]) - ee["y_b1"])/ee["sigy_b1"]/sigrat
            for tt, nn in monitor.data._structure['per_particle_vars']:
                with monitor.data._bypass_linked_vars():
                    getattr(monitor.data, nn)[:] = 0
            # monitor.state = 0
            #print(f"{key} : x: ({xmin:.2f}, {xmax:.2f}) y: ({ymin:.2f}, {ymax:.2f})")

            yxmin[key][ii] = min(yxmin[key][ii], xmin)
            yxmax[key][ii] = max(yxmax[key][ii], xmax)
            yymin[key][ii] = min(yymin[key][ii], ymin)
            yymax[key][ii] = max(yymax[key][ii], ymax)
        print(f"xmax: {xmax:.2f}, ymax: {ymax:.2f}")

save_dict = {"pzeta" : pzeta_list, 
             "xmin" : yxmin, "xmax" : yxmax,
             "ymin" : yymin, "ymax" : yymax,
             }
#pickle.dump(save_dict, open(f"aperture_{ecloud_type}.pkl", "wb"))
with open(f"aperture_{ecloud_type}.json","w") as outfile:
    json.dump(eclouds_info, outfile, indent=4)
end_running = time.time()
