from matplotlib import pyplot as plt

bary = [4.985, 6.244, 8.4252]
gan_no_tl = [5.17, 5.4510, 5.5267]
#gan_tl = [4.162, 4.480, 8.1309]
x = ['80 -> 1280 (93.7% reduction)', '20 -> 1280 (98.4% reduction)', '5 -> 1280 (99.6% reduction)']

plt.plot(x,bary,'s-',color='r',label='Barycentric')
plt.plot(x,gan_no_tl,'o-',color='g',label='GAN Without Tranfer Learning')
#plt.plot(x,gan_tl,'x-',color='b',label='GAN With Tranfer Learning')
plt.title('SD Error')
plt.xlabel('interpolated nodes number')
plt.ylabel('error (dB)')
plt.legend()
plt.show()



bary = [6.5694, 6.1057, 22.4410]
gan_no_tl = [10.3851, 13.0904, 13.2910]
#gan_tl = [24.0596, 20.7226, 29.6498]
real = [3.4612, 3.4612, 3.4612]

plt.plot(x,bary,'s-',color='r',label='Barycentric')
plt.plot(x,gan_no_tl,'o-',color='g',label='GAN Without Tranfer Learning')
#plt.plot(x,gan_tl,'x-',color='b',label='GAN With Tranfer Learning')
plt.plot(x,real,'--',color='grey',label='Real HRTF')
plt.title('Localization -- Polar Accuracy Error (abs)')
plt.xlabel('interpolated nodes number')
plt.ylabel('Absolute Polar Accuracy Error (degrees)')
plt.legend()
plt.show()



bary = [31.3358, 34.2954, 41.4414]
gan_no_tl = [37.0304, 38.0232, 38.6161]
#gan_tl = [41.8075, 40.8904, 42.2717]
real = [27.6179, 27.6179, 27.6179]

plt.plot(x,bary,'s-',color='r',label='Barycentric')
plt.plot(x,gan_no_tl,'o-',color='g',label='GAN Without Tranfer Learning')
#plt.plot(x,gan_tl,'x-',color='b',label='GAN With Tranfer Learning')
plt.plot(x,real,'--',color='grey',label='Real HRTF')
plt.title('Localization -- Polar RMS Error')
plt.xlabel('interpolated nodes number')
plt.ylabel('Polar RMS Error (degrees)')
plt.legend()
plt.show()



bary = [13.9916, 20.2492, 33.2841]
gan_no_tl = [30.5644, 30.1276, 31.7318]
#gan_tl = [35.8505, 35.8489, 41.4459]
real = [10.1612, 10.1612, 10.1612]

plt.plot(x,bary,'s-',color='r',label='Barycentric')
plt.plot(x,gan_no_tl,'o-',color='g',label='GAN Without Tranfer Learning')
#plt.plot(x,gan_tl,'x-',color='b',label='GAN With Tranfer Learning')
plt.plot(x,real,'--',color='grey',label='Real HRTF')
plt.title('Localization -- Quadrant Error')
plt.xlabel('interpolated nodes number')
plt.ylabel('Quadrant Error (%)')
plt.legend()
plt.show()