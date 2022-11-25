import scipy.io as sio
from pylab import imshow, colorbar, show, savefig, clf, squeeze, title, xlabel, ylabel, floor
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import json
import os

from scipy.constants import e as qe


firs_pass = 0
last_pass = 400
folder = "/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/Buildup/simulations/LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_multi5/"

sim = folder.split("/")[-2]
ecloud_type = sim.split("_")[2]
index = sim.split("_")[3]
ecloud_type = ecloud_type.lower()
ir = ecloud_type[-1]
os.makedirs(f"images_{sim}")

with open("/home/kparasch/workspace/eclouds-in-xsuite/LHC_top_energy/eclouds_LHCIT_v1.json", "r") as fid:
    eclouds_info = json.load(fid)
ecloud_info = eclouds_info[f"ecloud.{ecloud_type}.ir{ir}.{index}"]

beamscreen = ecloud_info["beamscreen"].upper()
chamber = f"../../Beam_chambers/LHC_{beamscreen}.mat"

n=5
theta = np.linspace(0.,2*np.pi, 1000)
ellip1_x = n*ecloud_info["sigx_b1"]*np.cos(theta) + ecloud_info["x_b1"]
ellip1_y = n*ecloud_info["sigy_b1"]*np.sin(theta) + ecloud_info["y_b1"]
ellip2_x = n*ecloud_info["sigx_b2"]*np.cos(theta) + ecloud_info["x_b2"]
ellip2_y = n*ecloud_info["sigy_b2"]*np.sin(theta) + ecloud_info["y_b2"]

flag_log = True

N_dec = 2

i_photog = 0

fig = plt.figure(0)
for pass_ind in range(firs_pass, last_pass):

    filename_rho = folder + 'rho_video/rho_pass%d.mat'%pass_ind

    dict_ecl_video = sio.loadmat(filename_rho)
    dict_pyecltest = sio.loadmat(folder + 'Pyecltest.mat')
    chamb=sio.loadmat(chamber)
    NN = len(chamb['Vx'][0])
    xc = np.zeros([NN+1])
    yc = np.zeros([NN+1])
    xc[:-1] = chamb['Vx'][0]*1000
    xc[-1] = chamb['Vx'][0][0]*1000
    yc[:-1] = chamb['Vy'][0]*1000
    yc[-1] = chamb['Vy'][0][0]*1000

    xg = dict_ecl_video['xg_sc']
    yg = dict_ecl_video['yg_sc']
    rho_video = dict_ecl_video['rho_video']/(-qe)
    t_video = squeeze(dict_ecl_video['t_video'].real)
    b_spac = squeeze(dict_pyecltest['b_spac'].real)
    (nphotog, _, _) = rho_video.shape

    #subprocess.check_call(('rm',  '*.png'))

    for ii in range(0, nphotog, N_dec):
        fig.clear()
        ax=fig.add_subplot(111)
        ax.set_aspect('equal')
        print('Pass %d %d/%d'%(pass_ind, ii, nphotog))
        imm = np.squeeze(rho_video[ii, :, :])
        if flag_log:
            imm = np.log10(np.abs(imm))
        #imshow(imm.T, cmap=None, norm=None, interpolation=None,
        #       alpha=None, vmin=9, vmax=12)
        mb = ax.pcolormesh(xg[0]*1000, yg[0]*1000, imm.T, cmap=None, norm=None,
               alpha=None, vmin=10, vmax=13)
        ax.plot(ellip1_x*1000, ellip1_y*1000, "b", lw=2)
        ax.plot(ellip2_x*1000, ellip2_y*1000, "r", lw=2)
        cb = plt.colorbar(mappable=mb,ax=ax,aspect=20)
        cb.set_label('$\\log_{10}\\  \\rho \\ [e^-]$')
        plt.title(('passage = %d' % floor(t_video[ii] / b_spac)))
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        ax.plot(xc, yc, 'k-', lw=5)
        filename = f"images_{sim}" + str('/Pass%05d' % (i_photog)) + '.png'
        #filename = str('Pass%05d_%05d' % (pass_ind, ii)) + '.png'
        fig.savefig(filename, dpi=100)
        #clf()
        i_photog += 1


command = ('mencoder',
           'mf://*.png',
           '-mf',
           'type=png:w=800:h=600:fps=5',
           '-ovc',
           'lavc',
           '-lavcopts',
           'vcodec=mpeg4',
           '-oac',
           'copy',
           '-o',
           'output.avi')

#subprocess.check_call(command)


