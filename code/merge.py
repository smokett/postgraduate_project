from turtle import right
import torch
import numpy as np
import os
import pickle

file_list = os.listdir("./valid_real")
file_index_list = []
for i in range(len(file_list)):
    if file_list[i].endswith("left"):
        file_list[i] = file_list[i].replace("ARI_","")
        file_list[i] = file_list[i].replace("left","")
        file_index_list.append(int(file_list[i]))

file_index_list.sort()
for f in file_index_list:
    with open("./valid_real/"+"ARI_"+str(f)+"left", "rb") as file:
        left_data = pickle.load(file)
    with open("./valid_real/"+"ARI_"+str(f)+"right", "rb") as file:
        right_data = pickle.load(file)
    data = torch.cat((left_data,right_data),dim=3)
    with open("./valid/"+"ARI_"+str(f), "wb") as file:
        pickle.dump(data, file)
        print(data.shape)
    
