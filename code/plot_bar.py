import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import numpy as np

mpl.rcParams['figure.dpi'] = 300

x = ['80 -> 1280 (93.7% reduction)', '20 -> 1280 (98.4% reduction)', '5 -> 1280 (99.6% reduction)']
x_axis = np.arange(len(x))


bary = np.array([4.985,6.244,8.4252])
bary_std = np.array([0.623893,0.5913,0.556915])
bary_min = np.array([3.730465,5.126742,7.29963])
bary_max = np.array([6.429319,7.491331,9.6269])
gan_no_tl = np.array([5.1728,5.4510,5.526739])
gan_no_tl_std = np.array([0.2067,0.253673,0.305187])
gan_no_tl_min = np.array([4.60015,4.71335,4.65615])
gan_no_tl_max = np.array([5.70082,6.08567,6.4129])
gan_tl = np.array([4.88278,5.11183,5.3453])
gan_tl_std = np.array([0.210375,0.233909,0.264607])
gan_tl_min = np.array([4.27686,4.38124,4.81673])
gan_tl_max = np.array([5.41218,5.71226,6.21855])
bary_median = np.array([4.9341,6.2265,8.3860])
gan_no_tl_median = np.array([5.1560,5.4673,5.4969])
gan_tl_median = np.array([4.8565,5.1240,5.3431])


plt.errorbar(x_axis-0.05, bary, bary_std, lw=8, markersize='20', fmt='_', color='r', label='Barycentric')
plt.errorbar(x_axis-0.05, bary, [bary-bary_min,bary_max-bary], lw=1, fmt='.', color='r', capsize=5, markersize='0')
plt.errorbar(x_axis+0.05, gan_no_tl, gan_no_tl_std, lw=8, markersize='20', fmt='_', color='g', label='GAN Without Tranfer Learning')
plt.errorbar(x_axis+0.05, gan_no_tl, [gan_no_tl-gan_no_tl_min,gan_no_tl_max-gan_no_tl], lw=1, fmt='.', color='g', capsize=5, markersize='0')
plt.errorbar(x_axis+0.15, gan_tl, gan_tl_std, lw=8, markersize='20',fmt='_', color='b', label='GAN With Tranfer Learning')
plt.errorbar(x_axis+0.15, gan_tl, [gan_tl-gan_tl_min,gan_tl_max-gan_tl], lw=1, fmt='.', color='b', capsize=5, markersize='0')
plt.plot(x_axis-0.05, bary_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.05, gan_no_tl_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.15, gan_tl_median, 'D', color='black', markersize='5')


plt.xticks(x_axis, x)
plt.title('SD Error')
plt.xlabel('Interpolated nodes number')
plt.ylabel('error (dB)')
plt.legend(loc=2)
plt.show()




bary = np.array([6.44, 5.9901, 19.3505])
bary_std = np.array([3.1675,4.0467,18.4109])
bary_min = np.array([-0.4301,-2.8852,-32.5976])
bary_max = np.array([12.5009,15.3781,62.6848])
gan_no_tl = np.array([7.5083, 11.6588, 9.2787])
gan_no_tl_std = np.array([12.9373, 12.9101, 13.0120])
gan_no_tl_min = np.array([-32.4767,-17.3895,-21.3209])
gan_no_tl_max = np.array([33.8278,47.5795,40.3159])
gan_tl = np.array([8.1772,9.4727,8.5249])
gan_tl_std = np.array([14.2740,11.6589,14.1482])
gan_tl_min = np.array([-33.0635,-24.0477,-22.7150])
gan_tl_max = np.array([33.8585,37.2195,37.1928])
real = np.array([3.2815, 3.2815, 3.2815])
real_std = np.array([2.2191,2.2191,2.2191])
real_min = np.array([-1.5209, -1.5209, -1.5209])
real_max = np.array([8.3658,8.3658,8.3658])
bary_median = np.array([7.1061, 6.3957, 18.4262])
gan_no_tl_median = np.array([4.4981,9.8950,10.1845])
gan_tl_median = np.array([6.64,7.2156,7.9143])
real_median = np.array([3.3221,3.3221,3.3221])



plt.errorbar(x_axis-0.15, real, real_std, lw=8, markersize='20', fmt='_', color='grey', label='Real HRTF')
plt.errorbar(x_axis-0.15, real, [real-real_min,real_max-real], lw=1, fmt='.', color='grey', capsize=5, markersize='0')
plt.errorbar(x_axis-0.05, bary, bary_std, lw=8, markersize='20', fmt='_', color='r', label='Barycentric')
plt.errorbar(x_axis-0.05, bary, [bary-bary_min,bary_max-bary], lw=1, fmt='.', color='r', capsize=5, markersize='0')
plt.errorbar(x_axis+0.05, gan_no_tl, gan_no_tl_std, lw=8, markersize='20', fmt='_', color='g', label='GAN Without Tranfer Learning')
plt.errorbar(x_axis+0.05, gan_no_tl, [gan_no_tl-gan_no_tl_min,gan_no_tl_max-gan_no_tl], lw=1, fmt='.', color='g', capsize=5, markersize='0')
plt.errorbar(x_axis+0.15, gan_tl, gan_tl_std, lw=8, markersize='20',fmt='_', color='b', label='GAN With Tranfer Learning')
plt.errorbar(x_axis+0.15, gan_tl, [gan_tl-gan_tl_min,gan_tl_max-gan_tl], lw=1, fmt='.', color='b', capsize=5, markersize='0')
plt.plot(x_axis-0.15, real_median, 'D', color='black', markersize='5')
plt.plot(x_axis-0.05, bary_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.05, gan_no_tl_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.15, gan_tl_median, 'D', color='black', markersize='5')


plt.xticks(x_axis, x)
plt.title('Localisation -- Polar Accuracy Error (Elevation Bias)')
plt.xlabel('Interpolated nodes number')
plt.ylabel('Polar Accuracy Error (degrees)')
plt.legend(loc=2)
plt.show()




bary = np.array([31.3358,34.2954,41.4414])
bary_std = np.array([1.5517,1.3544,1.4131])
bary_min = np.array([28.1162,30.4129,38.6340])
bary_max = np.array([34.1474,37.2833,44.5246])
gan_no_tl = np.array([37.8635,38.0232,38.6161])
gan_no_tl_std = np.array([2.3075,2.2260,2.2152])
gan_no_tl_min = np.array([32.4781,33.1632,33.2929])
gan_no_tl_max = np.array([42.8533,45.2249,44.7010])
gan_tl = np.array([37.8327,37.4562,38.1068])
gan_tl_std = np.array([2.5480,2.2572,2.3452])
gan_tl_min = np.array([30.8255,32.5034,32.3064])
gan_tl_max = np.array([42.8024,41.9715,42.9718])
real = np.array([27.6179,27.6179,27.6179])
real_std = np.array([1.8612,1.8612,1.8612])
real_min = np.array([23.1944,23.1944,23.1944])
real_max = np.array([31.6905,31.6905,31.6905])
bary_median = np.array([31.5595,34.3570,41.5300])
gan_no_tl_median = np.array([37.4782,38.1350,38.6071])
gan_tl_median = np.array([37.9541,37.4934,38.1861])
real_median = np.array([27.4791,27.4791,27.4791])


plt.errorbar(x_axis-0.15, real, real_std, lw=8, markersize='20', fmt='_', color='grey', label='Real HRTF')
plt.errorbar(x_axis-0.15, real, [real-real_min,real_max-real], lw=1, fmt='.', color='grey', capsize=5, markersize='0')
plt.errorbar(x_axis-0.05, bary, bary_std, lw=8, markersize='20', fmt='_', color='r', label='Barycentric')
plt.errorbar(x_axis-0.05, bary, [bary-bary_min,bary_max-bary], lw=1, fmt='.', color='r', capsize=5, markersize='0')
plt.errorbar(x_axis+0.05, gan_no_tl, gan_no_tl_std, lw=8, markersize='20', fmt='_', color='g', label='GAN Without Tranfer Learning')
plt.errorbar(x_axis+0.05, gan_no_tl, [gan_no_tl-gan_no_tl_min,gan_no_tl_max-gan_no_tl], lw=1, fmt='.', color='g', capsize=5, markersize='0')
plt.errorbar(x_axis+0.15, gan_tl, gan_tl_std, lw=8, markersize='20',fmt='_', color='b', label='GAN With Tranfer Learning')
plt.errorbar(x_axis+0.15, gan_tl, [gan_tl-gan_tl_min,gan_tl_max-gan_tl], lw=1, fmt='.', color='b', capsize=5, markersize='0')
plt.plot(x_axis-0.15, real_median, 'D', color='black', markersize='5')
plt.plot(x_axis-0.05, bary_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.05, gan_no_tl_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.15, gan_tl_median, 'D', color='black', markersize='5')

plt.xticks(x_axis, x)
plt.title('Localisation -- Polar RMS Error')
plt.xlabel('Interpolated nodes number')
plt.ylabel('Polar RMS Error (degrees)')
plt.legend(loc=2, bbox_to_anchor=(-0.1,1.15))
plt.show()




bary = np.array([13.9916,20.2492,33.2841])
bary_std = np.array([2.8202,3.3175,4.4075])
bary_min = np.array([7.2098,13.6161,23.8604])
bary_max = np.array([20.1716,28.4865,42.6073])
gan_no_tl = np.array([31.5644,30.1276,31.7318])
gan_no_tl_std = np.array([5.6973,5.7992,5.6682])
gan_no_tl_min = np.array([17.6794,19.2012,19.1475])
gan_no_tl_max = np.array([43.9515,46.6667,42.8305])
gan_tl = np.array([32.0767,29.8669,31.0653])
gan_tl_std = np.array([6.2066,5.8403,6.0263])
gan_tl_min = np.array([13.0506,14.1455,18.3647])
gan_tl_max = np.array([46.6755,41.6085,42.5804])
real = np.array([10.1612,10.1612,10.1612])
real_std = np.array([2.4092,2.4092,2.4092])
real_min = np.array([4.1098,4.1098,4.1098])
real_max = np.array([16.1438,16.14383,16.1438])
bary_median = np.array([13.7814,20.2051,33.4783])
gan_no_tl_median = np.array([31.8519,29.8652,31.3487])
gan_tl_median = np.array([32.0031,29.5682,30.0969])
real_median = np.array([10.5226,10.5226,10.5226])


plt.errorbar(x_axis-0.15, real, real_std, lw=8, markersize='20', fmt='_', color='grey', label='Real HRTF')
plt.errorbar(x_axis-0.15, real, [real-real_min,real_max-real], lw=1, fmt='.', color='grey', capsize=5, markersize='0')
plt.errorbar(x_axis-0.05, bary, bary_std, lw=8, markersize='20', fmt='_', color='r', label='Barycentric')
plt.errorbar(x_axis-0.05, bary, [bary-bary_min,bary_max-bary], lw=1, fmt='.', color='r', capsize=5, markersize='0')
plt.errorbar(x_axis+0.05, gan_no_tl, gan_no_tl_std, lw=8, markersize='20', fmt='_', color='g', label='GAN Without Tranfer Learning')
plt.errorbar(x_axis+0.05, gan_no_tl, [gan_no_tl-gan_no_tl_min,gan_no_tl_max-gan_no_tl], lw=1, fmt='.', color='g', capsize=5, markersize='0')
plt.errorbar(x_axis+0.15, gan_tl, gan_tl_std, lw=8, markersize='20',fmt='_', color='b', label='GAN With Tranfer Learning')
plt.errorbar(x_axis+0.15, gan_tl, [gan_tl-gan_tl_min,gan_tl_max-gan_tl], lw=1, fmt='.', color='b', capsize=5, markersize='0')
plt.plot(x_axis-0.15, real_median, 'D', color='black', markersize='5')
plt.plot(x_axis-0.05, bary_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.05, gan_no_tl_median, 'D', color='black', markersize='5')
plt.plot(x_axis+0.15, gan_tl_median, 'D', color='black', markersize='5')

plt.xticks(x_axis, x)
plt.title('Localisation -- Quadrant Error')
plt.xlabel('interpolated nodes number')
plt.ylabel('Quadrant Error (%)')
plt.legend(loc=2, bbox_to_anchor=(0.7,1.15))
plt.show()
