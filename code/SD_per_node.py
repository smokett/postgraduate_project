import sofar as sf
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.fftpack
import os

file_list = os.listdir("./valid_real")
file_index_list = []
f = open("avg_score.txt","w")
for i in range(len(file_list)):
    if file_list[i].endswith("left"):
        file_list[i] = file_list[i].replace("ARI_","")
        file_list[i] = file_list[i].replace("left","")
        file_index_list.append(int(file_list[i]))

file_index_list.sort()
print(file_index_list)
for file in file_index_list:
    original_sofa = sf.read_sofa(".\\raw_data_1280\\ARI_"+str(file)+".sofa")
    interpolated_sofa = sf.read_sofa(".\\barycentric_interpolated_data_5_1280\\ARI_"+str(file)+".sofa")
    #interpolated_sofa = sf.read_sofa(".\\valid_sofa_50\\0_test.sofa")

    print(interpolated_sofa.Data_IR.shape)


    original_hrtf = np.zeros((original_sofa.Data_IR.shape[0], original_sofa.Data_IR.shape[1], original_sofa.Data_IR.shape[2]//2))
    interpolated_hrtf = np.zeros((original_sofa.Data_IR.shape[0], original_sofa.Data_IR.shape[1], original_sofa.Data_IR.shape[2]//2))

    for i in range(original_sofa.Data_IR.shape[0]):
        for j in range(original_sofa.Data_IR.shape[1]):
            original_hrtf[i,j,:] =  scipy.fft.rfft(original_sofa.Data_IR[i,j,1:])
            interpolated_hrtf[i,j,:] =  scipy.fft.rfft(interpolated_sofa.Data_IR[i,j,1:])

    source_positions = original_sofa.SourcePosition

    for index in range(2):

        left_SD = np.zeros((original_sofa.Data_IR.shape[0]))

        for i in range(original_sofa.Data_IR.shape[0]):
            sum_on_band = 0.0
            for j in range(10,original_hrtf.shape[2]):
                sum_on_band += (20.0 * np.log10(abs(original_hrtf[i,index%2,j]) / abs(interpolated_hrtf[i,index%2,j])))**2
            sum_on_band /= (original_hrtf.shape[2]-10)
            left_SD[i] = np.sqrt(sum_on_band)


        print(max(left_SD))

        x = source_positions[:,0] - 180.0
        y = source_positions[:,1]

        plt.scatter(x,y,c=left_SD, cmap="coolwarm", vmin=0.0, vmax=20.0)
        plt.colorbar()
        if index%2 == 0:
            plt.title("SD per node--real vs Barycentric " + "left ear avg SD:"+str(round(sum(left_SD)/(len(left_SD)),4)))
        else:
            plt.title("SD per node--real vs Barycentric " + "right ear avg SD:"+str(round(sum(left_SD)/(len(left_SD)),4)))
        plt.xlabel("azimuth")
        plt.ylabel("elevation")
        if index%2 == 0:
            plt.savefig("SD_node_"+str(file)+"left.png", dpi=300)
        else:
            plt.savefig("SD_node_"+str(file)+"right.png", dpi=300)
        #plt.show()
        plt.close()
        f.write(str(sum(left_SD)/(len(left_SD)))+'\n')
f.close()






