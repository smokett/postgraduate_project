import sofar as sf
import numpy as np
import math
from matplotlib import pyplot as plt
import os

file_list = os.listdir("D:\\fyp\\HRTFcomparison\\barycentric_interpolated_data_80_1280_valid")
print(file_list)

for file_name in file_list:
    if file_name != "add_ITD.py" and file_name != 'copy.py':
        sofa = sf.read_sofa(file_name)
        IR = sofa.Data_IR
        position = sofa.SourcePosition

        r = 8.75
        c = 340

        new_IR = np.zeros((IR.shape[0],IR.shape[1],IR.shape[2]))

        print(IR.shape)
        for i, [a,e,d] in enumerate(position):
            a = a - 180.0
            if a >= 0:
                ear = 1
            else:
                ear = 0
            padding = abs((r/c)*(math.sin(math.radians(a))))
            padding *= 1000
            padding = int(padding)
            print(padding)
            new_IR[i,ear,padding:] = IR[i,ear,0:256-padding]
            if ear == 1:
                new_IR[i,0,:] = IR[i,0,:]
            else:
                new_IR[i,1,:] = IR[i,1,:]



        sofa.Data_IR = new_IR



        sf.write_sofa(file_name, sofa)

