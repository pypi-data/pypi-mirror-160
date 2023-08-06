import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-15,30,2001)
dx = x[1]-x[0]
f = np.cos(x)*np.exp(-x**2/25)

df = -(np.sin(x)*np.exp(-x**2/25) + (2/25)*x*f)

k = np.fft.fftfreq(2001, dx)*2*np.pi

dff = np.fft.fft(f)
dff = 1j*k*dff
dff = np.real(np.fft.ifft(dff))

plt.plot(x,df,'r',linewidth=8)
plt.plot(x,dff,'b',linewidth=1)