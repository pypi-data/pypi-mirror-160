# All functions for ChargeProp

import numpy as np
from sympy.solvers import solve
from sympy import Symbol
from scipy.special import erf

# h-bar in eV * fs
hbarev = 6.58211951e-16 * 1e15

# h-bar in kg A^2 / fs
hbar = 1.0545718e-34 * 1e-15 * 1e20

# h-bar in J s
# Gives energy in J, k in 1/m
hbark = 1.0545718e-34

# electron mass in kg
me = 9.10938356e-31

# electron charge in C
q = 1.602176634e-19

def RunOneTimestep(wavefun, timestep, V, K):
    TempWavefun = np.exp(-1j*V*timestep/(2*hbarev))*wavefun
    TempWavefun = np.fft.fft(TempWavefun)
    TempWavefun = np.exp(-1j*hbar*timestep*K**2/(2*me))*TempWavefun
    TempWavefun = np.fft.ifft(TempWavefun)
    TempWavefun = np.exp(-1j*V*timestep/(2*hbarev))*TempWavefun
    return TempWavefun

def calculateProbabilityCurrent(wavefun, k):
    dwavefun = deriveOne(wavefun, k)
    cwavefun = np.conj(wavefun)
    cdwavefun = np.conj(dwavefun)
    j = hbar/(2*me*1j) * (cwavefun*dwavefun - wavefun*cdwavefun)
    return j

def deriveOne(wavefun, k):
    wavefun = np.fft.ifft(1j*k*np.fft.fft(wavefun))
    return wavefun

def potentialExpectation(wavefun, potential, dx):
    norm = np.sum(wavefun*np.conj(wavefun)*dx)**0.5
    wavefun = wavefun / norm
    Vexp = np.sum(wavefun*np.conj(wavefun)*potential*dx)
    return Vexp

def initialMomentum(totalEnergy, wavefun, potential, dx, sigma, L, x0):
    Vexp = np.real(potentialExpectation(wavefun, potential, dx))
    kineticEnergy = totalEnergy - Vexp
    A = np.sum(wavefun*np.conj(wavefun)*dx)
    k0 = Symbol('k0')
    k0 = solve(zFromGauss(k0,L,x0,sigma,kineticEnergy,A),k0)
    return k0

def zFromGauss(k0, L, x0, dx, kineticEnergy, A):
    x0 = x0 * 1e-10
    L = L * 1e-10
    dx = dx * 1e-10
    kineticEnergy = kineticEnergy
    sp = np.sqrt(np.pi)
    Lpart = (L-x0)/dx
    xpart = x0/dx
    erfpart = erf(Lpart) - erf(-xpart)
    expL = np.exp(-Lpart**2)
    expx0 = np.exp(-xpart**2)
    expLL = Lpart*expL
    expxx0 = xpart*expx0
    return -hbark**2/(2*me*A) * (1/(4*dx) * (sp*erfpart - 2*expLL - 2*expxx0) - 1j*k0*(expx0 - expL) - sp*dx/2*(k0**2 + 1/dx**2)*erfpart) - kineticEnergy
    #return (hbark**2/(2*me))*(A**2)*(1/(4*dx**2))*((1+2*dx**2*k0**2)*sp*dx*(erf(x0/dx)+erf((L-x0)/dx)) + 2*np.exp(-(x0/dx)**2)*(x0+2*1j*k0*dx**2) + 2*np.exp(-((L-x0)/dx)**2)*(L-x0-2*1j*k0*dx**2))

def cumulativeProb(wavefun, x, xcutoff, dx):
    xAxis = x >= xcutoff
    cutwavefun = wavefun[xAxis]
    cumProb = np.sum(cutwavefun*np.conj(cutwavefun)*dx)
    return cumProb