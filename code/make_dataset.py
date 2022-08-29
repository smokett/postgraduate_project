import os
import shutil


# for index in range(1,1001):
#     path = "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\Dataset\\" + str(index)
#     os.makedirs(path+"\\Rendering_Images")
#     os.makedirs(path+"\\Rendering_Images\\Images")
#     os.makedirs(path+"\\Rendering_Images\\Depth_PNG")
#     os.makedirs(path+"\\Rendering_Images\\Depth_EXR")
#     os.makedirs(path+"\\Rendering_Images\\Images\\L")
#     os.makedirs(path+"\\Rendering_Images\\Images\\R")
#     os.makedirs(path+"\\Rendering_Images\\Depth_PNG\\L")
#     os.makedirs(path+"\\Rendering_Images\\Depth_PNG\\R")
#     os.makedirs(path+"\\Rendering_Images\\Depth_EXR\\L")
#     os.makedirs(path+"\\Rendering_Images\\Depth_EXR\\R")

    
for index in range(901,1001):
    path = "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\Dataset\\" + str(index) + "\\"

    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRIR_dataset\\"+str(index)+".sofa",path+str(index)+"_HRIR.sofa")
    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRTF_dataset\\"+str(index)+".sofa",path+str(index)+"_HRTF.sofa")
    shutil.copy("D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\"+str(index)+".obj",path+str(index)+"_HLR.obj")
    shutil.copy("D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\"+str(index)+"_left.obj",path+str(index)+"_L.obj")
    shutil.copy("D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\"+str(index)+"_right.obj",path+str(index)+"_R.obj")
    shutil.copy("D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\"+str(index)+"_parameters_l.txt",path+str(index)+"_PPM_L.txt")
    shutil.copy("D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\"+str(index)+"_parameters_r.txt",path+str(index)+"_PPM_R.txt")
    for j in range(25):
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_L_"+str(j)+".png",path+"Rendering_Images\\Images\\L\\"+str(index)+"_Image_L_"+str(j)+".png")
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_R_"+str(j)+".png",path+"Rendering_Images\\Images\\R\\"+str(index)+"_Image_R_"+str(j)+".png")
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_L_"+str(j)+"_depth.png",path+"Rendering_Images\\Depth_PNG\\L\\"+str(index)+"_Depth_L_"+str(j)+".png")
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_R_"+str(j)+"_depth.png",path+"Rendering_Images\\Depth_PNG\\R\\"+str(index)+"_Depth_R_"+str(j)+".png")
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_L_"+str(j)+"_depth.exr",path+"Rendering_Images\\Depth_EXR\\L\\"+str(index)+"_Depth_L_"+str(j)+".exr")
        shutil.copy("D:\\fyp\\pinnar\\test_depth\\"+str(index)+"_R_"+str(j)+"_depth.exr",path+"Rendering_Images\\Depth_EXR\\R\\"+str(index)+"_Depth_R_"+str(j)+".exr")