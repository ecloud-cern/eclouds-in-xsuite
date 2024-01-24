import pickle
import numpy as np
import matplotlib.pyplot as plt
import json

with open("../../eclouds_LHCIT_v1.json", "r") as fid:
    eclouds = json.load(fid)

ecloud_type = "q1r5"
index=0
key = f"ecloud.{ecloud_type}.ir{ecloud_type[-1]}.{index}"
data = pickle.load(open("aperture_q1r5.pkl","rb"))

sigrat = (3.5/2.0)**0.5
xmin = data["xmin"][key]
xmax = data["xmax"][key]
ymin = data["ymin"][key]
ymax = data["ymax"][key]

pzeta = data["pzeta"]

plt.figure(2)
plt.plot(pzeta, np.array(xmin)*sigrat, "bo-")
plt.plot(pzeta, np.array(xmax)*sigrat, "bo-")
plt.plot(pzeta, np.array(ymin)*sigrat, "ro-")
plt.plot(pzeta, np.array(ymax)*sigrat, "ro-")
plt.xlabel("pzeta")
plt.ylabel("required aperture")
xnn = []
xnx = []
xxn = []
xxx = []
ynn = []
ynx = []
yxn = []
yxx = []
x_c = []
y_c = []
indices = []

ii=0
for reg in ["r5", "l5", "r1", "l1"]:
    for ecloud_type in ["q1", "dr12", "q2a", "dr2", "q2b", "dr23", "q3"]:
        data = pickle.load(open(f"aperture_{ecloud_type}{reg}.pkl","rb"))
        for index in range(len(data["xmin"].keys())):
            
            indices.append(ii)
            ii += 1
            key = f"ecloud.{ecloud_type}{reg}.ir{reg[-1]}.{index}"
    
            xminmin = np.min(data["xmin"][key])
            xminmax = np.max(data["xmin"][key])
            
            xmaxmin = np.min(data["xmax"][key])
            xmaxmax = np.max(data["xmax"][key])
    
            yminmin = np.min(data["ymin"][key])
            yminmax = np.max(data["ymin"][key])
            
            ymaxmin = np.min(data["ymax"][key])
            ymaxmax = np.max(data["ymax"][key])
            xnn.append(xminmin)#* sigrat  * eclouds[key]["sigx_b1"] + eclouds[key]["x_b1"])
            xnx.append(xminmax)#* sigrat  * eclouds[key]["sigx_b1"] + eclouds[key]["x_b1"])
            xxn.append(xmaxmin)#* sigrat  * eclouds[key]["sigx_b1"] + eclouds[key]["x_b1"])
            xxx.append(xmaxmax)#* sigrat  * eclouds[key]["sigx_b1"] + eclouds[key]["x_b1"])
            ynn.append(yminmin)#* sigrat  * eclouds[key]["sigy_b1"] + eclouds[key]["y_b1"])
            ynx.append(yminmax)#* sigrat  * eclouds[key]["sigy_b1"] + eclouds[key]["y_b1"])
            yxn.append(ymaxmin)#* sigrat  * eclouds[key]["sigy_b1"] + eclouds[key]["y_b1"])
            yxx.append(ymaxmax)#* sigrat  * eclouds[key]["sigy_b1"] + eclouds[key]["y_b1"])
            x_c.append(eclouds[key]["x_b1"] /eclouds[key]["sigx_b1"]/sigrat)
            y_c.append(eclouds[key]["y_b1"] /eclouds[key]["sigy_b1"]/sigrat)

fig1 = plt.figure(1)
ax = fig1.add_subplot(111)
ax.plot(indices, np.array(xnn), "bo-")
ax.plot(indices, np.array(xnx), "bo-")
ax.plot(indices, np.array(xxn), "bo-")
ax.plot(indices, np.array(xxx), "bo-", label = "Horizontal")
ax.plot(indices, np.array(ynn), "ro-")
ax.plot(indices, np.array(ynx), "ro-")
ax.plot(indices, np.array(yxn), "ro-")
ax.plot(indices, np.array(yxx), "ro-", label = "Vertical")
# ax.plot(indices, np.array(x_c), "ko--")
# ax.plot(indices, np.array(y_c), "ko--")
ax.set_xlabel("Index")
ax.set_ylabel("Required aperture")
ax.legend()
ax.axhline(-5*sigrat, c='k', ls="--", lw=2)
ax.axhline(+5*sigrat, c='k', ls="--", lw=2)
plt.show()