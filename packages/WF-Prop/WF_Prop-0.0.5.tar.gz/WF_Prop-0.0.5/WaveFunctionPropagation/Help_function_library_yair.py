# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:17:17 2021
@author: Yair Reichman
"""
import numpy
from numpy.random import Generator, PCG64
import sys, os
import numpy as np
import sympy as smp
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sympy import I, oo, integrate, conjugate, lambdify, exp, sin, cos
import math
import scipy.special as nps
from scipy.fft import fft, ifft, fftfreq, fft2, ifft2, fftshift, ifftshift
from scipy.interpolate import PchipInterpolator as pchip
from scipy.stats import linregress as lin_reg
from scipy.optimize import curve_fit as cfit
from scipy.signal import peak_widths
from scipy.integrate import quad, cumulative_trapezoid
from scipy.interpolate import interp1d
from Locpot_class import *
from matplotlib.ticker import FormatStrFormatter
from pymatgen.io.vasp.outputs import Locpot
from pymatgen.core.structure import Structure, Lattice
from itertools import permutations
import scipy.signal as ss
from savitzky_golay import *
from Locpot_class import *

class Constants:
    '''
    A class that aims to handle constants and unit conversion.
    Sometimes it implemented as an instance attribute, and it appears at the initiation function, then
    it can be called as : <instance>.cons
    Other times it imported as an outer scope instance of the Constants class and then treated as
    just a class varibale.
    '''
    def __init__(self, eVA=False):
        self.hbareV = 6.58212e-16  # [eV*s/rad]or
        self.hbarJ = 6.62607e-34 / (2 * np.pi)  # [J*sec/rad]
        self.me = 9.10938e-31  # [kg] electron mass
        self.qe = 1.6021766e-19  # electron charge[]
        self.eVA = eVA

    def set_eVA(self, eVA):
        self.eVA = eVA

    def eV2J(self, ener_value):
        '''
        Parameters
        ----------
        ener_value : float
            gets energy value in eV.
        Returns
        -------
        Float
            returns energy value in J.
        '''
        types = [int, float, np.float64, np.int64]
        if not type(ener_value) in types:
            a = np.real(ener_value[-1])
        else:
            a = np.real(ener_value)
        if a < 0:
            if not np.log(-a) < -16:
                return np.float64(np.real(ener_value) * 1.6021765e-19)
            else:
                return np.float64(np.real(ener_value))
        else:
            if not np.log(a) < -16:
                return np.float64(np.real(ener_value) * 1.6021765e-19)
            else:
                return np.float64(np.real(ener_value))

    def J2eV(self, ener_value):
        '''
        Parameters
        ----------
        ener_value : float
            gets energy value in J.
        Returns
        -------
        Float
            returns energy value in eV.
        '''
        types = [int, float, np.float64, np.int64]
        if not type(ener_value) in types:
            a = np.real(ener_value[-1])
        else:
            a = np.real(ener_value)
        if a < 0:
            if np.log(-a) < -16:
                return np.float64(np.real(ener_value) * 6.241509596e+18)
            else:
                return np.float64(np.real(ener_value))
        else:
            if np.log(a) < -16:
                return np.float64(np.real(ener_value) * 6.241509596e+18)
            else:
                return np.float64(np.real(ener_value))

    def A2m(self, conver_value):
        '''
        Parameters
        ----------
        conver_value : float
            Gets metric value in A.
        Returns
        -------
        float
            returns metric value in m.
        '''
        types = [int, float, np.float64, np.int64]
        if not type(conver_value) in types:
            a = conver_value[-1]
        else:
            a = conver_value
        if a < 0:
            if not np.log(-a) < -16:
                return np.float64(conver_value * 1e-10)
            else:
                return np.float64(conver_value)
        else:
            if not np.log(a) < -16:
                return np.float64(conver_value * 1e-10)
            else:
                return np.float64(conver_value)

    def m2A(self, conver_value):
        '''
        Parameters
        ----------
        conver_value : float
            Gets metric value in m.
        Returns
        -------
        float
            returns metric value in A.
        '''
        types = [int, float, np.float64, np.int64]
        if not type(conver_value) in types:
            a = conver_value[-1]
        else:
            a = conver_value
        if a < 0 :
            if np.log(-a) < -16:
                return np.float64(conver_value * 1e+10)
            else:
                return np.float64(conver_value)
        else:
            if np.log(a) < -16:
                return np.float64(conver_value * 1e+10)
            else:
                return np.float64(conver_value)

    def sec2fs(self, conver_value):
        types = [int, float, np.float64, np.int64]
        if not type(conver_value) in types:
            a = conver_value[-1]
            a = np.float64(a)
        else:
            a = conver_value
            a = np.float64(a)
        if a < 0:
            if np.log(-a) < -23:
                return np.float64(conver_value * 1e+15)
            else:
                return np.float64(conver_value)
        else:
            if np.log(a) < -23:
                return np.float64(conver_value * 1e+15)
            else:
                return np.float64(conver_value)

    def fs2sec(self, conver_value):
        types = [int, float, np.float64, np.int64]
        if not type(conver_value) in types:
            a = conver_value[-1]
            a = np.float64(a)
        else:
            a = conver_value
            a = np.float64(a)
        if a < 0:
            if not np.log(-a) < -23:
                return np.float64(conver_value * 1e-15)
            else:
                return np.float64(conver_value)
        else:
            if not np.log(a) < -23:
                return np.float64(conver_value * 1e-15)
            else:
                return np.float64(conver_value)


# Here is an example for an outter scope varibale of Constants class instance
# that will be used along this document.
cons = Constants()

def to_1D_vec(vec):
    '''
    Parameters
    ----------
    vec : np.array
        This method enforce any 1D vector in any form into the shape of 1D vector in the shpae of (n,)
        while n is the number of rows. Pay attention that there is no another axis, and all opertations
        such as tranpose does not take any action on the resulted vector.
    Returns
    -------
    np.array
        The original vector in a form of a 1D vector.
    '''
    types = [int, float, np.float64, np.int64]
    if not type(vec) in types and not len(vec) <= 1:
        vec = np.squeeze(vec)
    if len(np.shape(vec)) >= 2:
        print('You have another not negligible axis')
    return vec

def find_peak_half_max_width(locpot_vec):
    '''
    Parameters
    ----------
    locpot_vec : `numpy.ndarray`, (N,2)
        Gets a 2d matrix with two columns represents [:,0] = positions\coords,
        and [:,1] represents the potential values (v(z)).
    Returns
    -------
    flaot
        It returns the average width of the peaks.
    '''
    peaks = np.column_stack((locpot_vec[:, 0], locpot_vec[:, 1]))
    allmax = find_peaks_maxima(locpot_vec[:, 0], locpot_vec[:, 1],ignore_local_maxima=True)
    maxima = [i for i in range(len(peaks[:, 0])) if peaks[:, 0][i] in allmax[:, 0]]
    widths = peak_widths(np.float64(peaks[:, 1]), maxima, rel_height=0.5)
    wid = cons.A2m(widths[0]) / 10
    dz = np.average(wid)
    return np.average(wid)

def to_column_vec(vec):
    '''
    As oppose the to_1D_vec method, this function do the opposite, it
    enforce any 1D or a column vector into column vector in the form (n,1)
    where n is the number of rows. Pay attention that here we hve addtitonal
    axis where we can perform an actions like traspose.
    Parameters
    ----------
    vec : np.array
        The original vector we wish convert into a column vector
    Returns
    -------
    np.array
        The original vector in a form of a coulmn vector.
    '''
    vec = np.squeeze(vec)
    if len(np.shape(vec)) <= 1:
        vec = vec[np.newaxis]
    if np.shape(vec)[0] < np.shape(vec)[1]:
        vec = vec.T
    return vec

def to_row_vec(vec):
    '''
    Similar to to_column_vec but it enforces the original vector into
    a row vector of the form (1,n) where n is the number of columns here.
    Parameters
    ----------
    vec : np.array
        The original vector we wish convert into a row vector
    Returns
    -------
    np.array
        The original vector in a form of a row vector.
    '''
    vec = np.squeeze(vec)
    if len(np.shape(vec)) <= 1:
        vec = vec[np.newaxis]
    if np.shape(vec)[0] > np.shape(vec)[1]:
        vec = vec.T
    return vec

def find_peaks(x, y, to_plot= False, dist = None):
    """
    Parameters
    ----------
    x : np.array, array_like
        The Spatial coordinates vector.
    y : np.array, array_like
       The functional values of the spatial coordiantes vector. The definiion for `f(x) = y`. Usually will be the local potential vector.
    to_plot : bool, optional, default: False
        Flag that determines whether to enable plotting or not.
    dist : float, optional, default: None
        The distance between peaks.
    Returns
    -------
    `numpy.ndarray`
        It returns a matrix of two columns. The first column is for the peaks position, and the second column is for and their heights. It also can plot.
    """

    x = np.asarray(np.float64(x))
    y = np.asarray(np.float64(y))
    global_max_y = np.max(y)
    global_min_y = np.min(y)
    y2 = y * -1
    if not dist is None:
        minima = ss.find_peaks(y2,prominence=0.2 ,distance=dist)
    else:
        minima = ss.find_peaks(y2,prominence=0.2 )
    min_pos = x[minima[0]]  # list of the minima positions
    min_height = y2[minima[0]]  # list of the mirrored minima heights

    if not dist is None:
        peaks = ss.find_peaks(y, height=[global_min_y - 0.5, global_max_y + 0.5],prominence=0.2 , distance=dist)
    else:
        peaks = ss.find_peaks(y, height=[global_min_y - 0.5, global_max_y + 0.5],prominence=0.2 )
    height = peaks[1]['peak_heights']  # list of the heights of the peaks
    peak_pos = x[peaks[0]]  # list of the peaks positions

    peaks_array_pos = np.append(peak_pos, min_pos)
    peaks_array_pos = np.sort(peaks_array_pos)
    peaks_array_height = np.append(minima[0], peaks[0])
    peaks_array_height = np.sort(peaks_array_height)
    peaks_array_height = y[peaks_array_height]
    peaks_array = np.column_stack([peaks_array_pos, peaks_array_height])
    peaks_array = to_2_column_mat(peaks_array)
    if to_plot:
        fig = plt.figure()
        ax = fig.subplots()
        ax.plot(x, y)
        ax.scatter(peaks_array_pos, peaks_array_height, color='r', s=15, marker='D', label='peaks')
        ax.grid()
        ax.legend()
        plt.show()

    return peaks_array

def find_peaks_maxima(x, y, ignore_local_maxima = False, to_plot = False, prominence = None):
    '''
    Parameters
    ----------
    x : np.array, array_like
        spatial coordinates vector.
    y : np.array, array_like
        Potential values v(z) vector.
    ignore_local_maxima : bool, optional, default: False
        It enables to turn on the option to ignore local maxima points.
    to_plot : bool, optional, default: False
        Flag that determines whether to enable plotting or not.
    prominence : float, optional, the default is None
        Input to detemine the prominence threshold for the find_peak.
    Returns
    -------
    `numpy.ndarray`
        It returns a matrix of the maximum peaks. The first column is the maximum peaks position. The second column is the
        maximum peaks height. It also can plot.
    '''

    x = np.asarray(np.float64(x))
    y = np.asarray(np.float64(y))
    flag_x = np.all(x == cons.m2A(x))
    flag_y = np.all(y == cons.J2eV(y))
    x = cons.m2A(x)
    y = cons.J2eV(y)
    window = len(y)
    window = window*0.0000001
    while np.fix(window) < 10:
        window *=10
    iteration = 0
    while iteration < 100:
        if np.mod(np.fix(window), 2) == 0:
            try:
                y_temp = savitzky_golay(y, window_size=np.fix(window) + 1, order=4)
            except:
                y_temp = np.ones(len(y))

            if r_sqrd(y, y_temp) >= 0.85:
                y = y_temp
                break
            else:
                if iteration == 0:
                    window = 1.0
                else:
                    window += 2
        else:
            try:
                y_temp = savitzky_golay(y, window_size=np.fix(window), order=4)
            except:
                y_temp = np.ones(len(y))
            if r_sqrd(y, y_temp) >= 0.85:
                y = y_temp
                break
            else:
                if iteration == 0:
                    window = 1.0
                else:
                    window += 2
        iteration +=1
    global_max_y = np.max(y)
    global_min_y = np.min(y)
    if not ignore_local_maxima:
         maxima = ss.find_peaks(y, height=[global_min_y - 0.5, global_max_y + 0.5], prominence=0.1)

    else:
        maxima_temp = ss.find_peaks(y,prominence=0.1)
        if prominence is None:
            promin = ss.peak_prominences(y, maxima_temp[0])
            peaks_1 = ss.find_peaks(promin[0])
            if len(peaks_1[0]) == 0:
                temp_flag = True
                for i in range(len(y[maxima_temp[0]])-1):
                    if not np.abs(y[maxima_temp[0]][i] - y[maxima_temp[0]][i+1]) <= 0.12:
                        temp_flag = False
                if temp_flag:
                    try:
                        promin_max = np.min(promin[0])
                    except ValueError:
                        if promin[0] is None or len(promin[0]) == 0:
                            promin_max = 0.1
                        else:
                            raise  ValueError('Chceck Your input vectors')
                else:
                    try:
                         promin_max = np.max(promin[0])-0.2
                    except ValueError:
                        if promin[0] is None or len(promin[0]) == 0:
                            promin_max = 0.1
                        else:
                            raise  ValueError('Chceck Your input vectors')
            else:
                promin_max = promin[0][peaks_1[0]]
            maxima = ss.find_peaks(y, prominence=np.min(promin_max)- 0.2 )
        else:
            maxima = ss.find_peaks(y, prominence=prominence - 0.2)
    if not flag_x:
        maxima_pos = cons.A2m(x[maxima[0]])  # list of the minima positions
    else:
        maxima_pos = x[maxima[0]]  # list of the minima positions
    if not flag_y:
        max_height = cons.eV2J(y[maxima[0]])  # list of the mirrored minima heights
    else:
        max_height = y[maxima[0]]  # list of the mirrored minima heights
    peaks_array = np.column_stack([maxima_pos, max_height])

    return peaks_array

def get_prominence(z,v,num_of_min = None,is_max = False):
    '''
    Parameters
    ----------
    z : np.array, array_like
        The spatial coordinates vector.
    v : np.array, array_like
       The potential values (v(z)) vector
    num_of_min : int, optional, default : None
        Input to detemine how many kind of minima's we have in our system.
    is_max : bool, optional, default : None
    Returns
    -------
    `int`
        The prominence of out system regarding the main number of minima's.
    '''
    if not is_max:
        v = -1*v
    else:
        pass
    flag_y = np.all(v == cons.J2eV(v))
    if not flag_y:
        v = cons.J2eV(v)
    minima_temp = ss.find_peaks(v)
    promin = ss.peak_prominences(v, minima_temp[0])
    peaks_1 = ss.find_peaks(promin[0])

    if len(peaks_1[0]) == 0:
        temp_flag = True
        for i in range(len(v[minima_temp[0]]) - 1):
            if not np.abs(v[minima_temp[0]][i] - v[minima_temp[0]][i + 1]) <= 0.12:
                temp_flag = False
        if temp_flag:
            promin_max = np.min(promin[0])
        else:
            if type(promin_max) in [float, np.float64]:
                promin_max = np.sort(np.array([promin[0]]))[::-1]
            else:
                promin_max=np.sort(promin_max)[::-1][0]

    else:
        promin_max = promin[0][peaks_1[0]]

    try:
        if num_of_min is None:
            if type(promin_max) in [float, np.float64]:
                promin_max = np.sort(np.array([promin_max]))[::-1][0]
            else:
                promin_max=np.sort(promin_max)[::-1][0]
        elif num_of_min == -1:
            promin_max = np.min(promin_max)
        else:
            if type(promin_max) in [float, np.float64]:
                promin_max = np.sort(np.array([promin_max]))[::-1][0]
            else:
                promin_max = np.sort(promin_max)[::-1][0]
    except IndexError:
        print('you had an issue with the promincence')
        if not flag_y:
            promin_max = cons.eV2J(3)
        else:
            promin_max = 3
    if not flag_y:
        return cons.eV2J(promin_max)
    else:
        return promin_max

def find_peaks_minima(x, y, ignore_local_minima = False,to_plot = False, prominence=None):
    '''
    Parameters
    ----------
    x : np.array, array_like
        The spatial coordinates vector.
    y : np.array, array_like
       The potential values (v(z)) vector
    ignore_local_minima : bool, optional, default: False
       It enables to turn on the option to ignore local minima points.
    to_plot : bool, optional, default: False
        This is a flag that determines whether to enable plotting or not.
    prominence : float, optional, the default is None
        Input to detemine the prominence threshold for the find_peak.
    Returns
    -------
    `numpy.ndarray`
        It returns a matrix of the minimum peaks. The first column is the minimum peaks position. The second column is the
        minimum peaks height. It also can plot.
    '''

    if type(x) == list:
        x = np.asarray(np.float64(x))
    if type(y) == list:
        y = np.asarray(np.float64(y))
    flag_x = np.all(x == cons.m2A(x))
    flag_y = np.all(y == cons.J2eV(y))
    x = cons.m2A(x)
    y = cons.J2eV(y)
    window = len(y)
    window = window*0.0000001
    while np.fix(window) < 10:
        window *=10
    iteration = 0
    while iteration < 100:
        if np.mod(np.fix(window),2) == 0:
            try:
                y_temp = savitzky_golay(y, window_size= np.fix(window) +1, order=4)
            except:
                y_temp = np.ones(len(y))

            if r_sqrd(y,y_temp) >= 0.85:
                y = y_temp
                break
            else:
                if iteration == 0 :
                    window = 1.0
                else:
                    window +=2
        else:
            try:
                y_temp = savitzky_golay(y, window_size=np.fix(window) , order=4)
            except:
                y_temp = np.ones(len(y))
            if r_sqrd(y,y_temp) >= 0.85:
                y = y_temp
                break
            else:
                if iteration == 0 :
                    window = 1.0
                else:
                    window +=2
        iteration +=1
    y2 = y * -1
    global_min_y = np.min(y)


    if not flag_y:
        y = cons.J2eV(y)
        y2 = y * -1
    if not ignore_local_minima:
        if flag_y:
            minima = ss.find_peaks(y2,prominence=0.1)
        else:
            minima = ss.find_peaks(y2, prominence=cons.eV2J(0.1))
    else:
        minima_temp = ss.find_peaks(y2,prominence=0.1)
        if prominence is None:
            promin = ss.peak_prominences(y2,minima_temp[0])
            peaks_1 = ss.find_peaks(promin[0])

            if len(peaks_1[0]) == 0:
                temp_flag = True
                for i in range(len(y[minima_temp[0]]) - 1):
                    if not np.abs(y[minima_temp[0]][i] - y[minima_temp[0]][i + 1]) <= 0.12:
                        temp_flag = False
                if temp_flag:
                    try:
                        promin_max = np.min(promin[0])
                    except ValueError:
                        if promin[0] is None or len(promin[0]) == 0:
                            promin_max = 0.1
                        else:
                            raise ValueError('Chceck Your input vectors')
                else:
                    try:
                        promin_max = np.max(promin[0])-0.2
                    except ValueError:
                        if promin[0] is None or len(promin[0]) == 0:
                            promin_max = 0.1
                        else:
                            raise ValueError('Chceck Your input vectors')
            else:
                promin_max = promin[0][peaks_1[0]] - 0.2

            minima = ss.find_peaks(y2, prominence=np.min(promin_max))
        else:
            minima = ss.find_peaks(y2, prominence=prominence-0.2)
    if not flag_x:
        min_pos = cons.A2m(x[minima[0]])  # list of the minima positions
    else:
        min_pos = x[minima[0]]  # list of the minima positions
    if not flag_y:
        min_height =cons.eV2J( -1 * y2[minima[0]])  # list of the mirrored minima heights
    else:
        min_height = -1 * y2[minima[0]]  # list of the mirrored minima heights

    # peaks = ss.find_peaks(y,height = [global_min_y-0.5,global_max_y+0.5])
    # height = peaks[1]['peak_heights'] #list of the heights of the peaks
    # peak_pos = x[peaks[0]] #list of the peaks positions

    # peaks_array_pos = np.array(peak_pos)
    # peaks_array_pos = np.sort(peaks_array_pos)
    # peaks_array_height = np.array(peaks[0])
    # peaks_array_height = np.sort(peaks_array_height)
    # peaks_array_height = y[peaks_array_height]
    peaks_array = np.column_stack([min_pos, min_height])

    if to_plot:
        fig = plt.figure()
        ax = fig.subplots()
        ax.plot(x, y)
        ax.scatter(min_pos, min_height, color='r', s=15, marker='D', label='peaks')
        ax.grid()
        ax.legend()
        plt.show()

    return peaks_array

def create_k_grid(N, L, dimention='1D'):
    '''
    Parameters
    ----------
    N : int/float
        The number of measuerment sample. The number of the k-grid points.
    L : int/float
         The actual length of the system. Should be given in units of [m].
    dimention : str, {'1D', '2D'}, optional, default: '1D'
        The choices are in the brackets. It defines the K-grid for 1D or 2D mesh.
    Returns
    -------
    K grid vector. Column vector. (numpy array with a shape of (N,1))
    '''

    if dimention == '1D':
        deltak = (2 * np.pi) / L
        if np.mod(N, 2) == 1:  # N is odd
            kk2_indice = np.arange((-(N - 1) / 2), 0, 1)
            kk1_indice = np.arange(0, (((N - 1) / 2) + 1), 1)
            kk2 = kk2_indice * deltak
            kk1 = kk1_indice * deltak
            # kk = np.append(kk1,kk2) # this is in the case that x=[-L/2,L/2] and not as it is in our case: L=[0,L]
        else:  # N is even
            kk2_indice = np.arange((-N / 2), 0, 1)
            kk1_indice = np.arange(0, (N / 2), 1)
            kk2 = kk2_indice * deltak
            kk1 = kk1_indice * deltak
        kk = np.append(kk1, kk2)

        assert len(kk) == N, 'length of N = {} and length of kk {}'.format(N, len(kk))
        kk = kk[np.newaxis]
        if np.shape(kk)[0] < np.shape(kk)[1]:
            kk = kk.T
        return kk

    elif dimention == '2D':
        print('yet to be programmed')
    else:
        print('The input should be relating the dimentions order as "1D"\
              for 1 dimention and as "2D" for the two dimentions')
        return None

def normalize_wave_function_numerically(z,wave_function, units = 'Meter'):
    '''
    Parameters
    ----------
    z : np.array, array_like
        The spatial coordinates vector where the wave function spreads.
    wave_function : np.array, array_like
        The complex values of the wave function in at the relevant z positions.
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    A : flaat
        The numeric normaliztion factor.
    '''
    wave_function = force_psi_units(wave_function,units=units)
    max_1 = np.max(np.real(wave_function))
    if units == 'Meter':
        z = to_1D_vec(z)
        z = cons.A2m(z)
        if np.log10(max_1) > 9:
            wave_function = to_1D_vec(wave_function) * 1E-5
        elif np.log10(max_1) <= 3.65:
             wave_function = to_1D_vec(wave_function) * 1E5
        else:
            wave_function = to_1D_vec(wave_function)
        integral = np.real(np.trapz(wave_function * np.conj(wave_function), z))
        A = np.real(1 / np.sqrt(integral))
    elif units == 'Angstrum':
        z = to_1D_vec(z)
        z = cons.m2A(z)
        if np.log10(max_1) > 9:
             wave_function =  to_1D_vec(wave_function) * 1E-10
        elif np.log10(max_1) >= 3.65:
             wave_function =  to_1D_vec(wave_function) * 1E-5
        else:
            wave_function =  to_1D_vec(wave_function)
        integral = np.real(np.trapz(wave_function * np.conj(wave_function), z))
        A = np.real(1 / np.sqrt(integral))
    else:
        print('Please enter the units correctly.')
    return A

def normalize_wave_function(wave_equation, bound_up=np.inf, bound_down=0, units = 'Meter'):
    '''
    Parameters
    ----------
    wave_equation : lambda
        It is in a lambda function format. It can be a static function or a lambda state.
        The equation of the wave function we wish to normalize. In this project, mainly supplied as
        a gaussian wave function.
    bound_up : int/float, optional, default: smp.oo
        The intgration boundaries. (default = inifinity)
    bound_down : int/float, optional, default: -smp.oo
        The intgration boundaries. (default = -inifinity)
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    A : int/float
        The normalization factor. Where psi(x) = A*f(x) -> it returns A.
    '''
    integrand_real = lambda z: np.real(wave_equation(z) * np.conj(wave_equation(z)))
    integrand_img = lambda z: np.imag(wave_equation(z) * np.conj(wave_equation(z)))
    val_int_real = quad(integrand_real, bound_down, bound_up)[0]
    val_int_img = quad(integrand_img, bound_down, bound_up)[0]
    integral_val = val_int_real + 1j * val_int_img
    A = np.real(1 / np.sqrt(integral_val))
    if units == 'Meter':
        if np.log10(A) > 9:
            A = A  * 1E-5
        elif np.log10(A) <= 3.65:
            A = A * 1E5
    elif units == 'Angstrum':
        if np.log10(A) > 9:
            A = A  * 1E-10
        elif np.log10(A) >= 3.65:
            A = A * 1E-5
    return A

def normalize_wave_function_sym(wave_equation, bound_up=smp.oo, bound_down=0, units = 'Meter'):
    '''
    Parameters
    ----------
    wave_equation : lambda
        It is in a lambda function format. It can be a static function or a lambda state.
        The equation of the wave function we wish to normalize. In this project, mainly supplied as
        a gaussian wave function.
    bound_up : int/float, optional, default: smp.oo
        The intgration boundaries. (default = inifinity)
    bound_down : int/float, optional, default: -smp.oo
        The intgration boundaries. (default = -inifinity)
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    A : float
        The symbolic normaliztion factor.
    '''

    x = smp.symbols('x', real=True)
    integrand_real = smp.re(wave_equation * smp.conjugate(wave_equation))
    integrand_img = smp.im(wave_equation * smp.conjugate(wave_equation))
    val_int_real = smp.integrate(integrand_real, (x, bound_down, bound_up))
    val_int_img = smp.integrate(integrand_img, (x, bound_down, bound_up))
    integral_val = val_int_real + 1j * val_int_img
    A = smp.re(1 / smp.sqrt(integral_val))
    A = np.float64(A)
    if units == 'Meter':
        if np.log10(A) > 9:
            A = A  * 1E-5
        elif np.log10(A) <= 3.65:
            A = A * 1E5
    elif units == 'Angstrum':
        if np.log10(A) > 9:
            A = A  * 1E-10
        elif np.log10(A) >= 3.65:
            A = A * 1E-5
    return A

def is_normalized(z, psi_values,units = 'Meter'):
    '''
    Parameters
    ----------
    z : np.array, array_like
        The spatial coordinates the wave function is specified at.
    psi_values : np.array, array_like
        The wavefunction values along the spatial coordinates. Must suit the units for angstrums.
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    bool
        It checks if the wave function is normalized, True if it does, atherwise it returns False.
        It performs numerical integrarion and checks if it to be equal to 1.
    '''
    max_1 = np.max(np.real(psi_values))
    if units == 'Meter':
        if np.log10(max_1) > 9:
             x, y = to_1D_vec(cons.A2m(z)), to_1D_vec(psi_values) * 1E-5
        elif np.log10(max_1) <= 3.65:
             x, y = to_1D_vec(cons.A2m(z)), to_1D_vec(psi_values) * 1E5
        else:
            x, y = to_1D_vec(cons.A2m(z)), to_1D_vec(psi_values)
    elif units == 'Angstrum':
        if np.log10(max_1) > 9:
             x, y = to_1D_vec(cons.m2A(z)), to_1D_vec(psi_values) * 1E-10
        elif np.log10(max_1) >= 3.65:
             x, y = to_1D_vec(cons.m2A(z)), to_1D_vec(psi_values) * 1E-5
        else:
            x, y = to_1D_vec(cons.m2A(z)), to_1D_vec(psi_values)
    else:
        return None
    integral = np.real(np.trapz(y * np.conj(y), x))
    if 0.95 <= integral <= 1.05:
        return True
    else:
        return False

def gaussian_function_sym( k0, sigma, z0, dimention='1D', A=None):
    '''
    Parameters
    ----------
    k0 : float
        The initial momentum value,
    sigma : float
        The standard devaiation of the gaussian wave-function.
    z0 : float
        Initial poisition where the wave function is centered at.
    dimention : str, {'1D', '2D'}, optional, default: '1D'
        The choices are in the brackets. It defines the K-grid for 1D or 2D mesh.
    A : float, optional, default: None
        If we already calculated the normaliztion factor we can supply it here.
        Otherwise it calculate from scratch here.
    Returns
    -------
    lambda
        It returns a symbolic expression of the wavefunction, in lambda format.
    '''
    x = smp.symbols('x', real=True)
    if A is None:
        # return np.exp(-(((x-z0)**2)/(2*(sigma**2)))+1j*k0*x)
        return smp.exp(1j * k0 * x) * smp.exp(-0.5 * (((x - z0) / sigma) ** 2))
    else:
        return A * smp.exp(-(((x - z0) ** 2) / (2 * (sigma ** 2))) + 1j * k0 * x)

def gaussian_function(x, k0, sigma, z0, dimention='1D', A=None):
    '''
    Parameters
    ----------
    x : np.array
        The spatial coordinates vector.
    k0 : float
        The initial momentum value,
    sigma : float
        The standard devaiation of the gaussian wave-function.
    z0 : float
        Initial poisition where the wave function is centered at.
    dimention : str, {'1D', '2D'}, optional, default: '1D'
        The choices are in the brackets. It defines the K-grid for 1D or 2D mesh.
    A : float, optional, default: None
        If we already calculated the normaliztion factor we can supply it here.
        Otherwise it calculate from scratch here.
    Returns
    -------
    np.array
        The wave function vector.
    '''
    if A is None:
        # return np.exp(-(((x-z0)**2)/(2*(sigma**2)))+1j*k0*x)
        return np.exp(1j * k0 * x) * np.exp(-0.5 * (((x - z0) / sigma) ** 2))
    else:
        return A * np.exp(-(((x - z0) ** 2) / (2 * (sigma ** 2))) + 1j * k0 * x)

def get_psi0(k0, sigma, z0, z, dimention='1D', sqrd_psi=False,units= 'Meter'):
    '''
    Parameters
    ----------
    k0 : float
        The initial momentum value,
    sigma : float
        The standard devaiation of the gaussian wave-function.
    z0 : float
        Initial poisition where the wave function is centered at.
    dimention : str, {'1D', '2D'}, optional, default: '1D'
        The choices are in the brackets. It defines the K-grid for 1D or 2D mesh.
    sqrd_psi : bool, optional, default: False
        It gives an optiona to return also the absolute sqrd of the wave function.
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    np.array, np.array
        The first vector represents the spatial coordinates grid
        and the second vector represnts the wave function value at this position. the values are complex numbers.
    '''
    if dimention == '1D':
        z0 = cons.m2A(z0)
        sigma = cons.m2A(sigma)
        k0 = cons.A2m(k0)
        z = cons.m2A(z)
        wave_function = lambda z: gaussian_function(z, k0, sigma, z0, dimention='1D')
        A = normalize_wave_function(wave_function,bound_up=z[-1],units=units)
        if units == 'Angstrum':
            wave_function = lambda z: gaussian_function(z, k0, sigma, z0, dimention='1D')
            psi0 = np.vectorize(wave_function)(z)
            # if not np.abs(np.abs(np.average(np.real(psi0[0:5]))) - np.abs(np.average(np.real(psi0[-6:-1])))) < 1E-5:
            #     print('Your wave fucntion is not symmetric in the given range')
            if not sqrd_psi:
                if is_normalized(z, A * psi0,units=units):
                    return z, A * psi0
                else:
                    A = normalize_wave_function_numerically(z, psi0, units=units)
                    return z, A * psi0
            else:
                if is_normalized(z, A * psi0, units=units):
                    return z, A * psi0, (A ** 2) * psi0 * np.conj(psi0)
                else:
                    A = normalize_wave_function_numerically(z, psi0, units=units)
                    return z, A * psi0, (A ** 2) * psi0 * np.conj(psi0)
        elif units == 'Meter':
            z0 = cons.A2m(z0)
            sigma = cons.A2m(sigma)
            k0 = k0 * 1E10
            z = cons.A2m(z)
            wave_function = lambda z: gaussian_function(z, k0, sigma, z0, dimention='1D')
            psi0 = np.vectorize(wave_function)(z)

            # if not np.abs(np.abs(np.average(np.real(psi0[0:5]))) - np.abs(np.average(np.real(psi0[-6:-1])))) < 1E-5:
            #     print('Your wave fucntion is not symmetric in the given range')
            if not sqrd_psi:
                if is_normalized(z, A * psi0, units=units):
                    return z, A * psi0
                else:
                    A = normalize_wave_function_numerically(z, psi0, units=units)
                    return z, A * psi0
            else:
                if is_normalized(z, A * psi0, units=units):
                    return z, A * psi0, (A ** 2) * psi0 * np.conj(psi0)
                else:
                    A = normalize_wave_function_numerically(z, psi0, units=units)
                    return z, A * psi0, (A ** 2) * psi0 * np.conj(psi0)
    elif dimention == '2D':
        print('yet to be programmed')
    else:
        print('The input should be relating the dimentions order as "1D"\
              for 1 dimention and as "2D" for the two dimentions')

def get_first_derivative_fft(x, y, L=None):
    '''
    Parameters
    ----------
    x : np.array
        The spatial coordinates vector.
    y : np.array
        The appropriate function-values corresponds the spatial coordinates vector.
    L : float, optional, default: None
        It should be supplied with the length of the system. It stands for the creation of the K-grid vector.
    Returns
    -------
    np.array, np.array
        It returns the spatial coordinates vector and the first derivative vecotr.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    if L is None:
        if x[0] < 0:
            L = x[-1] - x[0]
        elif x[0] == 0:
            L = x[-1]
    N = len(x)
    k = create_k_grid(N, L)
    k = to_column_vec(k)
    fft_x = fft(y)
    fft_x = to_column_vec(fft_x)
    fft_x_k = (1j * k * fft_x)
    fft_x_k = to_1D_vec(fft_x_k)
    return x, np.real(ifft(fft_x_k))

def get_second_derivative_fft(x, y, L=None):
    '''
    Parameters
    ----------
    x : np.array
        The spatial coordinates vector.
    y : np.array
        The appropriate function-values corresponds the spatial coordinates vector.
    L : float, optional, default: None
        It should be supplied with the length of the system. It stands for the creation of the K-grid vector.
    Returns
    -------
    np.array, np.array
        It returns the spatial coordinates vector and the second derivative vecotr.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    if L is None:
        if x[0] < 0:
            L = x[-1] - x[0]
        elif x[0] == 0:
            L = x[-1]
    N = len(x)
    k = create_k_grid(N, L)
    k = to_1D_vec(k)
    fft_x = fft(y)
    fft_x = to_1D_vec(fft_x)
    fft_x_k = -(k ** 2) * fft_x
    fft_x_k = to_1D_vec(fft_x_k)
    return x, (ifft(fft_x_k))

def get_first_derivative(x, y):
    '''
    Numerical derivative
    Parameters
    ----------
    x : np.array
        The spatial coordinates vector.
    y : np.array
        The appropriate function-values corresponds the spatial coordinates vector.
    Returns
    -------
    np.array, np.array
        It returns the spatial coordinates vector and the first derivative vector.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    real_part = np.gradient(np.real(y), x)
    imag_part = np.gradient(np.imag(y), x)
    return x, (real_part + 1j * imag_part)

def get_second_derivative(x, y):
    '''
    Numerical derivative
    Parameters
    ----------
    x : np.array
        The spatial coordinates vector.
    y : np.array
        The appropriate function-values corresponds the spatial coordinates vector.
    Returns
    -------
    np.array, np.array
        It returns the spatial coordinates vector and the second derivative vector.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    real_part = np.gradient(np.gradient(np.real(y), x), x)
    imag_part = np.gradient(np.gradient(np.imag(y), x), x)
    return x, (real_part + 1j * imag_part)

def interpolate_pchip(N, *args):
    '''

    The interpolant uses monotonic cubic splines to find the value of new points.
    (PCHIP stands for Piecewise Cubic Hermite Interpolating Polynomial).

    Parameters
    ----------
    N : int/float
        It rerpesents the number of the desired samples.
    *args :  `numpy.ndarray` (N, 2)/ np.array, np.array
        It the first column is for the coords vector, and the second column is for the potential. It can handle an input
        in the form of a 2-column matrix or two different array_like arguments.

    Returns
    -------
    new_coords : np.array,(n,)
        It is the bew coords divided into the number of the N partition given as input.
    v : np.array (n,)
        It is the new potential divided into the number of the N partitiongiven as an input.
    '''
    if len(args) == 1:
        if len(np.shape(np.squeeze(args))) == 2:
            coords = np.squeeze(args)[:, 0]
            coords = to_1D_vec(coords)
            v = np.squeeze(args)[:, 1]
            v = to_1D_vec(v)
        else:
            print('check again your input')
    elif len(args) == 2:
        coords = args[0]
        coords = to_1D_vec(coords)
        v = args[1]
        v = to_1D_vec(v)
    else:
        raise TypeError('Check your input structure')
    new_coords = np.linspace(coords[0],coords[-1],N)
    new_coords = to_1D_vec(new_coords)

    try:
        v = pchip(coords, v)
        v = v.__call__(new_coords)
        v = np.squeeze(v)

    except:
        new_original_coords = np.linspace(coords[0],coords[-1],len(v))
        new_original_coords = to_1D_vec(new_original_coords)
        v = pchip(new_original_coords, v)
        v = v.__call__(new_coords)
        v = np.squeeze(v)

    if len(new_coords) == 0 or len(v) == 0:
        z = cons.m2A(coords)
        z,v = interpolate_pchip(N, new_coords,v)
        z = cons.A2m( z)
        new_coords = z
    if len(new_coords) == 0 or len(v) == 0:
        raise ValueError('Please Check your interpolation')
    return new_coords, v

def interpolate_cubic(N, *args):
    '''
    Cubic interpolation.

    Parameters
    ----------
    N : int/float
        It rerpesents the number of the desired samples.
    *args :  `numpy.ndarray` (N, 2)/ np.array, np.array
        It the first column is for the coords vector, and the second column is for the potential. It can handle an input
        in the form of a 2-column matrix or two different array_like arguments.

    Returns
    -------
    new_coords : np.array,(n,)
        It is the bew coords divided into the number of the N partition given as input.
    v : np.array (n,)
        It is the new potential divided into the number of the N partitiongiven as an input.
    '''
    if len(args) == 1:
        if len(np.shape(args[0])) == 2:
            coords = args[0][:, 0]
            coords = np.squeeze(coords)
            v = args[0][:, 1]
            v = np.squeeze(v)
        else:
            print('check again your input')
    elif len(args) == 2:
        coords = args[0]
        # coords = np.squeeze(coords)
        v = args[1]
        v = np.squeeze(v)
    new_coords = np.arange(coords[0], coords[-1], (coords[-1] / N))

    if len(coords[1:][coords[1:] - coords[:-1] == 0]) > 0:
        coords = np.linspace(coords[0], coords[-1], len(coords))
    interp_c = interp1d(coords, v, 'cubic')
    new_v = interp_c(new_coords)

    return to_1D_vec(new_coords), to_1D_vec(new_v)

def potential_expectation_nadav(psi0_values, dx, v):
    '''
    Parameters
    ----------
    psi0_values : np.array
        The wave-function values in a vector.
    dx : float
        The spatial grid spacing.
    v : np.array
        The local potential vector.
    Returns
    -------
    float
        It returns the value of the Potential Energy expectation value.
    '''
    dx = cons.A2m(dx)
    psi0 = psi0_values
    psi0 = force_psi_units(psi0,units='Meter')
    Vexp = np.sum((psi0 * np.conj(psi0)) * v * dx)
    return np.real(Vexp)

def kinetic_energy_operator(psi0_values, z, L=None):
    '''
    Parameters
    ----------
    psi0_values : np.array
        The wave-function values in a vector.
    z : float
        The spatial grid vector.
    L : float, optional, default: None
        The length of the system. if not suuplied it is calculated as
        the difference between the last value of z and its first value. L=z[-1]-z[0]
    Returns
    -------
    np.array
        It returns a vector of the results that comes after operates the kinetic energy operator on the wave-function vector.
    '''
    x = to_1D_vec(z)
    y = to_1D_vec(psi0_values)
    if L is None:
        if x[0] < 0:
            L = x[-1] - x[0]
        elif x[0] == 0:
            L = x[-1]
    N = len(x)
    k = create_k_grid(N, L)
    k = to_1D_vec(k)
    fft_x = fft(y)
    fft_x = to_1D_vec(fft_x)
    fft_x_k = (k ** 2) * ((cons.hbarJ ** 2) / (2 * cons.me)) * fft_x
    fft_x_k = to_1D_vec(fft_x_k)
    kinetic_energy_operator_vec = ifft(fft_x_k)
    kinetic_energy_operator_vec = np.squeeze(kinetic_energy_operator_vec)
    return to_column_vec(kinetic_energy_operator_vec)

def kinetic_energy_expectation_value(psi0_values, z):
    '''
    Parameters
    ----------
    psi0_values : np.array
        The wave-function values in a vector.
    z : float
        The spatial grid vector.
    Returns
    -------
    float
         It returns the value of the Kinetic Energy expectation value.
    '''
    dx = cons.A2m(np.diff(to_1D_vec(z))[0])
    T_exp = dx * to_column_vec(np.conj(psi0_values)).T @ to_column_vec(kinetic_energy_operator(psi0_values, z))
    # integrand = to_1D_vec(np.conj(psi0_values))*to_1D_vec(kinetic_energy_operator(psi0_values,z))
    # T_exp = np.trapz(integrand,to_1D_vec(z))
    if np.imag(T_exp) / np.real(T_exp) < 1E-10:
        T_exp = np.real(T_exp)
    return np.float64(np.squeeze(T_exp))

def initial_momentum_yair(sigma, E0, L, z0, A, T0):
    '''
    Parameters
    ----------
    sigma : float/int
        Standard deviation in spatial grid for the gaussin wave function.
    E0 : float/int
        Initial Energy. Usually stands for the energy value of an electorn located at the bootom of the
        conduction band.
    L : float/int
        The length of the system.
    z0 : float/int
        Initial position where the gaussian wave-packet is centered.
    A : float/int
        Normaliztion factor.
    T0 : float/int
        Initial Kinetic energy.
    Returns
    -------
    float
        The initial momentum of an electorn.
    '''
    k = smp.Symbol('k')
    eqn = ((-cons.hbarJ ** 2 / (2 * cons.me)) * (A ** 2) * (1 / (4 * (sigma ** 2)))) * \
          ((-np.pi ** 0.5) * sigma * (1 + 2 * (sigma ** 2) * (k ** 2)) * (nps.erf((L - z0) / sigma) +
                                                                            nps.erf(z0 / sigma)) + 2 * np.exp(
              -((L - z0) ** 2) / (sigma ** 2)) * (2J * (sigma ** 2) * k
                                                  - (L - z0)) - 2 * np.exp(-(z0 / sigma) ** 2) * (
                   2J * (sigma ** 2) * k + z0)) - T0

    k0 = smp.solve(eqn, k)

    flag = False
    real_sol = [0]
    for i in k0:
        if not smp.re(i) == 0:
            flag = True
            real_sol.append([smp.re(i)])
    if len(real_sol) > 0 and not (len(real_sol) == 1 and real_sol[0] == 0):
        real_sol = real_sol[1:]
    k0_for_psi = np.array([])

    if not len(real_sol) > 1:
        raise ValueError('You did not get any real solution for k0')
    for i in real_sol:
        i = i[0]
        k0_for_psi = np.append(k0_for_psi, i)
    k0_for_psi = k0_for_psi[k0_for_psi > 0]
    return np.float64(k0_for_psi[0])
    # else:
    #     print('You did not get any real solution for the value of K0, instead K0 initialized with k0=0.1e10 [1/m]. Pay attention for this.')
    #     return np.float64(10)

def find_closest_value_in_array(num, arr):
    '''
    Parameters
    ----------
    num : int/float
        The value we wish to locate in the given array.
    arr : np.array
        The array in which we wish to find the index of the closest value.
    Returns
    -------
    int, float
        It returns an index of the closest value (An integer) . And the closest value, position (a float).
    '''
    flag_num = False
    flag_arr = False
    arr = to_1D_vec(arr)
    max_in_array = np.max(arr)
    num = np.float64(num)
    if np.log10(np.abs(max_in_array)) - np.log10(np.abs(num)) <= -6:
        num = cons.A2m(num)
        flag_num = True
    elif np.log10(np.abs(num)) - np.log10(np.abs(max_in_array)) <= -6:
        arr = cons.A2m(arr)
        flag_arr = True
    dist = np.abs(arr - num)
    n = arr[dist == np.min(dist)][0]
    ind = np.where(dist == np.min(dist))[0][0]
    if flag_arr:
        return np.int64(ind), cons.m2A(n)
    else:
        return np.int64(ind), n

def to_2_column_mat(vec):
    '''
    Parameters
    ----------
    vec : `numpy.ndarray`
        The input vector we wish convert.
    Returns
    -------
    `numpy.ndarray`
        It retruns the input matrix in a form of 2 columns.
    '''
    if len(np.shape(vec)) == 2:
        if np.shape(vec)[0] == 2 and np.shape(vec)[1] == 1:
            vec = np.transpose(vec)
        elif np.shape(vec)[0] < np.shape(vec)[1] and not (np.shape(vec)[0] == 1 and np.shape(vec)[1] == 2) :
            vec = np.transpose(vec)
    elif type(vec) in [list,tuple]:
        if len(vec) == 2:
            vec = np.column_stack((np.array(vec[0]),np.array(vec[1])))
    return vec

def find_adjacent_minima_maxima(z,v,start_peak_pos,reverse = False,prominence=None):
    '''
    Very not elegnat and very complex method to find adjacent minima to maxima point in a locpot vector.

    Parameters
    ----------
    z : np.array
        The spatial coordinates vector.
    v : np.array
        The local potential vector.
    start_peak_pos : float
        The initial position where to start seaching for the minima point.
    reverse : bool, optional, default: None
        It enables to look for maxima to minima adjacent points. (The reverse order).
    prominence : float, optional, default: None
        The prominence of the peak. It helps to detemine what peaks we wish relate during the calculation.
        For more inforamtion about this mathematical entity it is recommended to look for it on web (it has to be with topology in mathematics)

    Returns
    -------
    (int, float), (int, float)
        It returns the values of the index and the position of the minima and maxima points with respect to the order in the
        reverse flag. If not supplied, the first index,position pair regards the minima point and the second index,position pair
        regards the maxima points. Otherwise - it is returned in the reveresed order. index - is an integer, and position is a float.
    '''
    maxima_global = find_peaks_maxima(z, v, ignore_local_maxima=True)
    if len(maxima_global) >= 8:
        minima_global = find_peaks_minima(z, v, ignore_local_minima=True,prominence=get_prominence(z,v,num_of_min=-1))
    else:
        minima_global = find_peaks_minima(z, v, ignore_local_minima=True)

    minima_tot = find_peaks_minima(z, v, ignore_local_minima=False)
    maxima_tot = find_peaks_maxima(z, v, ignore_local_maxima=False)
    minima_z_global = minima_global[:, 0]
    minima_v_global= minima_global[:, 1]
    maxima_z_global = maxima_global[:, 0]
    maxima_v_global = maxima_global[:, 1]
    minima_z_tot = minima_tot[:, 0]
    minima_v_tot= minima_tot[:, 1]
    maxima_z_tot = maxima_tot[:, 0]
    maxima_v_tot = maxima_tot[:, 1]

    ind_max, pos_max = find_closest_value_in_array(start_peak_pos, maxima_z_tot)
    ind_min, pos_min = find_closest_value_in_array(start_peak_pos,
                                                   minima_z_global)  # assumes that the sub-peaks are being gotten at the maxima peaks exclusively.

    if np.all(maxima_z_global == maxima_z_tot) and np.all(minima_z_tot == minima_z_global):
        if not reverse:
            return find_closest_value_in_array(minima_z_tot[minima_z_tot < maxima_z_global[-1]][-1],z) , find_closest_value_in_array(maxima_z_global[-1],z)
        else:
            if len(maxima_z_global) == 1:
                return find_closest_value_in_array(maxima_z_global[0], z), find_closest_value_in_array(
                    minima_z_tot[minima_z_tot > maxima_z_global[0]][0],
                    z)
            else:
                return find_closest_value_in_array(maxima_z_global[1], z) ,find_closest_value_in_array(minima_z_tot[minima_z_tot > maxima_z_global[1]][0],
                                                   z)
    else:

        if not reverse:
            pos_min_list = []
            while pos_min < pos_max:
                if pos_min in pos_min_list:
                    break
                if ind_min < len(minima_z_global) - 1:
                    ind_min +=1
                    pos_min_list.append(minima_z_global[ind_min])
                    pos_min =  minima_z_global[ind_min]
                else:
                    ind_min -=1
                    pos_min = minima_z_global[ind_min]
                    ind_max, pos_max = find_closest_value_in_array(pos_min, maxima_z_tot)
            dist = pos_min - pos_max
            while pos_min > pos_max and ind_max <= len(maxima_z_tot):
                ind_max +=1
                if ind_max <= len(maxima_z_tot) - 1:
                    pos_max = maxima_z_tot[ind_max]
                if dist < np.abs(pos_min - pos_max):
                    dist = pos_min - pos_max
            return  find_closest_value_in_array(pos_min,z) , find_closest_value_in_array(pos_max,z)
        else:
            pos_min_list = []
            while pos_min > pos_max :
                if pos_min in pos_min_list:
                    break
                if ind_min > 0:
                    ind_min -=1
                    pos_min_list.append(minima_z_global[ind_min])
                    pos_min =  minima_z_global[ind_min]
                else:
                    ind_min +=1
                    if ind_min >=len(minima_z_global):
                        pos_min = minima_z_global[ind_min-1]
                        pos_min_list.append(pos_min)
                    ind_max, pos_max = find_closest_value_in_array(pos_min, maxima_z_tot)
            dist =  pos_max - pos_min
            flag = True
            while pos_max > pos_min and ind_max >= 0:
                ind_max -=1
                if np.abs(ind_max) > len(maxima_z_tot):
                    pos_max = maxima_z_tot[ind_max + 1]
                    flag = False
                else:
                    pos_max = maxima_z_tot[ind_max]

                if dist < pos_max - pos_min:
                    dist =  pos_max - pos_min
                if not flag:
                    break
            return find_closest_value_in_array(pos_max,z), find_closest_value_in_array(pos_min,z)

def force_psi_units(psi, units = 'Meter'):
    '''
    Parameters
    ----------
    psi : np.array
        The vector of the wave-function values to be forced into the desired units.
    units : str, {'Meter', 'Angstrum'], optioanl, default: 'Meter'
         The choices are in the brackets. It defines the units of the normilization factor.
    Returns
    -------
    np.array
        It returns a vector of the Wave-function values in the desired units.
    '''
    max_val = np.max(np.real(np.abs(psi)))
    if units == 'Meter':
        if np.log10(max_val) > 9:
             psi =  to_1D_vec(psi) * 1E-5
        elif np.log10(max_val) <= 3.65:
             psi =  to_1D_vec(psi) * 1E5
        else:
            psi =  to_1D_vec(psi)
    elif units == 'Angstrum':
        if np.log10(max_val) > 9:
             psi =  to_1D_vec(psi) * 1E-10
        elif np.log10(max_val) >= 3.65:
             psi =  to_1D_vec(psi) * 1E-5
        else:
            psi =  to_1D_vec(psi)
    return psi

def run_one_time_step(wave_function, time_step, v, z , k):
    '''
    Parameters
    ----------
    wave_function : np.array
        Wave function values vector to be propagated.
    time_step : float
        dt. time step in which we wish perform the propagation proccess
    v : np.array
        Should be as the same size as `wave_function` vector.
        This is the local potential vector.
    z : np.array.
        Should be as the same size as `wave_function` vector.
        This is the spatial coordinates vector.
    k : np.array.
        Should be as the same size as `wave_function` vector.
        This the `k grid` axis vector.
    Returns
    -------
    np. array
        It returns a vector of the one time-step propagated wave-fucntion.
    '''
    v = cons.eV2J(v)
    z = cons.A2m(z)
    time_step = cons.fs2sec(time_step)
    wave_function = force_psi_units(wave_function,units = 'Meter')
    if not is_normalized(z,wave_function,units = 'Meter'):
        temp = np.real(np.trapz(wave_function * np.conj(wave_function), z))
        if not 0.97 <= temp <= 1.03:
            print('Psi was not normalized, Now it forces again normalization')
            print(temp)
            wave_function = wave_function * normalize_wave_function_numerically(z,wave_function,units='Meter')
    k = cons.m2A(k)
    temp_wave_function = np.exp(-1j*v * time_step/(2*cons.hbarJ)) * wave_function
    temp_wave_function = np.fft.fft(temp_wave_function)
    temp_wave_function = np.exp(-1j*cons.hbarJ * time_step * k**2 / (2 * cons.me) ) * temp_wave_function
    temp_wave_function = np.fft.ifft(temp_wave_function)
    temp_wave_function = np.exp(-1j*v * time_step/(2*cons.hbarJ)) * temp_wave_function
    temp_wave_function = force_psi_units(temp_wave_function,units='Meter')
    if not is_normalized(z,temp_wave_function,units = 'Meter'):
        temp = np.real(np.trapz(temp_wave_function * np.conj(temp_wave_function), z))
        if not 0.97 <= temp <= 1.03:
            print('Psi after propagation was not normalized, Now it forces again normalization')
            print(np.real(np.trapz(temp_wave_function * np.conj(temp_wave_function), z)))
            temp_wave_function = temp_wave_function * normalize_wave_function_numerically(z,temp_wave_function,units='Meter')
    return temp_wave_function

def calculate_probability_current(wave_function, k):
    '''
    Parameters
    ----------
    wave_function : np.array
        wave function values vector to be propagated.
    k : np.array.
        Should be as the same size as wave_function vector.
        This is the `k grid` axis vector.
    Returns
    -------
    float
        It returns the probabilty current.
    '''
    d_wave_function = fft_first_drivative(wave_function, k)
    c_wave_function = np.conj(wave_function)
    c_d_wave_function = np.conj(d_wave_function)
    j = ( cons.hbarJ / (2 * cons.me * 1j)) * ( c_wave_function * d_wave_function - wave_function * c_d_wave_function)
    return j

def fft_first_drivative(wave_function, k):
    '''
    Parameters
    ----------
    wave_function : np.array
        The wave function values vector to be propagated.
    k : np.array
        Should be as the same size as `wave_function` vector.
        This is the `k-grid` axis vector.
    Returns
    -------
    np.array
        It returns the first derivative of the wave_function
    '''
    wave_function = np.fft.ifft(1j*k*np.fft.fft(wave_function))
    return wave_function

def cumulative_probabilty(wave_function, z, z_cutoff, dz):
    '''
    Parameters
    ----------
    wave_function : np.array
        The Wave function values vector to be propagated.
    z : np.array
        The z spatial coordinates vector
    z_cutoff : float
        The maximum value of to calculate the accumulated probability.
    dz : float
        The spatial gird differnce between points.
    Returns
    -------
    float
        The `cumulative_probabilty` value up to certain ``z`` value coordinate.
    '''
    z_axis = z >= z_cutoff
    cut_wave_function = wave_function[z_axis]
    cum_probability = np.sum(cut_wave_function * np.conj(cut_wave_function) * dz)
    return cum_probability

def transmision_coeff(psi0,Nt,dt,v,z,k,z_position,path_to_save = None, final_time = None):
    '''
    Integration for the all time of simulation, summing all the probabilty currents, for each time-step in the simulation.

    Parameters
    ----------
    psi0 : np.array
        The wave function values vector.
    Nt : int
        The number of time-step that are being made.
    dt : float
        The time-step magnitude.
    v : np.array
        The local potential vector.
    z : np.array
        The spatial coordinates vector.
    k : np.array
        K grid vector.
    z_position : float
        The position at which it calculates the transimission coefficient. Should
        be given in units of Meter.
    path_to_save : string, optional, default:None
        The absolute path to save the figure obtained from the calculation
    final_time : float, optional, default:None
        The top boundary for the integration as we can integrate until this given time of the simulation. It stands for **t_f**
    Returns
    -------
    float
        It returns the calculated transmission coefficient.
    '''

    def integrate_trapz(vector, df):
        vector = np.asarray(vector, dtype=complex)
        df = np.float64(df)
        return np.real(np.float64(np.trapz(np.real(to_1D_vec(vector)), dx=df)))
    psi0 = force_psi_units(psi0, units='Meter')
    dt = cons.fs2sec(dt)
    Nt = np.int64(Nt)
    k = to_1D_vec(k)
    v = cons.eV2J(v)
    z = cons.A2m(z)
    z_position = cons.A2m(z_position)
    z_ind, z_pos  = find_closest_value_in_array(z_position, z)
    z_axis = z == z_pos
    results = np.zeros((np.int64(Nt),2),dtype=complex)
    temp_psi = np.zeros(len(psi0),dtype=complex)
    temp_psi = psi0
    print('----------------------------')
    print('----------------------------')
    print('Entering the main  propagation for the trans. Coff calculation')
    for i in range(Nt):
        if i == 0:
            results[i, :] = [i, np.squeeze(calculate_probability_current(psi0,k)[z_axis])]
            temp_psi = run_one_time_step(psi0, dt, v,z, k)
        else:
            results[i, :] = [i,  np.squeeze(calculate_probability_current(temp_psi,k)[z_axis])]
            temp_psi = run_one_time_step(temp_psi, dt, v,z, k)
        if np.mod(i,20) == 0 and i < Nt-1:
            print('++++++++++++++++++++++++++++++++++')
            print('Reached iteration {:.3f}'.format(i))
            print('++++++++++++++++++++++++++++++++++')
    gs = GridSpec(1, 1)
    fig = plt.figure(figsize=(16, 11))
    fig.suptitle(r'Cumulative Probabilty Through the interface and Transmission coefficient')
    ax = plt.subplot(gs[0])
    ax.ticklabel_format(useOffset=False, useMathText=True, style='sci')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
    ax.set_xlabel('Time simulation, in secs')
    ax.set_ylabel('Cumulative probabilty through the interface')

    if final_time is None or final_time == 0:
        ax.plot(np.array(cons.sec2fs(dt * np.arange(0, Nt))), np.array(results[:,1]),
                  linewidth=2,
                  label=r'Probabilty current $J_{{z=z_{{interface}}}}$, Transmission coefficient is : {:.5f} $\frac{{e}}{{\AA}}$'.format(
                      np.real(np.cumsum(results[:, 1])[-1])*dt))
    else:
        ind_time, pos_time = find_closest_value_in_array(cons.sec2fs(final_time),np.array(cons.sec2fs(dt * np.arange(0, Nt))))
        ax.plot(np.array(cons.sec2fs(dt * np.arange(0, Nt))), np.array(results[:, 1]),
                    linewidth=2,
                    label=r'Probabilty current $J_{{z=z_{{interface}}}}$, Transmission coefficient is : {:.5f} $\frac{{e}}{{\AA}}$'.format(
                        np.real(np.cumsum(results[:, 1])[ind_time]) * dt))
        ax.scatter(cons.sec2fs(pos_time),0)
    ax.legend()
    ax.grid()

    if path_to_save is None:
        fig.savefig('Probabilty current, Transmission coefficient.svg'.format('z'), format="svg",
                    dpi=300, bbox_inches='tight', transparent=True)
    else:
        plt.savefig("/".join(list(os.path.join(path_to_save, 'Probabilty current, Transmission coefficient.svg').split("\\"))) + ".svg",format="svg", dpi=300,bbox_inches='tight', transparent=True)
    return np.real(np.cumsum(results[:, 1])[-1])

def adjust_grid_density(density,z,v):
    '''
    Parameters
    ----------
    density : float
        The grid density. A quantity that was determined through the convergence tests and is the number
        of the space steps divided by the length of the system.
    z : np.array
        The spatial coordinates vector.
    v : np.array
        The local potntial vector along the system.
    Returns
    -------
    np.array, np.array
        It returns the new spatial coordinate vecor as z, and the new local potneital vector as v.
        They have been adjusted to the defined grid density supplied.
    '''

    L = (z[-1]-z[0])
    L = cons.A2m(L)
    N = L * density
    N = np.int64(N)
    z = cons.A2m(z)
    if N == 0:
        L = (z[-1] - z[0])
        L = cons.m2A(L)
        z = cons.m2A(z)
        N = L * density
        N = np.int64(N)

    z,v = interpolate_pchip(N,z,v)
    return z,v

def reach_plateau(x,y,critiria_plat = 0.0001, tol_2 = 0.005):
    '''
    Parameters
    ----------
    x : np.array
        The independent variable, usually will be the spatial grid vector or time space vector.
    y : np.array
        The dependent variable. The matching value of a function to the respective x value. Can be the comulative probabilty.
    critiria_plat : float. optional, default: 0.0001
        The value we decide to relate as no change in slope to determine the plateau region. The closer to zero
        the stricter critiria.
    tol_2 :  float. optional, default: 0.005
        The value we decide to relate as no change in values of the cumulative probabilty. The smaller value -
        the stricter critiria.
    Returns
    -------
    bool
        It checks whether we reached plateau, namely steady-state according to the vector supplied.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    assert len(x) == len(y)
    assert len(y) >= 40
    if np.int64((len(y)/4)) % 2 == 0:
        par = 1
    else:
        par = 0
    y = savitzky_golay(y,np.int64((len(y)/4))+par ,2)
    first_der = np.diff(y)/np.diff(x)
    y_last_part = y[np.int64((2*len(y) / 3)):]
    x_last_part = x[np.int64((2*len(y) / 3)):]
    first_der_last_part = first_der[(np.int64(( 2*len(y) / 3))):]
    critiria = np.abs(critiria_plat)
    linreg = np.real(lin_reg(x_last_part,y_last_part).slope)
    first_der_last_part = first_der[(np.int64(2*(len(y) / 3))):]
    flag_1 = np.abs(linreg) <= critiria * (np.abs(np.max(y_last_part))/x[1]) and not is_straight_line(y)
    flag_2 = np.abs(cons.J2eV(np.real(y[-1]))-cons.J2eV(np.real(y[-2]))) <= tol_2 and  np.abs(cons.J2eV(np.real(y[-2]))-cons.J2eV(np.real(y[-3]))) <= tol_2 and np.abs(cons.J2eV(np.real(y[-3]))-cons.J2eV(np.real(y[-4]))) <= tol_2
    return flag_1 and flag_2

def is_straight_line(y):
    '''
    Check if the input vector repesents a straight line
    Parameters
    ----------
    y : np.array
        The vector values we wish to check.
    Returns
    -------
    bool
        It returns whether the input vector is a straight line or not.
    '''
    return np.all(y[:-1]==y[1:])

def find_interface(x, y):
    '''
    This is a method that was duplicated from LOCPOT Class. It also appears there.
    It helps when we wish to allocate the interface position of the system,
    but have not created a locpot class instance.
    Parameters
    ----------
    x : np.array
        It stands for the spatial coordinates array.
    y : np.array
        The local potential vector.
    Returns
    -------
    int, float
        It returns the interface index in the locpot vector, and its `z` position
        If the system does not contain an interface, it just returns the last spatial grid coordinate position
        and its corresponded index. -> [index,position] ==> [len(z)-1,z[-1]]
    '''
    peaks = find_peaks(x, y)
    diff = []
    diff2 = []
    index_flag = 0
    max_flag = 0
    zz = []
    for i in range(0, len(peaks) - 1):
        diff = np.append(diff, np.abs(peaks[i + 1, 1] - peaks[i, 1]))
        zz = np.append(zz, peaks[i + 1, 0])
    num_of_peaks = 4
    iterations = 0
    while num_of_peaks >= 4 and iterations < 3:
        if iterations == 0:
            peaks_step_2 = find_peaks(zz, diff)
            diff = peaks_step_2[:, 1]
            zz = peaks_step_2[:, 0]
            zzz = []
        for i in range(0, len(diff) - 1):
            diff2 = np.append(diff2, np.abs(diff[i + 1] - diff[i]))
            zzz = np.append(zzz, zz[i + 1])
        num_of_peaks = len(diff2)
        iterations += 1
        if iterations < 3:
            if num_of_peaks >= 4:
                peaks_step_2 = find_peaks(zzz, diff2)
                try:
                    if len(peaks_step_2[:, 1]) <= 3:
                        break
                    else:
                        diff = peaks_step_2[:, 1]
                        zz = peaks_step_2[:, 0]
                        zzz = []
                        diff2 = []
                except IndexError:
                    diff2 = diff
                    zzz = zzz
                    break
            else:
                return 0, 0
    if len(diff) <= 2:
        print(' It did not find an interface, instead you will treat the end of the locpot as an interface')
        return len(x) - 1, x[-1]
    else:
        max_value = np.where(diff2 == np.max(diff2))
        z_interface = zzz[max_value]
        return find_closest_value_in_array(z_interface, x)

def integrate_trapz(vector, df):
    '''
    Parameters
    ----------
    vector : np.array
        The vector we wish the integrate numerically.
    df : float
        The step difference between adjacent steps. It assumes the the vector is spaced evenlly.
    Returns
    -------
    float
        The numerical intgration result.
    '''
    vector = np.asarray(vector, dtype=complex)
    df = np.float64(df)
    return np.float64(np.trapz(to_1D_vec(vector), dx=df))

def plateau_val(x,y,critiria = 0.0001):
    '''
    Parameters
    ----------
    x : np.array
        The spatial coordinates array.
    y : np.array
        The relevent functional values that corresponds the spatial coordinates vector.
    critiria : float, optional, default: 0.0001
        It can be changed for more of less strict evalutaion where the plateau has come.
    Returns
    -------
    float
        It returns the average value of the points that the plateau spread on.
    '''
    x = to_1D_vec(x)
    y = to_1D_vec(y)
    assert len(x) == len(y)
    if reach_plateau(x,y,critiria_plat = critiria):
        first_der = np.diff(y) / np.diff(x)
        y_last_part = y[np.int64(( 0.98 * len(y) )):]
        if len(y_last_part) <= 10:
            y_last_part = y[np.int64((0.95 * len(y))):]
            if len(y_last_part) <= 10:
                y_last_part = y[np.int64((0.85 * len(y))):]
                if len(y_last_part) <= 10:
                    if len(y) < 100:
                        y_last_part = y[np.int64((0.75 * len(y))):]
                    else:
                        y_last_part = y[np.int64((0.6667 * len(y))):]
        return np.float64(np.average(y_last_part))
    else:
        #print('The input vector has not reached plateau')
        return 0


def is_peak_minimum(peaks, peak):
    '''
    Notes
    -----
    Pay attention - the peak is within the range of the peaks and not at its edges.
    Otherwise it will raise an index out-of-range error.
    Parameters
    ----------
    peaks : `numpt.ndarray`, (N,2)
        The first column stands for the spatial poisition of the peaks.
        The second column is for the height of the peaks.
    peak : list: [int,float,float]
        The first argument is for the index of the peak inside the peaks array,
        The second argument is for the position of the peak. The third argument is for the height of the peak.
    Returns
    -------
    bool
        This function checks whether a given peak is a minimum point. (or at least a local minimum).
    '''
    flag = False
    try:
        if ((peaks[:, 1][np.int64(peak[0] - 1)]) > (peaks[:, 1][np.int64(peak[0])]) and
                (peaks[:, 1][np.int64(peak[0] + 1)]) > (peaks[:, 1][np.int64(peak[0])])):
            flag = True
    except IndexError:
        pass
    return flag



def is_peak_maximum(peaks, peak):
    '''
    Notes
    -----
    Pay attention - the peak is within the range of the peaks and not at its edges.
    Otherwise it will raise an index out-of-range error.
    Parameters
    ----------
    peaks : `numpy.ndarray`, (N,2)
        The first column stands for the spatial poisition of the peaks.
        The second column is for the height of the peaks.
    peak : list: [int,float,float]
        The first argument is for the index of the peak inside the peaks array,
        The second argument is for the position of the peak. The third argument is for the height of the peak.
    Returns
    -------
    bool
        This function checks whether a given peak is a maximum point. (or at least a local maximum).
    '''
    flag = False
    try:
        if ((peaks[:, 1][np.int64(peak[0] - 1)]) < (peaks[:, 1][np.int64(peak[0])]) and
                (peaks[:, 1][np.int64(peak[0] + 1)]) < (peaks[:, 1][np.int64(peak[0])])):
            flag = True
    except IndexError:
        pass
    return flag

def is_peak_maximum_2(z,v, peak_pos):
    '''
    Notes
    -----
    Pay attention - the peak is within the range of the peaks and not at its edges.
    Otherwise it will raise an index out-of-range error.
    Parameters
    ----------
    Returns
    -------
    bool
        This function checks whether a given peak is a maximum point. (or at least a local maximum).
    '''
    flag = False
    ind_peak,pos_peak = find_closest_value_in_array(peak_pos,z)
    if ind_peak > 2:
        if ind_peak < len(z)-2:
            if v[ind_peak-2] < v[ind_peak - 1] < v[ind_peak] and v[ind_peak] > v[ind_peak+1] > v[ind_peak+2]:
                flag=True
        elif ind_peak < len(z)-1:
            if v[ind_peak-2] < v[ind_peak - 1] < v[ind_peak] and v[ind_peak] > v[ind_peak+1]:
                flag=True
    elif ind_peak < len(z)-2:
        if v[ind_peak - 1] < v[ind_peak] and v[ind_peak] > v[ind_peak + 1] > v[ind_peak + 2]:
            flag = True
        elif ind_peak < len(z) - 1:
            if v[ind_peak - 1] < v[ind_peak] and v[ind_peak] > v[ind_peak + 1]:
                flag = True

    promin = ss.peak_prominences(v,[ind_peak])
    if flag and promin[0] > 0.3:
        flag = True
    else:
        flag = False
    return flag

def r_sqrd(v_original, v_fitted):
    '''
    Notes
    -----
    This function calculates the R square fitting parameter between two vectors.

    Parameters
    ----------
    v_original : np.array
        The vector contains the values whom we wish to compare to.
    v_fitted : np.array
        The vector contains the values whom we wish to fit .
    Returns
    -------
    float
        The calculated R sqrd value.
    '''
    if not len(to_1D_vec(v_original)) == len(to_1D_vec(v_fitted)):
        return 0
    else:
        return 1 - (np.sum(((v_original - v_fitted) ** 2)) / np.sum((v_original - np.mean(v_original)) ** 2))

def smooth_function(z,v):
    '''
    Notes
    -----
    This function calculates the R square fitting parameter between two vectors.

    Parameters
    ----------
    z : np.array
        The spatial coordinates array.
    v : np.array
        The relevent function's values that corresponds the spatial coordinates vector.
    Returns
    -------
    np.array, np.array
        This function returns the smoothed local potential vector with the corresponding spatial coordinates.
    '''
    flag_z = np.all(z == cons.m2A(z))
    flag_v = np.all(v == cons.J2eV(v))
    z = cons.m2A(z)
    v = cons.J2eV(v)
    window = len(v)
    window = window*0.0000001
    while np.fix(window) < 10:
        window *=10
    iteration = 0
    while iteration < 100:
        if np.mod(np.fix(window), 2) == 0:
            try:
                v_temp = savitzky_golay(v, window_size=np.fix(window) + 1, order=3)
            except:
                v_temp = np.ones(len(v))

            if r_sqrd(v, v_temp) >= 0.96:
                v = v_temp
                break
            else:
                if iteration == 0:
                    window = 1.0
                else:
                    window += 2
        else:
            try:
                v_temp = savitzky_golay(v, window_size=np.fix(window), order=3)
            except:
                v_temp = np.ones(len(v))
            if r_sqrd(v, v_temp) >= 0.96:
                v = v_temp
                break
            else:
                if iteration == 0:
                    window = 1.0
                else:
                    window += 2
        iteration +=1


    z,v = interpolate_pchip(np.int64(len(z)*0.8),z,v)
    z, v = interpolate_pchip(np.int64(len(z) * 1.25), z, v)
    return z,v