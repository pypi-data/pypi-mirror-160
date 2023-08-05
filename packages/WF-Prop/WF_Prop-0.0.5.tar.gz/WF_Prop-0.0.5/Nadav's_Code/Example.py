# Example wave propagation through harmonic oscillator

import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import matplotlib.animation as anim

x = np.linspace(-10,10,1024);
dx = x[1]-x[0]

m = 1 # mass
w = 1 # vibrational frequency
hbar = 1 # h-bar

V = 1/2*w**2*x**2 # harmonic oscillator potential

k = fft.fftfreq(1024,dx)*2*np.pi
#k = 2*np.pi/dx * np.arange(1024)
#$${1 \over {\sqrt 2 }}\left( {\left| 0 \right\rangle  + \left| 2 \right\rangle } \right)$$
kinit = 0
x0 = 0
x = x - x0
wavefun = (x+1)*np.exp(-w*x**2/2)
#avefun = np.cos(x)
#wavefun = np.concatenate((np.zeros((300)), np.ones((224)), np.zeros((500))))
#plt.plot(x,wavefun)
timestep = 0.1
norm = np.linalg.norm(wavefun,ord=2)
wavefun = wavefun / norm / np.sqrt(dx)

fig = plt.figure()
pxlabel = 'Position x'
ptitle = r'Harmonic Oscillator $\left| 0 \right\rangle$'
axis = plt.axes(xlim=(min(x),max(x)),ylim=(-1.5,1.5),xlabel=pxlabel,title=ptitle)
wline, = axis.plot([],[])
wline.set_color('blue')
rline, = axis.plot([],[])
rline.set_color('black')
vline, = axis.plot([],[])
vline.set_color('red')
fig.legend(["Probability Density","Real Part of Wavefunction", "Potential (Normalized)"], \
           bbox_to_anchor=(0.4, 0., 0.5, 0.3),loc=0)

n = 1000
wavefuncs = np.zeros((n,wavefun.size),dtype=np.cdouble)
for i in range(n):
    tempwavefun = np.exp(-1j*timestep*V/2)*wavefun
    tempwavefun = fft.fft(tempwavefun)
    tempwavefun = np.exp(-1j*timestep*k**2/2)*tempwavefun
    tempwavefun = fft.ifft(tempwavefun)
    wavefun = np.exp(-1j*timestep*V/2)*tempwavefun
    wavefuncs[i,:] = wavefun
    
def showWavefuncs(i):
    global wavefuncs, x, V
    wline.set_data(x,np.abs(wavefuncs[i,:])**2)
    rline.set_data(x,np.real(wavefuncs[i,:]))
    vline.set_data(x,V/np.max(V)*5)
    return wline, vline, rline
    
ani = anim.FuncAnimation(fig,showWavefuncs,frames=n,interval=50,blit=True)
#Fwriter = anim.FFMpegWriter(fps=24)
#ani.save('Harmonic_0_1_Real.mp4',writer=Fwriter)