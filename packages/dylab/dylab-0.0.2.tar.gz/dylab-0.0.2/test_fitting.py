import laserbeamsize as lbs
from dylab import Fitting
import numpy as np
import lmfit
import matplotlib.pyplot as plt

from dylab.FittingFunction import twoD_Gaussian

xc = 300
yc = 200
dx = 100
dy = 50
phi = np.radians(0)
h = 600
v = 400
max_value = 1023
noise = 25
x = np.linspace(0, h - 1, h)
y = np.linspace(0, v - 1, v)
# generate test image
test = lbs.beam_test_image(h, v, xc, yc, dx, dy, phi, noise=noise)

# a = Fitting.TwoD_Gaussian_fitting(test, x, y)
#
# a.run_fitting()
#
# lmfit.report_fit(a.result)
# print(a.result.best_values)
#
# plt.subplots(2, 1, figsize=(12, 12))
# plt.subplot(2, 1, 1)
# plt.imshow(test)
# plt.colorbar()
# plt.xticks([])
# plt.yticks([])
# plt.title('Original')
#
# plt.subplot(2, 1, 2)
# # aaa = twoD_Gaussian(a.x, a.y, **a.result.best_values)
# # aaa = aaa.reshape(np.shape(a.data_origin))
# aaa = a.get_fitting_data(test.shape)
# plt.imshow(aaa)
# plt.colorbar()
# plt.xticks([])
# plt.yticks([])
# plt.title('Original')
# plt.show()

# test_b = test[199:200][:]
# b = Fitting.OneD_Gaussian_fitting(test_b, x)
# b.run_fitting()
# bbb = b.get_fitting_data(np.shape(test_b))
# bbb = bbb.flatten()
# lmfit.report_fit(b.result)
# plt.plot(x, bbb)
#
# plt.show()

a = Fitting.Two_OneD_Gaussian_fitting(test, x, y)

a.run_fitting()

plt.subplots(2, 1, figsize=(12, 12))
plt.subplot(2, 1, 1)
plt.imshow(test)
plt.colorbar()
plt.xticks([])
plt.yticks([])
plt.title('Original')

plt.subplot(2, 1, 2)
# aaa = twoD_Gaussian(a.x, a.y, **a.result.best_values)
# aaa = aaa.reshape(np.shape(a.data_origin))
aaa = a.get_fitting_data(test.shape)
print(a.result.best_values)

plt.imshow(aaa)
plt.colorbar()
plt.xticks([])
plt.yticks([])
plt.title('Original')
plt.show()
