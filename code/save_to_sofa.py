import sofar as sf
import math
import pickle
import numpy as np
import scipy.fftpack
import torch
import os

file_list = os.listdir("./"+"low_5")
file_set = []
for i in range(len(file_list)):
    if file_list[i].endswith("left"):
        file_set.append(file_list[i][:-4])

sofa = sf.read_sofa("0_test.sofa")
print(sofa.Data_IR.shape)
print(sofa.SourcePosition.shape)

for f in file_set:
    with open("./" + "low_5/" + f + "left", "rb") as file:
        left = pickle.load(file)
        left = left.numpy()
        print(left.shape)

    with open("./" + "low_5/" + f + "right", "rb") as file:
        right = pickle.load(file)
        right = right.numpy()

    # for real data remove padding
    #left = left[:,2:-2,2:-2,:]
    #right = right[:,2:-2,2:-2,:]

    left_hrir = np.zeros((left.shape[0],left.shape[1],left.shape[2],left.shape[3]*2))
    right_hrir = left_hrir.copy()

    for i in range(left.shape[0]):
        for j in range(left.shape[1]):
            for k in range(left.shape[2]):
                left_hrir[i,j,k] = scipy.fft.irfft(np.concatenate((np.array([1.0]),left[i,j,k])))
                right_hrir[i,j,k] = scipy.fft.irfft(np.concatenate((np.array([1.0]),right[i,j,k])))

    total_hrir = np.zeros((left_hrir.shape[0]*left_hrir.shape[1]*left_hrir.shape[2],2,left_hrir.shape[3]))
    count = 0
    for i in range(left_hrir.shape[0]):
        for j in range(left_hrir.shape[1]):
            for k in range(left_hrir.shape[2]):
                total_hrir[count,0] = left_hrir[i,j,k]
                total_hrir[count,1] = right_hrir[i,j,k]
                count += 1

    # when saving real data, exchange the first four panels and flip the last sky panel

    # temp = total_hrir[0:1024]
    # tmp1 = temp[0:512]
    # tmp2 = temp[512:]
    # temp = np.concatenate((tmp2,tmp1),0)

    # temp_1 = total_hrir[1024:]
    # temp_1 = np.flip(temp_1,0)

    # total_hrir = np.concatenate((temp, temp_1), axis=0)

    sofa.Data_IR = total_hrir
    total_SourcePosition = np.zeros((total_hrir.shape[0],3))
    coordinates_file = open("generated_coordinates_degree.txt","r")
    count = 0
    for line in coordinates_file:
        line = line.strip()
        total_SourcePosition[count,0] = float(line.split(" ")[1])
        total_SourcePosition[count,1] = float(line.split(" ")[0])
        total_SourcePosition[count,2] = 1.0
        count += 1
    sofa.SourcePosition = total_SourcePosition
    sf.write_sofa(".//barycentric_interpolated_data_5_1280//"+f+".sofa", sofa)






