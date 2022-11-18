import numpy as np
import matplotlib.pyplot as plt
import scipy.io

#BS = scipy.io.loadmat("Beam_chambers/LHC_BS005.mat")
BS = scipy.io.loadmat("Beam_chambers/LHC_BS010.mat")

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.plot(np.squeeze(BS["Vx"]), np.squeeze(BS["Vy"]),"k.-")

plt.show()
