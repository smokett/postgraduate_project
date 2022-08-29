import sofar as sf
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.fftpack


original_sofa = sf.read_sofa(".\\raw_data_1280\\ARI_5.sofa")
interpolated_sofa = sf.read_sofa(".\\barycentric_interpolated_data_1280\\ARI_5.sofa")
#interpolated_sofa = sf.read_sofa(".\\valid_sofa_50\\0_test.sofa")

original_hrtf = np.zeros((original_sofa.Data_IR.shape[0], original_sofa.Data_IR.shape[1], original_sofa.Data_IR.shape[2]//2))
interpolated_hrtf = np.zeros((original_sofa.Data_IR.shape[0], original_sofa.Data_IR.shape[1], original_sofa.Data_IR.shape[2]//2))

for i in range(original_sofa.Data_IR.shape[0]):
    for j in range(original_sofa.Data_IR.shape[1]):
        original_hrtf[i,j,:] =  scipy.fft.rfft(original_sofa.Data_IR[i,j,1:])
        interpolated_hrtf[i,j,:] =  scipy.fft.rfft(interpolated_sofa.Data_IR[i,j,1:])

source_positions = original_sofa.SourcePosition

left_SD = np.zeros((original_hrtf.shape[2]))

for i in range(original_hrtf.shape[2]):
    sum_on_node = 0.0
    for j in range(0,original_sofa.Data_IR.shape[0]):
        sum_on_node += (20 * np.log10(abs(original_hrtf[j,0,i]) / abs(interpolated_hrtf[j,0,i])))**2
    sum_on_node /= original_sofa.Data_IR.shape[0]
    left_SD[i] = np.sqrt(sum_on_node)


#print(left_SD)

x = np.linspace(0.0,24000.0,128)
#print(x)

plt.bar(x,left_SD,width=50)
plt.title("SD per frequency -- real vs barycentric interpolated " + "left")
plt.xlabel("azimuth")
plt.ylabel("elevation")
#plt.show()
plt.savefig("SD_band.png", dpi=300)
plt.close()






