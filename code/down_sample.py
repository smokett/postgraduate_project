import sofar as sf
import math
import pickle
import numpy as np
import scipy.fftpack
import torch
import os

scale_f = 16

sofa = sf.read_sofa("0_test.sofa")

file_list = os.listdir("./"+"all_data")
file_set = []
for i in range(len(file_list)):
    if file_list[i].endswith("left"):
        file_set.append(file_list[i][:-4])


IR_temp = np.zeros((3,5,16,16))
IR_low_temp = np.zeros((1280//(scale_f**2),3))
count = 0


for i in range(5):
    for j in range(16):
        for k in range(16):
            IR_temp[:,i,j,k] = sofa.SourcePosition[count,:]
            count += 1

IR_temp = torch.tensor(IR_temp)       
IR_temp = torch.nn.functional.interpolate(IR_temp, scale_factor=1 / scale_f, mode='nearest-exact')
print(IR_temp.shape)

count = 0
for i in range(5):
    for j in range(16//scale_f):
        for k in range(16//scale_f):
            IR_low_temp[count,:] = IR_temp[:,i,j,k]
            count += 1

sofa.SourcePosition = IR_low_temp


for f in file_set:
    with open("./" + "all_data/" + f + "left", "rb") as file:
        left = pickle.load(file)


    with open("./" + "all_data/" + f + "right", "rb") as file:
        right = pickle.load(file)

    left = torch.permute(left, (0,3,1,2))
    right = torch.permute(right, (0,3,1,2))
    left = torch.nn.functional.interpolate(left, scale_factor=1 / scale_f, mode='nearest-exact')
    right = torch.nn.functional.interpolate(right, scale_factor=1 / scale_f, mode='nearest-exact')
    left = left.numpy()
    right = right.numpy()
    print(left.shape)

    left_hrir = left
    right_hrir = right

    total_hrir = np.zeros((1280//(scale_f**2),2,128))
    count = 0
    for i in range(left_hrir.shape[0]):
        for j in range(left_hrir.shape[2]):
            for k in range(left_hrir.shape[3]):
                total_hrir[count,0,:] = left_hrir[i,:,j,k]
                total_hrir[count,1,:] = right_hrir[i,:,j,k]
                count += 1

    sofa.Data_IR = total_hrir

    sf.write_sofa(f.replace('ARI_', 'hrtf b_nh') + ".sofa", sofa)