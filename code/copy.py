import os
import shutil

file_list = os.listdir("./valid_real")
file_index_list = []
for i in range(len(file_list)):
    if file_list[i].endswith("left"):
        file_list[i] = file_list[i].replace("ARI_","")
        file_list[i] = file_list[i].replace("left","")
        file_index_list.append(int(file_list[i]))

file_index_list.sort()
print(file_index_list)

for file in file_index_list:
    shutil.copy('.\\barycentric_interpolated_data_5_1280\\'+'ARI_'+str(file)+'.sofa','.\\barycentric_interpolated_data_20_1280_valid\\'+'ARI_'+str(file)+'.sofa')

