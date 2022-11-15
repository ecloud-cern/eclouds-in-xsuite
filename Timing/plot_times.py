import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


tppt_no_0 = []
tpt_no_6 = []
tppt_all_0 = []
tpt_all_6 = []

num_particles_list = [2000, 4000, 6000, 6912, 6913, 8000, 10000, 12000, 13824, 13825, 14000, 16000, 18000, 20000, 20738, 20739, 22000, 24000, 26000, 27648, 27649, 28000, 30000]
num_particles_list_v100 = [2000, 4000, 5120, 5121, 6000, 6912, 6913, 8000, 10000, 10240, 10241, 12000, 13824, 13825, 14000, 15360, 15361, 16000, 18000, 20000, 20480, 20481, 20738, 20739, 22000, 24000, 26000, 27648, 27649, 28000, 30000]

def get_tpt_tppt(num_particles_list, ecloud, optimization, gpu="a100"):
    tpt = []
    tppt = []
    for num_particles in num_particles_list:
        mydict = json.load(open(f"timing_measurements/{gpu}_injection_time_{optimization}opt_{num_particles}parts_1000turns_{ecloud}ecloud.json","r"))
        tppt.append(mydict["time_per_part_turn"]*1e6)
        tpt.append(mydict["time_per_turn"]*1e3)
    return tppt, tpt


ecloud_type = "all"
tppt_no_0, tpt_no_0 = get_tpt_tppt(num_particles_list, "no", 0)
tppt_no_6, tpt_no_6 = get_tpt_tppt(num_particles_list, "no", 6)
tppt_all_0, tpt_all_0 = get_tpt_tppt(num_particles_list, ecloud_type, 0)
tppt_all_6, tpt_all_6 = get_tpt_tppt(num_particles_list, ecloud_type, 6)

tppt_no_0_v100, tpt_no_0_v100 = get_tpt_tppt(num_particles_list_v100, "no", 0, gpu="v100")
tppt_no_6_v100, tpt_no_6_v100 = get_tpt_tppt(num_particles_list_v100, "no", 6, gpu="v100")
tppt_all_0_v100, tpt_all_0_v100 = get_tpt_tppt(num_particles_list_v100, ecloud_type, 0, gpu="v100")
tppt_all_6_v100, tpt_all_6_v100 = get_tpt_tppt(num_particles_list_v100, ecloud_type, 6, gpu="v100")

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

fig3 = plt.figure(3)
ax3 = fig3.add_subplot(111)
ax3.plot(num_particles_list, tppt_no_0, 'b-', label="A100")
ax3.plot(num_particles_list, tppt_all_0, 'r-', label="A100, e-clouds")
ax3.plot(num_particles_list_v100, tppt_no_0_v100, 'b--', label="V100")
ax3.plot(num_particles_list_v100, tppt_all_0_v100, 'r--', label="V100, e-clouds")
ax3.set_yscale('log')
ax3.set_xscale('log')
ax3.set_xlabel("Number of particles")
ax3.set_ylabel("Time / turn / particle [us]")
#ax3.set_xticks([2000, 4000, 7000, 10000, 20480, 27648])
ax3.set_xticks([2000, 4000, 7000, 10000, 20000, 30000])
ax3.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax3.set_yticks([1, 2, 4, 7, 10, 20])
ax3.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax3.legend()

fig4 = plt.figure(4)
ax4 = fig4.add_subplot(111)
ax4.plot(num_particles_list, tpt_no_0, 'b-', label="A100")
ax4.plot(num_particles_list, tpt_all_0, 'r-', label="A100, e-clouds")
ax4.plot(num_particles_list_v100, tpt_no_0_v100, 'b--', label="V100")
ax4.plot(num_particles_list_v100, tpt_all_0_v100, 'r--', label="V100, e-clouds")
ax4.set_xlabel("Number of particles")
ax4.set_ylabel("Time / turn [ms]")
ax4.legend()

plt.show()