import tkinter as tk
import numpy as np
from tkinter import filedialog
from ReadLOCPOT import ReadLOCPOT
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from CPFunctions import *

def showWavefuncs(i):
    global wavefuncs, z, Potential, KAxis, axis
    wline.set_data(z,np.abs(wavefuncs[i,:])**2)
    wline.set_color('blue')
    vline.set_data(z,Potential/np.max(Potential))
    vline.set_color('red')
    jline.set_data(z,probcurs[i,:]/4)
    jline.set_color('magenta')
    axis.legend([r'${\left| \psi  \right|^2}$ [1/A]', 'V [eV]', \
                 'Probability Current [1/fs]'],loc="upper left")
    #tline.set_data(timesteps[0:i],cumprob[0:i])
    #,z,Potential/np.max(Potential),'r')
    return wline, vline, jline


root = tk.Tk()
root.withdraw()


n = 1000
timestep = 0.001 # in fs
flt = 0
cumprob = np.zeros((n,4),dtype=np.cdouble)

for fl in ['OHH', 'OH', 'O', 'OOH']:
    #FilePath = filedialog.askopenfilename(title="Choose LOCPOT File")
    FilePath = 'D:\OneDrive - Technion/Charge Transfer\LOCPOT-' + fl
    Potential, ZAxis, KAxis = ReadLOCPOT(FilePath)
    #plt.plot(ZAxis,Potential)

    # electron charge in C
    q = 1.602176634e-19

    z = ZAxis

    tempPot = np.copy(Potential)
    tempPot[(z < 11) | (z > 13)] = 0
    MinPot = np.argmin(tempPot)
    if (z[MinPot] == z[-1]/2):
        MinPot = MinPot + 1
        
    z0 = z[MinPot]
        
    dz = z[1]-z[0]
        
    sigma = 1 # in A
        
    # From OUTCAR. Ordered OH2, OH, O, OOH
    totalEnergy = np.array([2.2844, 1.9731, 0.0116, 1.7893])*q
    
    k0 = initialMomentum(totalEnergy[flt], np.exp(-(z-z0)**2/(2*sigma**2)), Potential*q, \
                         dz*1e-10, sigma, np.max(z), z0)
    k0 = np.abs(float(np.real(complex(k0[0]))/1e10))
    
    wavefun = np.exp(1j*k0*z)*np.exp(-(z-z0)**2/(2*sigma**2))
    owavefun = wavefun = np.exp(1j*k0*z)*np.exp(-(z-z0)**2/(2*sigma**2))
    norm = np.linalg.norm(wavefun,ord=2)
    
    wavefun = wavefun / norm / np.sqrt(dz)
    
    Vexp = potentialExpectation(wavefun, Potential, dz)
    
    wavefuncs = np.zeros((n+1,z.size),dtype=np.cdouble)
    
    timesteps = timestep*np.arange(n)
    probcurs = np.zeros((n+1,z.size),dtype=np.cdouble)
    for i in range(n):
        wavefuncs[i,:] = wavefun
        probcurs[i,:] = calculateProbabilityCurrent(wavefun, KAxis)
        cumprob[i,flt] = cumulativeProb(wavefun, z, 0.77*max(z), dz)
        wavefun = RunOneTimestep(wavefun, timestep, Potential, KAxis)
        
    
    """
    headers = ['$*OH_2$','$*OH$','$*O$','$*OOH$']
    
    fig = plt.figure()
    pxlabel = 'Position z [A]'
    ptitle = r'Wavefunction Propagation of ' + headers[flt] + ' Termination'
    axis = plt.axes(xlim=(min(z),max(z)),ylim=(-4.5,3.5),xlabel=pxlabel,title=ptitle)
    wline, = axis.plot([],[])
    vline, = axis.plot([],[])
    jline, = axis.plot([],[])

    ani = anim.FuncAnimation(fig,showWavefuncs,frames=n,interval=50,blit=True)
        
    Fwriter = anim.FFMpegWriter(fps=24)
    ani.save('LOCPOT-' + fl + '.mp4',writer=Fwriter)
    plt.close(fig)
    """
    flt = flt + 1

# end of outer loop

figt = plt.figure()
pxlabel = 'Time t [fs]'
ptitle = 'Cumulative Probability Beyond Surface'
axist = plt.axes(xlim=(0,n*timestep),ylim=(0,1),xlabel=pxlabel,title=ptitle)
tline = axist.plot(timesteps,cumprob)
axist.legend([r'$*OH_2$',r'$*OH$',r'$*O$',r'$*OOH$'])