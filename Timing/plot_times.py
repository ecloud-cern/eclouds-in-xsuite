import json
import numpy as np
import matplotlib.pyplot as plt


tppt_no_0 = []
tpt_no_6 = []
tppt_all_0 = []
tpt_all_6 = []

num_particles_list = [2000, 4000, 6000, 6912, 6913, 8000, 10000, 12000, 13824, 13825, 14000, 16000, 18000, 20000, 20738, 20739, 22000, 24000, 26000, 27648, 27649, 28000, 30000]

def get_tpt_tppt(num_particles_list, ecloud, optimization):
    tpt = []
    tppt = []
    for num_particles in num_particles_list:
        mydict = json.load(open(f"timing_measurements/a100_injection_time_{optimization}opt_{num_particles}parts_1000turns_{ecloud}ecloud.json","r"))
        tppt.append(mydict["time_per_part_turn"]*1e6)
        tpt.append(mydict["time_per_turn"]*1e3)
    return tppt, tpt


tppt_no_0, tpt_no_0 = get_tpt_tppt(num_particles_list, "no", 0)
tppt_no_6, tpt_no_6 = get_tpt_tppt(num_particles_list, "no", 4)
tppt_all_0, tpt_all_0 = get_tpt_tppt(num_particles_list, "mq", 0)
tppt_all_6, tpt_all_6 = get_tpt_tppt(num_particles_list, "mq", 4)

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(num_particles_list, tppt_no_0, 'b--o')
ax1.plot(num_particles_list, tppt_no_6, 'b-o')
ax1.plot(num_particles_list, tppt_all_0, 'r--o')
ax1.plot(num_particles_list, tppt_all_6, 'r-o')
ax1.set_yscale('log')
ax1.set_xscale('log')
ax1.set_xlabel("Number of particles")
ax1.set_ylabel("Time / turn / particle [us]")

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(num_particles_list, tpt_no_0, 'b--o')
ax2.plot(num_particles_list, tpt_no_6, 'b-o')
ax2.plot(num_particles_list, tpt_all_0, 'r--o')
ax2.plot(num_particles_list, tpt_all_6, 'r-o')
ax2.set_xlabel("Number of particles")
ax2.set_ylabel("Time / turn [ms]")


plt.show()