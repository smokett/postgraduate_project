import os
import shutil
# for index in range(704,705):
#     os.system("cd "+ "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\" +str(index)+" && Output2HRTF.py")
#     print("finished " + str(index))

# #name for training
for index in range(521,522):
    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\" +str(index)+"\\Output2HRTF\\HRIR_gan_1280.sofa", "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRIR\\hrtf b_nh"+str(index)+".sofa")

for index in range(521,522):
    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\" +str(index)+"\\Output2HRTF\\HRTF_gan_1280.sofa", "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRTF\\hrtf b_nh"+str(index)+".sofa")




# # #name for dataset
for index in range(521,522):
    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\" +str(index)+"\\Output2HRTF\\HRIR_gan_1280.sofa", "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRIR_dataset\\"+str(index)+".sofa")

for index in range(521,522):
    shutil.copy("D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\" +str(index)+"\\Output2HRTF\\HRTF_gan_1280.sofa", "D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\HRTF_dataset\\"+str(index)+".sofa")