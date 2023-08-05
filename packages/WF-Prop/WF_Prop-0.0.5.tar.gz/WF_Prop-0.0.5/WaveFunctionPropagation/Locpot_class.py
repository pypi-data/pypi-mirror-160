# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 12:11:13 2021

@author: Yair Reichman
"""
import time

from pymatgen.io.vasp.outputs import Locpot
from pymatgen.core.structure import Structure, Lattice
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import os
from itertools import permutations
# from Find_peaks import find_peaks
import scipy.signal as ss
from Help_function_library_yair import *
from scipy.optimize import curve_fit
from matplotlib.widgets import Cursor
#from lmfit import Model, Parameters, Minimizer, minimize
import matplotlib.font_manager as fm

class Locpot_yair:
    '''
     Class of locpot where all its properties and its methods can be found
    '''

    def __init__(self, input_locpot=None, axis_index=None, is_2D=False, is_bulk_material = False, Has_interface = True, Locpot_file_name = None, Locpot_file_directory= None, Bulk_Locpot_file_name = None, Bulk_Locpot_file_directory = None,Locpot_Full_path = None, Locpot_bulk_materials_full_path = None, to_flip = False, has_flipped = False):
        '''
        Initiation method:
        ==================

        Parameters
        ----------

        input_locpot : pymatgen.io.vasp.outputs.Locpot, optional, default: None
                Can be initialized with an existing pymatgen locpot object.
        axis_index : int,{0: x, 1: y, 2: z}, optional, default: 2
                The axis index to be averaged along. (for x, insert  axis_index=0, for y axis insert axis_index=1,
                and for z axis insert axis_index=2).
        is_2D : bool, optional, default: False
                A flag that enables to perform 2D calculations. Not all functions support 2D calculations yet.
        bulk_material : bool, optional, default: False
                Aims to skip unecessary steps in the initializtion process for loading bulk materials.
        Locpot_file_name : str, optional, default: None
                Supply the string for the name of the locpot file, and also a string for the full path of the directory where the locpot files
                are located.
        Locpot_file_directory : str, optional, default: None
                Supply the string for the name of the locpot file, and also a string for the full path of the directory where the locpot files
                are located.
        Bulk_Locpot_file_name : list/tuple (str,str), optional, default: None
                For two different bulk locpot file names and full paths - supply it in a form of a list\tuple. The first place is for the first bulk material
                and the second place is for the second bulk material.
        Bulk_Locpot_file_directory : list/tuple (str,str), optional, default: None
                For two different bulk locpot file names and full paths - supply it in a form of a list\tuple. The first place is for the first bulk material
                and the second place is for the second bulk material.
        Locpot_Full_pat : str, optional, default: None
                Supply the string for the the full path of the Locpot file.
        Locpot_bulk_materials_full_path : list/tuple (str,str), optional, default: None
                For two different bulk locpot full paths - supply it in a form of a list\tuple. The first place is for the first bulk material
                and the second place is for the second bulk material.
        '''
        self.Locpot_file_name = Locpot_file_name
        self.to_flip = to_flip
        self.has_flipped = has_flipped
        self.Locpot_file_directory = Locpot_file_directory
        self.Bulk_Locpot_file_name = Bulk_Locpot_file_name
        self.Bulk_Locpot_file_directory = Bulk_Locpot_file_directory
        self.Locpot_full_path = Locpot_Full_path
        self.Locpot_bulk_materials_full_path = Locpot_bulk_materials_full_path
        if not (self.Locpot_file_name is None or self.Locpot_file_directory is None):
            self.locpot_path = os.path.join(self.Locpot_file_directory,  self.Locpot_file_name)
        elif not self.Locpot_full_path is None:
            self.locpot_path = self.Locpot_full_path
        else:
            self.locpot_path = None
        if not (self.Bulk_Locpot_file_name is None or self.Bulk_Locpot_file_directory is None):
            self.bulk_locpot_path = []
            types = [int, float, np.float64, np.int64,str,np.str]
            if type(self.Bulk_Locpot_file_name) in types:
                temp_path = os.path.join(self.Bulk_Locpot_file_directory,  self.Bulk_Locpot_file_name)
                self.bulk_locpot_path.append(temp_path)
            else:
                for i in range(len(self.Bulk_Locpot_file_name)):
                    temp_path = os.path.join(self.Bulk_Locpot_file_directory[i],  self.Bulk_Locpot_file_name[i])
                    self.bulk_locpot_path.append(temp_path)
        elif not self.Locpot_bulk_materials_full_path is None:
            self.bulk_locpot_path = []
            types = [int, float, np.float64, np.int64, str, np.str]
            if type(self.Locpot_bulk_materials_full_path) in types:
                self.bulk_locpot_path.append(self.Locpot_bulk_materials_full_path)
            else:
                for i in range(len(self.Locpot_bulk_materials_full_path)):
                    self.bulk_locpot_path.append(self.Locpot_bulk_materials_full_path)
        else:
            self.bulk_locpot_path = None

        if input_locpot is None:
            if not self.locpot_path is None:
                self.locpot = Locpot.from_file(self.locpot_path)
        else:
            self.locpot = input_locpot
        if input_locpot is None and (self.Locpot_file_name is None or self.Locpot_file_directory is None) and  self.Locpot_full_path is None:
            raise ValueError('You should supply an locpot object or a locpot file name and path')
        if axis_index is None:
            self.axis_index = 2
        else:
            self.axis_index = axis_index
        self.Has_interface = Has_interface
        self.locpot_vec = []
        self.is_2D = is_2D
        self.set_locpot_vec()
        self.is_bulk_material = is_bulk_material
        self.locpot_bulk_materials = []
        self.set_locpot_bulk_materials( bulk_material = self.is_bulk_material)
        self.locpot_vec_elongated = []
        self.cursor = None


    def get_atoms_position(self):
        '''
        Parameters
        ----------
        self

        Returns
        -------
        `numpy.ndarray`, (N,5)
                A matrix of the the coordinates of the atoms. There are 5 columns, the first three are the spatial coordinates of the atoms,
                as the first column is for x axis, the scond column is for the y axis, and the third column is for the z axis. The fourth column contains
                the atoms symbols, and the fifth and the last column has the atomic radius of the atoms.

        '''
        atom_coord = self.locpot.structure.cart_coords
        list_atomic_symbols = []
        list_atomic_radius = []
        species = self.locpot.structure.species[:]
        for i in range(len(atom_coord)):
            list_atomic_symbols.append(species[i].symbol)
        for i in range(len(atom_coord)):
            list_atomic_radius.append(species[i].atomic_radius)
        hist_atomic_radius = np.histogram(np.array(list_atomic_radius))
        atom_coord = np.column_stack((atom_coord, list_atomic_symbols, list_atomic_radius))
        return atom_coord

    def averaging_along_axis(self,locpot_vec = None, to_plot=False,to_plot_atoms=False,to_plot_widths=False,to_plot_heights=False,to_plot_cursor_choice=False):
        '''

        Parameters
        ----------
        locpot_vec : np.array, optional. default : None
                2 Columns arrays for the spatial coordinates and the local potential values.
        to_plot : bool, optional, default: False
                A flag to determine whether to plot or not.
        to_plot_atoms : bool, optional, default: False
                A flag that represents the choice whether to plot or not another plot of the atoms arrangement in 1D.
        to_plot_widths : bool, optional, default: False
                A flag that represents the choice whether to annotate or not the peaks widths of the locpot.
        to_plot_heights : bool, optional, default: False
                A flag that represents the choice whether to annotate or not the peaks heights of the locpot.
        to_plot_cursor_choice : bool, optional, default: False
                A flag that represents the choice whether to show cursor lines and annotate each click with box.
        Returns
        -------
        `numpy.ndarray`, (N,2)
                It returns a locpot matrix.The first column is the vector that contains the spatial coordinates of system.
                The second column is the averaged potential along the desires axis.

        '''
        # This code uses pymatgen for importing vasp relevant outputs.(locpot and contcar)

        font_dir = r'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\advent_Re.ttf'
        fonts = fm.findSystemFonts(fontpaths=font_dir)
        for font in fonts:
            fm.fontManager.addfont(font)
        plt.rcParams['font.family'] = 'advent'
        plt.rcParams['font.size'] = 8
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['axes.unicode_minus'] = False

        if locpot_vec is None:
            locpot_array = self.locpot.data['total']

            # The Locpot contains the electrostatic potential energy

            # Get the lengths of each coordinates of the 3D matrix of the input locpot:
            size = np.array([len(self.locpot.xpoints), len(self.locpot.ypoints), len(self.locpot.zpoints)])

            # 3x3 matrix whose rows are the lattice vectors.
            lattice = self.locpot.structure.lattice._matrix

            # Extracting a, b and c lattice vectors from the lattice pymatgen object
            a = np.array(lattice[0, :])
            b = np.array((lattice[1, :]))
            c = np.array((lattice[2, :]))

            # Calculating the norm for each lattice vector
            anorm = math.sqrt(a @ np.transpose(a))
            bnorm = math.sqrt(b @ np.transpose(b))
            cnorm = math.sqrt(c @ np.transpose(c))
            norm_dic = {0: anorm, 1: bnorm, 2: cnorm}
            axis_dic = {0: 'X', 1: 'Y', 2: 'Z'}

            # Calculate the grid point differnce for each direction.
            d = np.divide([anorm, bnorm, cnorm], [size])

            # Creating the desired grid
            if type(self.axis_index) == int:
                if self.axis_index == 0:
                    locpot_grid = np.array(self.locpot.xpoints)
                elif self.axis_index == 1:
                    locpot_grid = np.array(self.locpot.ypoints)
                elif self.axis_index == 2:
                    locpot_grid = np.array(self.locpot.zpoints)
                else:
                    raise ValueError('The axis index should be given as an integer 0:x 1:y 2:z or as a list for 2D '
                                     'calculation')
            elif type(self.axis_index) == list:
                if self.axis_index[0] == 0 and self.axis_index[1] == 1 or self.axis_index[0] == 1 and self.axis_index[
                    1] == 0:
                    locpot_grid = np.meshgrid(self.locpot.xpoints, self.locpot.ypoints)
                elif self.axis_index[0] == 0 and self.axis_index[1] == 2 or self.axis_index[0] == 2 and self.axis_index[
                    1] == 0:
                    locpot_grid = np.meshgrid(self.locpot.xpoints, self.locpot.zpoints)
                elif self.axis_index[0] == 1 and self.axis_index[1] == 2 or self.axis_index[0] == 2 and self.axis_index[
                    1] == 1:
                    locpot_grid = np.meshgrid(self.locpot.ypoints, self.locpot.zpoints)
                else:

                    raise ValueError('The axis index should be supplied as an integer 0:x 1:y 2:z or a list of \
                            two integers of these values')
            else:
                raise ValueError('The axis index should be supplied as an integer 0:x 1:y 2:z or a list of two \
                            integers of these values')

            # Get atoms position for plotting
            atoms_pos = self.get_atoms_position()

            # pymatgen function for finding the averaged potential along a given axis. the
            # axis is given by its index : 0=x; 1=y; 2=z

        if not self.is_2D:
            # integrating over the two axes:
            # Firstly we tried trapz, but for the numeric errors it was better to just sum over the values.
            # intgeral_over_x_y = d[0][1]*d[0][0]*np.trapz(np.trapz(locpot_array,axis=1),axis=0)/(bnorm*anorm)
            if self.to_flip and not locpot_vec is None and not self.has_flipped:
                to_plot_atoms = False
            if locpot_vec is None:
                assert type(self.axis_index) == int
                temp_axis_index = np.array([0, 1, 2])
                axis_index_2 = [temp_axis_index[i] for i in range(0, len(temp_axis_index)) if
                                not temp_axis_index[i] == self.axis_index]
                intgeral = (d[0][axis_index_2[0]]) * (d[0][axis_index_2[1]]) * np.sum(
                    np.sum(locpot_array, axis=axis_index_2[1]), axis=axis_index_2[0]) / (
                                   norm_dic[axis_index_2[1]] * norm_dic[axis_index_2[0]])

            # creating the final matrix to be returned
                locpot_mat = np.column_stack((locpot_grid, intgeral))
                if self.to_flip and not self.has_flipped:
                    max_z = locpot_mat[:,0][-1] - locpot_mat[:,0][0]
                    locpot_mat[:,0] = max_z - locpot_mat[:,0][-1::-1]
                    locpot_mat[:, 1] = locpot_mat[:, 1][-1::-1]
                    self.has_flipped = True
            else:
                locpot_mat = locpot_vec
                locpot_mat[:,0] = cons.m2A(locpot_mat[:,0])
                locpot_mat[:, 1] = cons.J2eV(locpot_mat[:, 1])
            if to_plot:
                if to_plot_atoms and locpot_vec is None:
                    fig, axs = plt.subplots(2, 1, figsize=(4,5),sharex=True)
                else:
                    fig, axs = plt.subplots(1, 1,  figsize=(4,5),sharex=True)
                    # Just for treating the case for indexing to get a single ax when all the code from beneath is based on this syntext.
                    axs = [axs]

                if locpot_vec is None:
                    axs[0].plot(locpot_mat[:, 0] * norm_dic[self.axis_index], locpot_mat[:, 1],label = '1D Local potential',lw=2.5)
                    axs[0].grid(True)
                else:
                    axs[0].plot(locpot_mat[:, 0] , locpot_mat[:, 1],label = '1D Local potential',lw=2.5)
                    axs[0].grid(True)

            # Draw below the plot atoms positions
            # Firstly, we find the species in our system
                if locpot_vec is None:
                    atoms_specie, atoms_specie_num = np.unique(atoms_pos[:, 3], return_counts=True)
                    atomic_radius = np.unique(np.float64(atoms_pos[:, 4]))
                    relative_atomic_radius = np.float64(atoms_pos[:, 4]) / np.sum(atomic_radius)
            # relative_atomic_radius = np.multiply(np.float64(atoms_pos[:,4]),0.25)/np.sum(atomic_radius)
            # relative_atomic_radius = relative_atomic_radius/np.sum(relative_atomic_radius)

            # for each specie, we want the draw the atom positions with different color for each atom and different size according to the realtive atomic radius
                    specie = [i for i in atoms_specie]
                    temp = [specie[0]]
                    for i in specie[1:]:
                        if not i in temp:
                            temp.append(i)
                    specie = temp
                    color_list = ['r','g', 'b', 'c', 'm', 'y', 'k']
                    dic_specie = {}
                    dic_color = {}
                    for i in range(len(specie)):
                        dic_specie.update({specie[i]: 0})
                        dic_color.update({specie[i]: color_list[i]})

                    for specie in atoms_specie:
                        list_for_each_atoms_specie_pos = []
                        list_for_each_atoms_specie_height = []
                        list_for_each_atomic_radius = []
                        for i in range(len(atoms_pos[:, self.axis_index])):
                            if atoms_pos[i, 3] == specie:
                                list_for_each_atoms_specie_pos.append(np.float64(atoms_pos[i, self.axis_index]))
                                list_for_each_atoms_specie_height.append(np.float64(atoms_pos[i, axis_index_2[0]]))
                                list_for_each_atomic_radius.append(np.float64(relative_atomic_radius[i]))
                        if to_plot:
                            if to_plot_atoms and  locpot_vec is None:
                                axs[1].scatter(np.float64(list_for_each_atoms_specie_pos),np.float64(list_for_each_atoms_specie_height), facecolors=dic_color[specie],
                               s=np.multiply(list_for_each_atomic_radius, 1000), label=specie,alpha = 0.8,edgecolor='black',zorder=10)
                                axs[1].grid(True)

                    #  axs[1].scatter(np.float64(atoms_pos[:,axis_index]),np.float64(atoms_pos[:,axis_index_2[0]]))
                    #plt.tick_params(labelcolor='none', which='both', top=False, bottom=True, left=False, right=False)
                        plt.xlabel('{} axis in Angstrum'.format(axis_dic[self.axis_index]))
                        if to_plot_atoms and  locpot_vec is None:
                            try:
                                axs[1].set_ylabel('Perpendicular grid in Angstrum',fontsize = 8)
                            except ValueError:
                                pass
                            axs[1].legend(labelspacing=2, fontsize=8, markerscale=0.5, handletextpad=0.3,
                                          loc='center right')
                        axs[0].set_ylabel('Electrostatic potential in eV, V({})'.format(axis_dic[self.axis_index]),fontsize = 12)
                        axs[0].legend( fontsize=8, handletextpad=0.3, loc='lower right')
            if locpot_vec is None:
                if self.axis_index == 0:
                    x = locpot_mat[:, 1] * self.find_unit_cell_lattice_parameter()
                    y = locpot_mat[:, 2]
                elif self.axis_index == 1:
                    x = locpot_mat[:, 0] * self.find_unit_cell_lattice_parameter()
                    y = locpot_mat[:, 2]
                else:
                    x = locpot_mat[:, 0] * self.find_unit_cell_lattice_parameter()
                    y = locpot_mat[:, 1]
            else:
                x = locpot_mat[:, 0]
                y = locpot_mat[:, 1]

            # peaks_minima = find_peaks_minima(x, y, ignore_local_minima = True)
            # peaks_maxima = find_peaks_maxima(x, y, ignore_local_maxima=True)
            # peaks = np.append(peaks_minima,peaks_maxima,axis=0)
            # peaks = peaks[peaks[:, 0].argsort()]
            peaks = find_peaks(x,y)
            if to_plot:
                axs[0].scatter(peaks[:, 0], peaks[:, 1])

                if to_plot_cursor_choice:
                    annot=axs[0].annotate("",xy=(0,0),xytext=(-40,40),textcoords="offset points",
                                          bbox=dict(boxstyle='round',fc='linen',ec='k',lw=1),arrowprops=dict(arrowstyle='-|>'),fontsize = 14  )
                    annot.set_visible(False)
                    # function for storing and showing the clicked values
                    # coord=[]
                    self.cursor = Cursor(axs[0], horizOn=True, vertOn=True, color='gray', lw=0.9)
                    def on_click(event):
                        # nonlocal coord
                        # coord.append((event.xdata,event.ydata))
                        x_val = event.xdata
                        y_val = event.ydata
                        annot.xy = (x_val,y_val)
                        try:
                            if locpot_vec is None:
                                 text = "({} = {:.5g} Ang, local potential = {:.3g} [eV])".format(axis_dic[self.axis_index],x_val,y_val)
                            else:
                                text = "({} = {:.5g} Ang, local potential = {:.3g} [eV])".format('z',
                                                                                             x_val, y_val)
                            annot._text = text
                            annot.set_visible(True)
                            fig.canvas.draw()
                        except TypeError:
                            pass

                    fig.canvas.mpl_connect('button_press_event',on_click)


                if to_plot_heights:
                    anotations = []
                    count = 0
                    for i in peaks[:, 1][range(0,len(peaks[:, 0]),10)]:
                        anotations.append([count,'{:.3g} eV'.format(i)])
                        count +=10
                    count = 1
                    for i in peaks[:, 1][range(5,len(peaks[:, 0]),10)]:
                        anotations.append([count,'{:.3g} eV'.format(i)])
                        count += 10
                    for i, label in enumerate(anotations):
                            if is_peak_minimum(peaks,[label[0],peaks[:, 0][label[0]],peaks[:, 1][label[0]]]):
                                try:
                                    axs[0].annotate(label[1], xy=(peaks[:, 0][label[0]], peaks[:, 1][label[0]]),
                                                    xytext=(-25, -25), textcoords="offset points",
                                                    bbox=dict(boxstyle='round', fc='linen', ec='k', lw=1),
                                                    arrowprops=dict(arrowstyle='->'), fontsize=8)
                                except IndexError:
                                    axs[0].annotate(label[1], xy=(peaks[:, 0][label[0] - 1], peaks[:, 1][label[0] - 1]),
                                                    xytext=(-25, -25), textcoords="offset points",
                                                    bbox=dict(boxstyle='round', fc='linen', ec='k', lw=1),
                                                    arrowprops=dict(arrowstyle='->'), fontsize=8)
                            else:
                                try:
                                    axs[0].annotate(label[1],xy=(peaks[:, 0][label[0]], peaks[:, 1][label[0]]),xytext=(25,25),textcoords="offset points",
                                                    bbox=dict(boxstyle='round', fc='linen', ec='k', lw=1),arrowprops=dict(arrowstyle='->'),fontsize=8)
                                except IndexError:
                                    axs[0].annotate(label[1],xy=(peaks[:, 0][label[0]-1], peaks[:, 1][label[0]-1]),xytext=(25,25),textcoords="offset points",
                                                    bbox=dict(boxstyle='round', fc='linen', ec='k', lw=1),arrowprops=dict(arrowstyle='->'),fontsize=8)
                if to_plot_widths:
                    allmax = find_peaks_maxima(self.locpot_vec[:, 0], self.locpot_vec[:, 1], ignore_local_maxima=False)
                    maxima = [i for i in range(len(self.locpot_vec[:, 0])) if self.locpot_vec[:, 0][i] in allmax[:, 0]]

                    widths,width_heights,left_ips, right_ips = ss.peak_widths(self.locpot_vec[:, 1], maxima, rel_height=0.5)
                    max_index = len(self.locpot_vec[:,0])-1
                    max_coord = self.locpot_vec[:,0][-1]
                    new_left_ips = []
                    new_right_ips = []
                    new_widths = []
                    for i in range(len(left_ips)):
                        new_left_ips.append((left_ips[i]*max_coord)/max_index)
                        new_right_ips.append((right_ips[i] * max_coord) / max_index)
                        new_widths.append(((right_ips[i] * max_coord) / max_index)-(left_ips[i]*max_coord)/max_index)
                    anotations = []
                    count = 0
                    new_left_ips = np.array(new_left_ips)
                    new_right_ips = np.array(new_right_ips)
                    new_widths = np.array(new_widths)
                    for n,i in enumerate(new_widths[range(0,len(new_widths),5)]):
                        anotations.append([count,'{:.3g}'.format(i)])
                        count +=5
                    for i, label in enumerate(anotations):
                        try:
                            axs[0].hlines(width_heights[label[0]], new_left_ips[label[0]], new_right_ips[label[0]],  color='gray',zorder=0)
                            axs[0].annotate(label[1],xy=((new_left_ips[label[0]]+new_right_ips[label[0]])/2,width_heights[label[0]]),xytext=(-25,-5),textcoords="offset points",
                                            bbox=dict(boxstyle='round4', fc='w', ec='gray', lw=1.5),arrowprops=dict(arrowstyle='->'),fontsize=8)
                        except IndexError:
                            axs[0].hlines(width_heights[label[0]-1], new_left_ips[label[0]-1], new_right_ips[label[0]-1],  color='gray',zorder=0)
                            axs[0].annotate(label[1],xy=((new_left_ips[label[0]-1]+new_right_ips[label[0]-1])/2,width_heights[label[0]-1]),xytext=(-25,-5),textcoords="offset points",
                                            bbox=dict(boxstyle='round4', fc='w', ec='gray', lw=1.5),arrowprops=dict(arrowstyle='->'),fontsize=8)
                plt.tight_layout()
                try:
                    plt.style.use(['science', 'notebook', 'grid'])
                except:
                    pass
                fig.show()
                if locpot_vec is None:
                     plt.subplots_adjust(left=0.135, right=0.845, bottom=0.30, top=0.70, wspace=0.085)
                else:
                    plt.tight_layout()
                if locpot_vec is None:
                    fig.savefig('1D potential along axis {}.svg'.format(axis_dic[self.axis_index]),format="svg",dpi=300, bbox_inches='tight', transparent=True)
                else:
                    fig.savefig('1D potential along axis {}.svg'.format('z'), format="svg",
                                dpi=300, bbox_inches='tight', transparent=True)
            return locpot_mat
        else:
            assert type(self.axis_index) == list and len(self.axis_index) == 2
            self.axis_index.sort()
            temp_axis_index = np.array([0, 1, 2])
            axis_index_2 = [temp_axis_index[i] for i in range(0, len(temp_axis_index)) if
                            not temp_axis_index[i] in self.axis_index]
            integral = (d[0][axis_index_2[0]]) * (
                    np.sum(locpot_array, axis=axis_index_2[0]) / (norm_dic[axis_index_2[0]]))
            locpot_mat = locpot_grid.copy()
            locpot_mat.append(np.transpose(integral))
            if to_plot:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(locpot_mat[0] * norm_dic[self.axis_index[0]],
                                locpot_mat[1] * norm_dic[self.axis_index[1]], locpot_mat[2])
                ax.set_xlabel('{} axis in Angstrum'.format(axis_dic[self.axis_index[0]]))
                ax.set_ylabel('{} axis in Angstrum'.format(axis_dic[self.axis_index[1]]))
                ax.set_zlabel('2D Electrostatic potential in eV, V({},{})'.format(axis_dic[self.axis_index[0]],
                                                                                  axis_dic[self.axis_index[1]]))
                fig.show()
                fig.savefig('2D potential along axis {} and {}'.format(axis_dic[self.axis_index[0]],
                                                                       axis_dic[self.axis_index[1]]))
            return locpot_mat

    def find_interface(self, x=None, y=None):
        '''

        Parameters
        ----------
        x : np.array, array_like, optional, default: None
                It stands for the spatial coordinates array.
                If not supplied, is calcualted from the instance attribute self.locpot.

        y : np.array, array_like, optional, default: None
                The local potential vector.
                If not supplied, is calcualted from the instance attribute ``self.locpot``.
        Returns
        -------
        float, float
                It returns the interface index in the locpot vector, and its z's position
                If the system does not contain an interface, it just returns the last spatial grid coordinate position
                and its corresponded index. -> [index,position] ==> [len(z)-1,z[-1]]

        '''
        try:
            if x is None:
                x = self.locpot_vec[:, 0]
        except:
            pass
        try:
            if y is None:
                y = self.locpot_vec[:, 1]

        except:
            pass

        if self.Has_interface:
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
                            zzz = zz
                            diff2 = diff
                            break

                    else:
                        return 0,0
            if len(diff) <= 2:
                 print(' It did not find an interface, instead you will treat the end of the locpot as an interface')
                 return len(x)-1, x[-1]
            else:
                max_value = np.where(diff2 == np.max(diff2))
                z_interface = zzz[max_value]
                return find_closest_value_in_array(z_interface, x)
        else:
            return len(x)-1, x[-1]

    def approximately(self, compare_to, *args, tol=5):
        '''

        Parameters
        ----------
        compare_to : int/float
                The value we wish to compare to.
        *args : int/float/array_like
                The value\s we wish to compare to.
        tol : int/float, optional, default: 5
                In precents. The tolerance level we wish to apply. The default value is set to 5% tolerance.

        Returns
        -------
        bool
                It returns `True` or `False` whether the input value is in the proxmity range of the tolerance
                with respect to the the values supplied.
        '''
        flag = False
        tol /= 100
        tol_p = tol + 1
        tol_m = 1 - tol
        compare_to = np.float64(compare_to)
        for i in args:
            i = np.float64(i)
            if compare_to <= 0.1 or i <= 0.1:
                if compare_to <= 0.1:
                    compare_to = 0.1
                if i <= 0.1:
                    i = 0.1
                flag = np.round(compare_to, 1) == np.round(np.float64(i), 1)

            if i * tol_m <= compare_to <= i * tol_p:
                flag = True

        return flag

    def find_unit_cell_lattice_parameter(self, is_axis_rel=True):
        '''

        Parameters
        ----------

        is_axis_rel : bool, optional, default: True
                A flag that tells if the class object attribute - `axis_index`
                is the relevant to return the appropriate lattice parameter in that direction.

        Returns
        -------
        float
                The relevant lattice parameter.
        '''

        lattice_parameters = self.locpot.structure.lattice.abc
        if is_axis_rel:
            if self.is_2D:
                raise ValueError("not programmed for 2D potentail calc")
            if self.axis_index == 0:
                return lattice_parameters[0]
            elif self.axis_index == 1:
                return lattice_parameters[1]
            elif self.axis_index == 2:
                return lattice_parameters[2]
            else:
                raise ValueError("axis index should be 0:x 1:y 2:z")
        else:
            return lattice_parameters

    def find_all_permutations(self,materials_list_strings):
        '''

        Parameters
        ----------
        materials_list_strings : array_like,type: str
                The input of the species names / materials names whithin the system

        Returns
        -------

        res : array_like,type: str
                It returns all the combinations of materials or species that can be found.
                It suppose to locate locpot files of the bulk materials in the current working directory
                to be loaded into the interface Locpot object.
                It meant to answer cases where we have a material constructed of several species such as
                GaAs\ AlN\ and so on..
        '''

        temp = []
        for idx in range(1, len(materials_list_strings) + 1):
            temp.extend(list(permutations(materials_list_strings, idx)))
        res = []
        for ele in temp:
            res.append("".join(ele))
        return res

    def set_locpot_bulk_materials(self, bulk_material = False):
        '''
        **Loading the bulk materials' locpots of the two materials involved in the interface system.**
        Parameters
        ----------
        bulk_material : bool, optional, default: False
                Can be given for skipping to load another level of bulk material.

        '''
        # if not bulk_material and len(self.locpot_bulk_materials) < 2 and self.Has_interface:
        #     interface_ind, interface = self.find_interface()
        #     species = self.locpot.structure.symbol_set
        #     atoms_positions = self.get_atoms_position()
        #     symbols_vector_main_axis = atoms_positions[:, 3]
        #     system_bottom = np.sort(np.float64(atoms_positions[:, 2]))[0]
        #     system_upper = np.sort(np.float64(atoms_positions[:, 2]))[-1]
        #     first_half_symbols_vector = symbols_vector_main_axis[[np.float64(atoms_positions[:, 2]) < interface - 2.5][0] *
        #                                      [np.float64(atoms_positions[:, 2]) > system_bottom + 2.5][0]]
        #     sec_half_symbols_vector = symbols_vector_main_axis[[np.float64(atoms_positions[:, 2]) > interface + 2.5][0] *
        #                                      [np.float64(atoms_positions[:, 2]) < system_upper - 2.5][0]]
        #     first_material = np.unique(first_half_symbols_vector)
        #     first_material_string = Locpot_yair.find_all_permutations(first_material)
        #     second_material = np.unique(sec_half_symbols_vector)
        #     second_material_string = Locpot_yair.find_all_permutations(second_material)
        if not bulk_material and len(self.locpot_bulk_materials) < 2 and self.Has_interface:
            if not self.bulk_locpot_path is None:
                for i in self.bulk_locpot_path:
                    try:
                         self.locpot_bulk_materials.append(Locpot.from_file(i))
                    except:
                        pass


        #     path = "../../LOCPOTS_For_Git/LOCPOT_"
        #     for i in first_material_string:
        #         locpot_path = os.path.join(path, str(i)).replace("\\", "")
        #         try:
        #             self.locpot_bulk_materials.append(Locpot.from_file(locpot_path))
        #         except:
        #             pass
        #     for i in second_material_string:
        #         locpot_path = os.path.join(path, str(i)).replace("\\", "")
        #         try:
        #             self.locpot_bulk_materials.append(Locpot.from_file(locpot_path))
        #         except:
        #             pass
        # else:
        #     pass

    def set_axis_index(self, axis_ind=None):
        '''

        Parameters
        ----------

        axis_ind : int, {0: x, 1: y, 2: z}, optional, default: None
                    The axis index we desire to update our object attribute.

        Returns
        -------
        None
                *Just set up a new axis index property of the object instance.*

        '''

        if axis_ind == None:
            pass
        else:
            self.axis_index = axis_ind

    def set_is_2D(self, is2d=False):
        '''

        Parameters
        ----------

        is2d : bool, optional, default: False
                A flag to determine whether the calculation should be performed in 2D.
                This is an editing method for the class object.

        Returns
        -------
        None
        '''
        self.is_2D = is2d

    def find_position_to_insert(self, zz=None, vv=None):
        '''

        Gets Locpot object. Using the interface and bulk materials' locpots.
        Look for the best place to insert the bulk locpot into the interface
        system locpot.
        Can be supplied in advance zz - spatial coordinates vector, and vv - local potential vector,
        to be referenced as the main vector to be searched to position to insert.


        Parameters
        ----------
        zz : np.array, optional, default: None
                If not supplied, the default is taken from `self.locpot_vec[:, 0]` attribute of `Locpot_yair` instance.
                Vector of the spatial grid. (spatial coordinates)
        vv : np.array, optional, default: None
                If not supplied, the default is taken from `self.locpot_vec[:, 1]` attribute of `Locpot_yair` instance.
                Vector of the local potential.

        Returns
        -------
        float, int
                It returns the position, and its corresponding index in the interface locpot interface. Regarding both the left side materials
                and the right side material. These 2 arrays of the form [,,] -> where [start_ind, finish_ind, minima_position, max_R_sqrd]
                If we don't have an interface, it returns the last index,position of the spatial grid vector.

        '''
        # input verification
        #..................................................
        self.locpot_vec = to_2_column_mat(self.locpot_vec)
        try:
            if zz is None:
                zz = self.locpot_vec[:, 0]
        except:
            pass
        try:
            if vv is None:
                vv = self.locpot_vec[:, 1]
        except:
            pass
        # ..................................................

        # Checks if the system contains an interface
        if self.Has_interface:
            # if it does has an interface:
            interface_ind,interface = self.find_interface(zz, vv)
            peaks = find_peaks(zz,vv)

            # first bulk material == from the left of the interface
            z_left = np.array([z for i, z in enumerate(zz) if zz[i] < interface])
            v_left = np.array([v for i, v in enumerate(vv) if zz[i] < interface])
            z_left_minimas = find_peaks_minima(z_left, v_left)[:, 0]
            v_left_minimas = find_peaks_minima(z_left, v_left)[:, 1]
            # second bulk material == from the right of the interface
            z_right = np.array([z for i, z in enumerate(zz) if zz[i] > interface])
            v_right = np.array([v for i, v in enumerate(vv) if zz[i] > interface])
            z_right_minimas = find_peaks_minima(z_right, v_right)[:, 0]
            v_right_minimas = find_peaks_minima(z_right, v_right)[:, 1]

            # Getting the first bulk material locpot from the class attribute.
            first_bulk_material = Locpot_yair(self.locpot_bulk_materials[0])
            z_first_bulk = first_bulk_material.locpot_vec[:, 0]
            v_first_bulk = first_bulk_material.locpot_vec[:, 1]
            z_first_bulk_minimas = find_peaks_minima( z_first_bulk , v_first_bulk)[:, 0]
            v_first_bulk_minimas = find_peaks_minima(z_first_bulk, v_first_bulk)[:, 1]

            # Getting the second bulk material locpot from the class attribute.
            sec_bulk_material = Locpot_yair(self.locpot_bulk_materials[1])
            z_sec_bulk = sec_bulk_material.locpot_vec[:, 0]
            v_sec_bulk = sec_bulk_material.locpot_vec[:, 1]
            z_sec_bulk_minimas = find_peaks_minima(z_sec_bulk, v_sec_bulk)[:, 0]
            v_sec_bulk_minimas = find_peaks_minima(z_sec_bulk, v_sec_bulk)[:, 1]

            # finds the vertical shifts between the system local potential and its bulk materials local potentials.
            shift_left, shift_right = self.find_locpot_shift()

            # Fixing the local potential values by adding or substracting the relevant shift.
            v_first_bulk = v_first_bulk - shift_left
            v_sec_bulk = v_sec_bulk - shift_right


            index_minimas_left = 0
            length_first_bulk_material = z_first_bulk[-1] - z_first_bulk[0]
            minima_position = z_left_minimas[index_minimas_left]
            max_R_sqrd = 0
            indices_left = [0, 0, 0]

            # The loop iterates via the minima points and jumps at each iteration by the length of the bulk material
            # locpot. It then compares the cut range of the system locpot with the bulk material locpot.
            # The comparison test is R_sqrd. Then Taking the section the yield the highest R_sqrd and returning the
            # indedice where it starts from and end at. The starting position will be considered as the position
            # to insert at.

            while minima_position + length_first_bulk_material <= z_left_minimas[-1] and index_minimas_left < len(
                    z_left_minimas):

                start_index, start_pos = find_closest_value_in_array(minima_position,z_left)
                finish_index, finish_pos = find_closest_value_in_array(minima_position + length_first_bulk_material,z_left)

                if finish_index < len(z_left):
                    temp_z, temp_v = z_left[start_index: finish_index], v_left[start_index: finish_index]
                    temp_z, temp_v = interpolate_pchip(len(v_first_bulk),temp_z, temp_v)
                    temp_R_sqrd = r_sqrd(v_first_bulk, temp_v)
                    if temp_R_sqrd > max_R_sqrd:
                        max_R_sqrd = temp_R_sqrd
                        start_index, start_pos = find_closest_value_in_array(minima_position, zz)
                        finish_index, finish_pos = find_closest_value_in_array(minima_position + length_first_bulk_material,
                                                                               zz)
                        indices_left = [start_index, finish_index, minima_position,max_R_sqrd,temp_z,temp_v,z_first_bulk+start_pos,v_first_bulk ]
                    index_minimas_left += 1
                    minima_position = z_left_minimas[index_minimas_left]
                else:
                    break

            index_minimas_right = 0
            length_sec_bulk_material = z_sec_bulk[-1] - z_sec_bulk[0]
            minima_position = z_right_minimas[index_minimas_right]
            max_R_sqrd = 0
            indices_right = [0, 0, 0]

            # The above loop treats the left hand side of the system. (from the left of the interface)
            # This loop treats the right hand side of the system in the same manner.

            while minima_position + length_sec_bulk_material <= z_right_minimas[-1] and index_minimas_right < len(
                    z_right_minimas):

                start_index, start_pos = find_closest_value_in_array(minima_position,z_right)
                finish_index, finish_pos = find_closest_value_in_array(minima_position + length_sec_bulk_material,z_right)

                if finish_index < len(zz):
                    temp_z, temp_v = z_right[start_index: finish_index], v_right[start_index: finish_index]
                    temp_z, temp_v = interpolate_pchip(len(v_sec_bulk),temp_z, temp_v)
                    temp_R_sqrd = r_sqrd(v_sec_bulk, temp_v)

                    if temp_R_sqrd > max_R_sqrd:
                        max_R_sqrd = temp_R_sqrd
                        start_index, start_pos = find_closest_value_in_array(minima_position, zz)
                        finish_index, finish_pos = find_closest_value_in_array(minima_position + length_sec_bulk_material,
                                                                               zz)
                        indices_right = [start_index, finish_index, minima_position, max_R_sqrd, temp_z,temp_v,z_sec_bulk+start_pos,v_sec_bulk]
                    index_minimas_right += 1
                    minima_position = z_right_minimas[index_minimas_right]
                else:
                    break

            return indices_left, indices_right

        # Namely, we don't have an interface in our system, so the position to insert will be
        # at the end of the system. It returns the index of the last position in the spatial grid vector
        # and the actual position at the grid,
        else:
            return len(zz)-1,zz[-1]

    def set_locpot_vec(self):
        '''
        A method aims to initialize Locpot vector of the Locpot object.

        Returns
        -------
        None
        '''
        # Input verifiaction
        # ...........................................................
        if self.locpot_vec is None or self.locpot_vec == []:
            self.locpot_vec = self.averaging_along_axis()
            lat_par = self.find_unit_cell_lattice_parameter()
            self.locpot_vec[:,0]= self.locpot_vec[:, 0] * lat_par
        # ...........................................................

        dx = np.diff(self.locpot_vec[:,0])[0]
        i=1

        # This loop guaruntee that the length of the system will be at least at the length of 20*spatial_spacing (dx)
        while  self.locpot_vec[:,0][-1] < 20 * dx:
            self.locpot_vec[:, 0],self.locpot_vec[:,1] = multiply_z_v_vecs(self.locpot_vec[:, 0],self.locpot_vec[:,1],multi = i)
            i +=1

    def elongate_locpot(self, multi_left = 1, multi_right = 1,manual = False,
        pos_to_insert = None, multi_manual = 1, z_to_insert_manual = None, v_to_insert_manual = None,locpot_vec = None, return_left_increment = False,return_right_increment = False):
        '''

        Parameters
        ----------
        multi_left : int, optional, default: 1
                It determines how many times to multiply the repeated locpot that will be inserted.
        multi_right : int, optional, default: 1
                It determines how many times to multiply the repeated locpot that will be inserted.
        manual : bool, optional, default: False
                This is a flag the tells if we are going to treat the elongation manually or automatically.
                If it is set to ``True``, we should supply more arguments as desribed in the next lines.
        pos_to_insert : float, optional, default: None
                If `manual =` ``True``, then it must be supplied. It determines where to insert the multiplied repeated locpot.
                It is a position in the spatial grid.
        multi_manual : int, optional, default: None
                If `manual =` ``True``, then it must be supplied. It determines how many times to
                multiply the repeated locpot that will be inserted manually.
        z_to_insert_manual : np.array, optional, default: None
                If `manual =` ``True``, then it must be supplied. The manully inserted spatial coordinates vector.
        v_to_insert_manual : np.array, optional, default: None
                If  `manual =` ``True``, then it must be supplied. The manully inserted local potential vector.
        locpot_vec : `numpy.ndarray`, (N,2), optional, default: None
                It is not necessarily goes with the 'manual' option. It just gives more flexibilty whether the
                elongation will be held on the class instance locpot attribute, or on an external locpot vector supplied as an argument. This is a two-column vector,
                the first column is for the spatial coordinates and the second column is for the local potential.
        return_left_increment : bool, optional, default : False
                If it is set to ``True``, the difference between the original and the elongated local potential vectors will be returned together with the reference point.
        return_right_increment : bool, optional, default : False
                If it is set to ``True``, the difference between the original and the elongated local potential vectors will be returned together with the reference point.

        Returns
        -------
        z_Locp, v_Locp : np.array, np.array
                The new elongated spatial grid vector, the new elongated local potential vector.
        z_Locp, v_Locp, delta, ref point : np.array, np.array, float, float
                If return_right_increment or return_right_increment == ``True``
                It returns also difference between the original and the elongated local potential vectors will be returned together with the reference point, if
                it was specified to return those.
        '''
        # if locpot_vec is supplied as an argument, all the changes will take ation uppon it.
        # Otherwise they will affect only the locpot attribute of the class instance.
        delta_length_right = 0
        delta_length_left = 0
        delta_length_general = 0
        if locpot_vec is None:
            z_Locp = self.locpot_vec[:,0]
            v_Locp = self.locpot_vec[:, 1]
        else:
            z_Locp = locpot_vec[:,0]
            v_Locp = locpot_vec[:, 1]
        z_Locp = cons.m2A(z_Locp)
        v_Locp = cons.J2eV(v_Locp)
        len_original_temp_right = z_Locp[-1] - z_Locp[0]
        len_original_temp_left = z_Locp[-1] - z_Locp[0]
        len_original_temp_general = z_Locp[-1] - z_Locp[0]
        # if we wish all the procedure to occure automatically with the class feature and attributes:
        if not manual and self.Has_interface:
            Locp_first_bulk_material = Locpot_yair(self.locpot_bulk_materials[0], is_bulk_material=True)
            Locp_sec_bulk_material = Locpot_yair(self.locpot_bulk_materials[1],is_bulk_material=True)
            z_first_bulk_material = Locp_first_bulk_material.locpot_vec[:,0]
            v_first_bulk_material = Locp_first_bulk_material.locpot_vec[:, 1]
            z_first_bulk_material, v_first_bulk_material = multiply_z_v_vecs(z_first_bulk_material, v_first_bulk_material, multi = multi_left)

            z_sec_bulk_material = Locp_sec_bulk_material.locpot_vec[:,0]
            v_sec_bulk_material = Locp_sec_bulk_material.locpot_vec[:, 1]
            z_sec_bulk_material, v_sec_bulk_material = multiply_z_v_vecs(z_sec_bulk_material, v_sec_bulk_material, multi = multi_right)

            left_shift, right_shift = self.find_locpot_shift()
            indices_left, indices_right = self.find_position_to_insert()
            z_locp_length_original = z_Locp[-1]
            # if loading the instance system locpot, and its bulk material locpot, and then, search for good match
            # of the bulk material locpot on the whole system locpot. When it satisfies the condition of the R_sqrd to be
            # greater than 0.85, it inserted the multiplied bulk material locpot at the position if found.
            # It does it both for the right and the left side of the interface system.
            if indices_left[3] > 0.85:
                ind_to_insert,pos_to_insert = find_closest_value_in_array(indices_left[2],z_Locp)
                z_locp_length_original = z_Locp[-1]
                z_Locp, v_Locp = insert_potential_into_position(z_Locp, v_Locp,ind_to_insert,z_first_bulk_material,v_first_bulk_material-left_shift)
                delta_length_left = (z_Locp[-1] - z_Locp[0]) - len_original_temp_left
            else:
                print('There was no a good fit between any peaks in the interface locpot and the  left bulk material locpot')
            indices_right[2] = indices_right[2] + (z_Locp[-1] - z_locp_length_original)
            if indices_right[3] > 0.85:
                ind_to_insert, pos_to_insert = find_closest_value_in_array(indices_right[2], z_Locp)
                z_Locp, v_Locp = insert_potential_into_position(z_Locp, v_Locp,ind_to_insert,z_sec_bulk_material,v_sec_bulk_material-right_shift)
                delta_length_right = (z_Locp[-1] - z_Locp[0]) - len_original_temp_left - delta_length_left
            else:
                print(
                    'There was no a good fit between any peaks in the interface locpot and the right bulk material locpot')

            self.locpot_vec_elongated = np.vstack((z_Locp, v_Locp))
            self.locpot_vec_elongated = to_2_column_mat(self.locpot_vec_elongated)
            if return_left_increment and not return_right_increment:
                return self.locpot_vec_elongated,delta_length_left
            elif return_right_increment and not return_left_increment:
                return self.locpot_vec_elongated, delta_length_right
            elif return_right_increment and  return_left_increment:
                return self.locpot_vec_elongated, delta_length_left,delta_length_right
            else:
                return self.locpot_vec_elongated
        else:
            if pos_to_insert is None:
                print('Please input as argument position in z where to start the elongation. If it is not supplied'
                      'the default is to elongate from the end of the vector')
                z_Locp, v_Locp = multiply_z_v_vecs(z_Locp, v_Locp, multi = multi_manual )
                pos_to_insert = z_Locp[-1]
            else:
                if z_to_insert_manual is None or v_to_insert_manual is None:
                    print('please provide z and v vectors to insert manually')
                    raise ValueError
                else:
        # Namely, we treat the system manually:
                    if self.Has_interface:
                        ref_point = pos_to_insert
                    z_to_insert_manual = cons.m2A(z_to_insert_manual)
                    v_to_insert_manual = cons.J2eV(v_to_insert_manual)
                    v_to_insert_global_min = np.min(v_to_insert_manual[2:-2])
                    locp_min_peaks_z,locp_min_peaks_v = find_peaks_minima(z_Locp,v_Locp,ignore_local_minima = True).T
                    if len(locp_min_peaks_z) == 0:
                        locp_min_peaks_z, locp_min_peaks_v = find_peaks_minima(z_Locp, v_Locp, ignore_local_minima=False).T
                    ind, pos = find_closest_value_in_array(pos_to_insert, locp_min_peaks_z)
                    if len(locp_min_peaks_v) <= 1:
                        v_locpot_global_min = locp_min_peaks_v[0]
                    else:
                        v_locpot_global_min = np.min([locp_min_peaks_v[ind-1],locp_min_peaks_v[ind],locp_min_peaks_v[ind+1]])
                    # Taking care of the vertical shifts between the system locpot and the going-to-be inserted locpot.
                    if v_to_insert_global_min >= v_locpot_global_min:
                        i = 1
                    else:
                        i = -1
                    if np.abs(np.log10(np.abs(v_to_insert_global_min))/np.log10(np.abs(v_locpot_global_min))) > 10:
                        v_to_insert_global_min = cons.J2eV(v_to_insert_global_min)
                        v_to_insert_manual = cons.J2eV(v_to_insert_manual)
                        v_shift = i * np.abs(v_to_insert_global_min - v_locpot_global_min)
                        v_to_insert_manual = v_to_insert_manual - v_shift
                    elif np.abs(np.log10(np.abs(v_to_insert_global_min))/np.log10(np.abs(v_locpot_global_min))) < 0.1:
                        v_to_insert_global_min = cons.eV2J(v_to_insert_global_min)
                        v_to_insert_manual = cons.eV2J(v_to_insert_manual)
                        v_shift = i * np.abs(v_to_insert_global_min - v_locpot_global_min)
                        v_to_insert_manual = v_to_insert_manual - v_shift
                    else:
                        v_shift = i * np.abs(v_to_insert_global_min - v_locpot_global_min)
                        v_to_insert_manual = v_to_insert_manual - v_shift

                    ind, pos = find_closest_value_in_array(pos_to_insert, z_Locp)
                    z_Locp, v_Locp = insert_potential_into_position(z_Locp, v_Locp,ind,z_to_insert_manual,v_to_insert_manual,multi=multi_manual )
                    locpot_vec_elongated = np.vstack((z_Locp, v_Locp))
                    locpot_vec_elongated = to_2_column_mat(locpot_vec_elongated)
                    delta_length_general = cons.m2A(z_Locp[-1] - z_Locp[0]) - len_original_temp_general
                    if return_right_increment or return_left_increment:
                        try:
                            return locpot_vec_elongated, delta_length_general,ref_point
                        except:
                            return locpot_vec_elongated, delta_length_general, z_Locp[-1]
                    else:
                        return locpot_vec_elongated
    def find_locpot_shift(self,locpot_vec = None, bulk_locpot_vec_first = None, bulk_locpot_vec_second = None):
        '''
        Finds the relative vertical shifts between the materials in the interface system and their corresponding
        bulk materials locpot.
        Afterwards, these value have to be substracted from the potential vector
        of the interface system in order to be inserted in the elongation procedure.

        Notes
        -----
        If your system does not have an interface, you should supply one of the arguments `bulk_locpot_vec_first` or `bulk_locpot_vec_second`
        with a locpot-formed vector.

        Parameters
        ----------
        locpot_vec : `numpy.ndarray`, (N,2), optional, default: None
                This is a two-column vector, the first column is for the spatial coordinates and the second column is for the local potential.
        bulk_locpot_vec_first : `numpy.ndarray`, (N,2), optional, default: None
                This is a two-column vector, the first column is for the spatial coordinates and the second column is for the local potential. This locpot matrix
                should describe the locpot matrix of the first bulk material.
        bulk_locpot_vec_second : `numpy.ndarray`, (N,2), optional, default: None
                This is a two-column vector, the first column is for the spatial coordinates and the second column is for the local potential. This locpot matrix
                should describe the locpot matrix of the second bulk material.
        Returns
        -------
        list, [float, float]
                The relative shifts of both the left and the right side materials.
                In the form of 2 floats -> [,] -> where [left_shift,right_shift].
                If the system does not contain an interface, it returns the shift only from the one part that was supplied.

        '''
        # if locpot_vec can be supplied as an argument, all the changes will take ation uppon it.
        # Otherwise they will affect only the locpot attribute of the class instance.
        if locpot_vec is None:
            zz = self.locpot_vec[:, 0]
            vv = self.locpot_vec[:, 1]
        else:
            zz = locpot_vec[:, 0]
            vv = locpot_vec[:, 1]
        interface_ind, interface = self.find_interface(zz, vv)
        peaks = find_peaks(zz, vv)

        # If our system contains an interface
        if self.Has_interface:
            # Taking care of the left hand side of the interface:
            z_left = np.array([z for i, z in enumerate(zz) if zz[i] < interface])
            v_left = np.array([v for i, v in enumerate(vv) if zz[i] < interface])
            z_left_minimas = find_peaks_minima(z_left, v_left)[:, 0]
            v_left_minimas = find_peaks_minima(z_left, v_left)[:, 1]
            mid_min_left =  np.int64(np.floor(len(v_left_minimas) / 2))
            tol_range_left = np.int64(0.2 * (np.floor(len(v_left_minimas))))
            v_left_global_min = np.min(v_left_minimas[mid_min_left - tol_range_left : mid_min_left + tol_range_left])
            # Taking care of the right hand side of the interface:
            z_right = np.array([z for i, z in enumerate(zz) if zz[i] > interface])
            v_right = np.array([v for i, v in enumerate(vv) if zz[i] > interface])
            z_right_minimas = find_peaks_minima(z_right, v_right)[:, 0]
            v_right_minimas = find_peaks_minima(z_right, v_right)[:, 1]
            mid_min_right =  np.int64(np.floor(len(v_right_minimas) / 2))
            tol_range_right = np.int64(0.2 * (np.floor(len(v_right_minimas))))
            v_right_global_min = np.min(v_right_minimas[mid_min_right - tol_range_right : mid_min_right + tol_range_right])

            # Loading the bulk-material locpots.
            if bulk_locpot_vec_first is None:
                try:
                    first_bulk_material = Locpot_yair(self.locpot_bulk_materials[0])
                except:
                    print('You did not succeeded to load the left bulk material locpot. try to handle it manully or fix it instead')
                    raise ValueError('You did not succeeded to load the left bulk material locpot. try to handle it manully or fix it instead')
                z_first_bulk = first_bulk_material.locpot_vec[:, 0]
                v_first_bulk = first_bulk_material.locpot_vec[:, 1]
            else:
                z_first_bulk = bulk_locpot_vec_first[:, 0]
                v_first_bulk = bulk_locpot_vec_first[:, 1]
            z_first_bulk_minimas = find_peaks_minima( z_first_bulk , v_first_bulk)[:, 0]
            v_first_bulk_minimas = find_peaks_minima(z_first_bulk, v_first_bulk)[:, 1]
            v_first_bulk_global_min = np.min(v_first_bulk_minimas)
            # Comparison for choosing whether to substract or adding the shift for the local potential.
            if v_first_bulk_global_min >= v_left_global_min:
                i = 1
            else:
                i = -1
            v_first_bulk_shift = i*np.abs(v_first_bulk_global_min - v_left_global_min)

            if bulk_locpot_vec_second is None:
                try:
                    sec_bulk_material = Locpot_yair(self.locpot_bulk_materials[1])
                except:
                    print('You did not succeeded to load the right bulk material locpot. try to handle it manully or fix it instead')
                    raise ValueError('You did not succeeded to load the right bulk material locpot. try to handle it manully or fix it instead')
                z_sec_bulk = sec_bulk_material.locpot_vec[:, 0]
                v_sec_bulk = sec_bulk_material.locpot_vec[:, 1]
            else:
                z_sec_bulk = bulk_locpot_vec_second[:, 0]
                v_sec_bulk = bulk_locpot_vec_second[:, 1]
            z_sec_bulk_minimas = find_peaks_minima(z_sec_bulk, v_sec_bulk)[:, 0]
            v_sec_bulk_minimas = find_peaks_minima(z_sec_bulk, v_sec_bulk)[:, 1]
            v_sec_bulk_global_min = np.min(v_sec_bulk_minimas)
            # Comparison for choosing whether to substract or adding the shift for the local potential.
            if v_sec_bulk_global_min >= v_right_global_min:
                i = 1
            else:
                i = -1
            v_sec_bulk_shift =  i* np.abs(v_sec_bulk_global_min - v_right_global_min)
            return v_first_bulk_shift, v_sec_bulk_shift
        else:
            # Namely, we does not have an interface in our system
            if bulk_locpot_vec_first is None and bulk_locpot_vec_second is None:
                print('You should supply at least one locpot in order to find the shifts')
                raise ValueError('You should supply at least one locpot in order to find the shifts')
            else:
                if not bulk_locpot_vec_first is None:
                    z_bulk =  bulk_locpot_vec_first[:, 0]
                    v_bulk =  bulk_locpot_vec_first[:, 1]
                elif not bulk_locpot_vec_second is None:
                    z_bulk =  bulk_locpot_vec_second[:, 0]
                    v_bulk =  bulk_locpot_vec_second[:, 1]
                # Taking care the bulk-like part of the comparison
                z_bulk_minimas = find_peaks_minima(z_bulk, v_bulk)[:, 0]
                v_bulk_minimas = find_peaks_minima(z_bulk, v_bulk)[:, 1]
                v_bulk_global_min = np.min(v_bulk_minimas)
                # Taking care the system part of the comparison
                z_minimas = find_peaks_minima(zz, vv)[:, 0]
                v_minimas = find_peaks_minima(zz, vv)[:, 1]
                mid_min = np.int64(np.floor(len(v_minimas) / 2))
                tol_range = np.int64(0.2 * (np.floor(len(v_minimas))))
                v_global_min = np.min(
                    v_minimas[mid_min_right - tol_range: mid_min + tol_range])
                # Comparison for choosing whether to substract or adding the shift for the local potential.
                if v_bulk_global_min >= v_global_min:
                    i = 1
                else:
                    i = -1
                v_bulk_shift = i * np.abs(v_bulk_global_min - v_global_min)
                return v_bulk_shift

def find_bulk_like_potential(z,v,interface_position, num_of_peaks = 3,limits = None, left = False, right = False):
    '''
    Notice that this is not a class method, it outside the scope of the class.

    Parameters
    ----------
    z : np.array
        Should be as the same size as wave_function vector. spatial coordinates vector.
    v : np.array
        Should be as the same size as wave_function vector. Local potential vector.
    interface_position : float
        The position where the interface is located. If you dont have an interface in your system,
        just input the `0` or the beginning position of the system.
    num_of_peaks : int, optional, default: 3
        If you have an interface, you can choose how many peaks to look for in the system locpot.
    limits : list\array_like, (float, float), optional, default: None
        This parameter is an optional for flexibility for chosing the range of where the pick the bulk-like potential.
        This should be input as a list of two floats, the first one is for the left limit and the second one is for the left limit.
        Should be given as the same units of the spatial coordainates vector, z.
    left : bool, optional, default: False
        A flag that determines whether to look at the left side hand of the system.
    right : bool, optional, default: False
        A flag that determines whether to look at the right side hand of the system.

    Returns
    -------
    np.array, np.array, float
        The first argument it returns is the spatial grid range where the bulk-like locpot was evaluated.
        The second argument it returns is the local potential range where the bulk-like locpot was evaluated.
        The last argument it returns is the start position where the bulk-like locpot was found.
    '''
    z_flag = np.all(z == cons.m2A(z))
    z = cons.m2A(z)
    interface_position = cons.m2A(interface_position)

    if right and interface_position > 0 and not left:
        v = v[z > interface_position]
        z = z[z > interface_position]

    elif left and interface_position  > 0 and not right:
        v = v[z < interface_position]
        z = z[z < interface_position]

    elif not left and not right:
        v = v[z > interface_position]
        z = z[z > interface_position]

    if not limits is None:
        limits = [cons.m2A(limits[0]),cons.m2A(limits[1])]
        if not len(limits) == 2:
            raise ValueError('You should supply the limits both for the right and the left sides of the chsoen region')
        else:
            pass
        if not limits[0] <= limits[1]:
            print('Notice that you supplied the borders in opposite order. I assume that you intend to the opposite order.')
            temp = limits[0]
            limits[0] = limits[1]
            limits[1] = temp
        else:
            pass

        if z[0] <= limits[0] <=z[-1] and z[0]<= limits[-1] <=z[-1]:
            pass
        else:
            if z[0] < 0.01 and limits[0] == 0 :
                limits[0] = z[0]
                if z[0] <= limits[0] <= z[-1] and z[0] <= limits[-1] <= z[-1]:
                    pass
                else:
                    if z[-1]*0.9 <= limits[-1] <= z[-1]*1.1:
                        limits[-1] = z[-1]
                        if z[0] <= limits[0] <= z[-1] and z[0] <= limits[-1] <= z[-1]:
                            pass
                        else:
                            raise ValueError('You should supply limits that are within the range of the spatial coordinates vector you supllied')
        v = v[(limits[0] < z) & (z < limits[1])]
        z = z[(limits[0] < z) & (z < limits[1])]
        if not z_flag:
            z = cons.A2m(z)



    peaks = find_peaks_minima(z,v,ignore_local_minima = True)
    z_peaks,v_peaks = peaks.T
    mid_peak_ind = np.int64(np.floor(len(z_peaks)/2))
    mid_peak_z = z_peaks[mid_peak_ind]
    mid_peak_v = v_peaks[mid_peak_ind]
    if not mid_peak_z - z_peaks[mid_peak_ind - np.int64(np.floor(num_of_peaks/2))] > 0:
        print('Your system is too small for searching bulk-like local potential trends, the results of this function for searching for bulk like locpot will be the vector itself')
        return z,v,z[0]
    z_start = z_peaks[mid_peak_ind - np.int64(np.floor(num_of_peaks/2))]
    if  not z_peaks[mid_peak_ind + np.int64(np.floor(num_of_peaks/2))] <= z_peaks[-1]:
        print(
            'Your system is too small for searching bulk-like local potential trends, the results of this function for searching for bulk like locpot will be the vector itself')
        return z, v,z[0]
    z_finish = z_peaks[mid_peak_ind + np.int64(np.floor(num_of_peaks/2))]
    z_to_return, v_to_return = fix_potential_edges(z[(z_start < z) & (z < z_finish)],v[(z_start < z) & (z < z_finish)])
    return z[(z_start < z) & (z < z_finish)], v [(z_start < z) & (z < z_finish)], z_start

def find_initial_position_to_initialize_next_to_interface(z,v,pos_inter,initi_side = 'Left',init_position = None):
    '''

    Parameters
    ----------
    z : np.array
        z spatial coordinates vector
    v : np.array
        Local potential vector.
    pos_inter : float
        The position where we want to initialize our wave-function next to. Usually will be the interface position if
        our system has one, otherwise - you can choose from where it begins.
    initi_side : str, {'Left', 'Right'}, optional, default: 'Left'
        Choices are in the bracket. It tells from where we sholud start and look for the next initialization point.
    init_position : float, optional, default: None
        In cases when we do not have an interface or want it to be initialized somewhere else.
        Must accompanied with `pos_inter=0`

    Returns
    -------
    z0 : float
        The initial position where to wave-fucntion is centered at.
    '''
    z = to_1D_vec(cons.A2m(z))
    v = to_1D_vec(cons.eV2J(v))
    temp = pos_inter
    pos_inter = cons.A2m(pos_inter)
    flag = temp == pos_inter # if it False, it means that the position was given in angstrum. So we should return it is angstrum.
    z_peaks_minima, v_peaks_minima = find_peaks_minima(z,v,ignore_local_minima = True).T
    z_peaks_minima = cons.A2m(z_peaks_minima)
    # If the interface position given here is 0, it means that the initialization can be only from the right side.
    if pos_inter == 0:
        initi_side = 'Right'
        if not init_position is None:
            init_position = cons.A2m(init_position)
            pos_inter = init_position

    # Initialization from the left side of the initialization position input.
    if initi_side == 'Left':
        z_peaks_minima = z_peaks_minima[z_peaks_minima < pos_inter]
        if len(z_peaks_minima) >= 3:
            z0 = z_peaks_minima[-3]
        elif len(z_peaks_minima) >= 2:
            z0 = z_peaks_minima[-2]
        else:
            z0 = z_peaks_minima[-2]
    # Initialization from the right side of the initialization position input.
    elif initi_side == 'Right':
        z_peaks_minima = z_peaks_minima[z_peaks_minima > pos_inter]
        if len(z_peaks_minima) >= 3:
            z0 = z_peaks_minima[2]
        elif len(z_peaks_minima) >= 2:
            z0 = z_peaks_minima[1]
        else:
            z0 = z_peaks_minima[0]
    if not flag:
        return cons.m2A(z0)
    return z0

def insert_potential_into_position(z_vec_original, v_vec_original, index_to_insert, z_vec_to_insert, v_vec_to_insert,
                                   multi=0):
    '''
    Very not elegant and complex function.
    It should be primitive. It does not looking for something, but just gets as input all the needed parameters
    and insert all the vectors at the right place where it was asked to.

    Parameters
    ----------
    z_vec_original : np.array
        The coords vector whom we wish to insert the other vector.
    v_vec_original :  np.array
        The potential vector whom we wish to insert the other vector.
    index_to_insert : int
        The index respect to the z_original_vec where from him and further we
        are going to insert the desired vector.
    z_vec_to_insert : np.array
        The new coords vector we wish insert into the original vector.
    v_vec_to_insert : np.array
        The new potential vector we wish insert into the original vector.
    multi : int, optional, default: 0
        When the default value is `0`, it means that there is no multiplication.
        Describes how many time we would like to insert the vector.

    Returns
    -------
    np.array, np.array
        The first one is the new elongated coords vector. The second one is the new elongated potential vector.
    '''
    # Input verification handling
    # .......................................................................
    z_vec_original = to_1D_vec(z_vec_original)
    v_vec_original = to_1D_vec(v_vec_original)
    z_vec_to_insert = to_1D_vec(z_vec_to_insert)
    v_vec_to_insert = to_1D_vec(v_vec_to_insert)
    try:
        z_vec_to_insert, v_vec_to_insert = fix_potential_edges(z_vec_to_insert, v_vec_to_insert)
    except ValueError:
        pass
    z_vec_to_insert, v_vec_to_insert = multiply_z_v_vecs(z_vec_to_insert, v_vec_to_insert, multi=multi)
    try:
        z_vec_to_insert, v_vec_to_insert = fix_potential_edges(z_vec_to_insert, v_vec_to_insert)
    except ValueError:
        pass
    z_vec_to_insert = cons.m2A(z_vec_to_insert)
    z_vec_original = cons.m2A(z_vec_original)
    original_grid_density =len(z_vec_original)/(z_vec_original[-1]-z_vec_original[0])
    z_vec_to_insert, v_vec_to_insert = adjust_grid_density(original_grid_density,z_vec_to_insert, v_vec_to_insert)
    insert_to_the_end = False
    if index_to_insert == len(v_vec_original) - 1:
        insert_to_the_end = True
    # .......................................................................
    # The normal case, where we don't insert at the end of the locpot
    if not insert_to_the_end:
        # The treatment here is to divide our locpot vector into 2 seperated parts, and handle these two part
        # separately. In between them we then insert the locpot we wish, and eventually put them all together into
        # one locpot vector.
        # The first part before the insertion is the locpot vector from its beginning to the index of insertion.
        # The second part before the insertion is the locpot vector from one index after the insertion index till the end.
        first_part_z_original = z_vec_original[0:index_to_insert+1]
        second_part_z_original = z_vec_original[index_to_insert+2::]
        first_part_v_original = v_vec_original[0:index_to_insert+1]
        second_part_v_original = v_vec_original[index_to_insert+2::]
        def fix_edges(z,v,ending = False, starting = False):
            # It is a very complicated function. It was built to handle the edges issues stem from the
            # cutting and inserting operations.
            # It also tries to handle cases where the peaks are in more complicated form with sub-peaks or local minima/maxima.

            # minima / maxima global and all kind of peaks including local ones.
            if starting:
                minima_global = find_peaks_minima(z, v, ignore_local_minima=True, prominence=get_prominence(z, v, num_of_min=3))
            else:
                minima_global = find_peaks_minima(z, v, ignore_local_minima=True)
            maxima_global = find_peaks_maxima(z, v,ignore_local_maxima=True)
            minima_tot = find_peaks_minima(z, v, ignore_local_minima=False)
            maxima_tot = find_peaks_maxima(z, v, ignore_local_maxima=False)
            minima_tot_z = minima_tot[:,0]
            minima_tot_v = minima_tot[:,1]
            maxima_tot_z = maxima_tot[:,0]
            maxima_tot_v = maxima_tot[:,1]
            minima_z = minima_global[:, 0]
            minima_v = minima_global[:, 1]
            maxima_z = maxima_global[:, 0]
            maxima_v = maxima_global[:, 1]
            if len(maxima_z) == 0 or len(minima_z) == 0 or len(maxima_tot_z) == 0 or len(minima_tot_z) == 0:
                if np.all(v[1:] >= v[:-1]) or np.all(v[1:] <= v[:-1]):
                    return z,v
                else:
                    z_original_begin = z[0]
                    z_original_end = z[-1]
                    v_original_begin = v[0]
                    v_original_end = v[-1]
                    v_temp = np.copy(v)
                    z_temp = np.copy(z)
                    z_dz = cons.m2A(np.diff(z)[0])
                    flag_z = np.all(z_temp == cons.m2A(z_temp))
                    flag_v = np.all(v_temp == cons.J2eV(v_temp))
                    if v[0] > v[-1]:
                    # We have to take care of the beginning since it higher
                        height_difference = cons.J2eV(v[0] - v[-1])
                        slope_from_right = height_difference/z_dz
                        ind_temp,pos_temp = find_closest_value_in_array(v[0],v[np.int64(np.floor(len(v)/2))::])
                        difference = (np.floor(len(v / 2)))
                        ind_temp = ind_temp + difference -1
                        dz_steps = len(v) - ind_temp + 1
                        temp_additive_step_z = z_original_end
                        temp_additive_step_v = v_original_begin
                        z_comp = np.array([])
                        v_comp = np.array([])
                        for i in dz_steps:
                            temp_additive_step_z += z_dz
                            temp_additive_step_v -= (slope_from_right/z_dz)*i
                            z_comp = np.append((z_comp,temp_additive_step_z))
                            v_comp = np.append((temp_additive_step_v,v_comp))
                        if not flag_z:
                            z_comp = cons.A2m(z_comp)
                        if not flag_v:
                            v_comp = cons.eV2J(v_comp)
                        v_temp = np.append((v_comp,v_temp))
                        z_temp = np.append((z_temp,z_comp))
                        z_temp,v_temp = interpolate_pchip(len(z_temp),z_temp,v_temp)
                    elif v[0] < v[-1]:
                # We have to take care of the ending since it higher
                        height_difference = cons.J2eV(v[-1] - v[1])
                        slope_from_left = height_difference/z_dz
                        ind_temp,pos_temp = find_closest_value_in_array(v[-1],v[::np.int64(np.floor(len(v)/2))])
                        difference = (np.floor(len(v / 2)))
                        dz_steps = ind_temp + 1
                        temp_additive_step_z = z_original_end
                        temp_additive_step_v = v_original_end
                        z_comp = np.array([])
                        v_comp = np.array([])
                        for i in dz_steps:
                            temp_additive_step_z += z_dz
                            temp_additive_step_v -= (slope_from_left/z_dz)*i
                            z_comp = np.append((z_comp,temp_additive_step_z))
                            v_comp = np.append((v_comp,temp_additive_step_v))
                        if not flag_z:
                            z_comp = cons.A2m(z_comp)
                        if not flag_v:
                            v_comp = cons.eV2J(v_comp)
                        v_temp = np.append((v_temp,v_comp))
                        z_temp = np.append((z_temp,z_comp))
                        z_temp,v_temp = interpolate_pchip(len(z_temp),z_temp,v_temp)
                    return z_temp,v_temp
            # each time we treat each part of the locpot. This section relates to the ending, namely - to the part from the insertion index to
            # the end of the locpot vector.
            if ending:
                # First we find the positions of the minima and maxima points when starting from the last maxima point of the whole locpot.
                # It will will search from the end a minima-maxima pair, but global points like these, and then it
                # would cut the range that in between them. Then it will be able to paste this cut-sub-vector at the region of the insertion for fixing its the edges.
                temp = find_adjacent_minima_maxima(z,v,maxima_z[-1],prominence=get_prominence(z,v,num_of_min=-1,is_max = True))
                tot_last_maxima = maxima_tot_z[-1]
                index_tot_last_maxima, tot_last_maxima = find_closest_value_in_array(tot_last_maxima,z)
                last_maxima_global = temp[1][1]
                index_last_maxima_global = temp[1][0]
                minima_before_last_maxima = temp[0][1]
                index_minima_before_last_maxima = temp[0][0]
                ending_vector_z = z[index_minima_before_last_maxima:index_last_maxima_global+1]
                inde=1
                while len(ending_vector_z) == 0 and inde < len(z)-1:
                    temp = find_adjacent_minima_maxima(z, v, maxima_z[-1-inde],
                                                       prominence=get_prominence(z, v, num_of_min=-1,is_max=True))
                    tot_last_maxima = maxima_tot_z[-1]
                    index_tot_last_maxima, tot_last_maxima = find_closest_value_in_array(tot_last_maxima, z)
                    last_maxima_global = temp[1][1]
                    index_last_maxima_global = temp[1][0]
                    minima_before_last_maxima = temp[0][1]
                    index_minima_before_last_maxima = temp[0][0]
                    ending_vector_z = z[index_minima_before_last_maxima:index_last_maxima_global + 1]
                    inde +=1
                if len(ending_vector_z) == 0:
                    raise ValueError('Check Your peaks detection')
                if tot_last_maxima > last_maxima_global:
                    ending_vector_z = ending_vector_z[-1] - ending_vector_z + tot_last_maxima
                    ending_vector_z = ending_vector_z[-1::-1]
                else:
                    ending_vector_z = ending_vector_z + ending_vector_z[-1] - ending_vector_z[0]
                ending_vector_v = v[index_minima_before_last_maxima:index_last_maxima_global+1]
                ending_vector_v = ending_vector_v[-1::-1]
                if tot_last_maxima > last_maxima_global:
                    z = np.delete(z, np.s_[index_tot_last_maxima::])
                    v = np.delete(v, np.s_[index_tot_last_maxima::])
                else:
                    z = np.delete(z, np.s_[index_last_maxima_global::])
                    v = np.delete(v, np.s_[index_last_maxima_global::])
                z = np.append(z, ending_vector_z)
                v = np.append(v, ending_vector_v)
            elif starting:
                # The same here. First we find the positions of the maxima and minima points when starting from the first maxima point of the whole locpot.
                # It will will search from the beginning a maxima-minima pair, but global points like these, and then it
                # would cut the range that in between them. Then it will be able to paste this cut-sub-vector at the region of the insertion for fixing its the edges.
                temp = find_adjacent_minima_maxima(z, v, maxima_z[0],reverse = True)
                tot_first_maxima = maxima_tot_z[0]
                index_tot_first_maxima, tot_first_maxima = find_closest_value_in_array(tot_first_maxima,z)
                first_maxima = temp[0][1]
                index_first_maxima = temp[0][0]
                first_minima_after = temp[1][1]
                index_first_minima_after = temp[1][0]

                starting_vector_z = z[index_first_maxima:index_first_minima_after+1]
                if tot_first_maxima <=  first_maxima:
                    starting_vector_z = np.abs(starting_vector_z[-1::-1] - starting_vector_z[-1]) + starting_vector_z[0] - (first_minima_after - tot_first_maxima)
                else:
                    starting_vector_z = np.abs(starting_vector_z[-1::-1] - starting_vector_z[-1] ) + starting_vector_z[0]
                starting_vector_v = v[index_first_maxima:index_first_minima_after + 1]
                starting_vector_v = starting_vector_v[-1::-1]
                if tot_first_maxima < first_maxima:
                    z = np.delete(z, np.s_[0:index_tot_first_maxima+1])
                    v = np.delete(v, np.s_[0:index_tot_first_maxima+1])
                else:
                    z = np.delete(z, np.s_[0:index_first_maxima+1])
                    v = np.delete(v, np.s_[0:index_first_maxima+1])
                z = np.append(starting_vector_z, z)
                v = np.append(starting_vector_v, v)
            return z,v

        first_part_z_original, first_part_v_original = fix_edges(first_part_z_original, first_part_v_original, ending = True)
        second_part_z_original, second_part_v_original = fix_edges(second_part_z_original, second_part_v_original, starting = True)
        second_part_z_original = second_part_z_original +  z_vec_to_insert[-1] - z_vec_to_insert[0]
        new_z_vec = np.append(first_part_z_original,z_vec_to_insert)
        new_z_vec = np.append(new_z_vec,second_part_z_original )
        new_z_vec = np.linspace(z_vec_original[0],z_vec_original[-1] + z_vec_to_insert[-1] - z_vec_to_insert[0] -z_vec_original[0]  ,len(new_z_vec))
        new_v_vec = np.append(first_part_v_original,v_vec_to_insert)
        new_v_vec = np.append(new_v_vec,second_part_v_original )

    #  Namely - the case when we inserting to the end
    else:
        new_z_vec = np.append(z_vec_original, z_vec_to_insert)
        new_z_vec[(len(z_vec_original) - 1):] = new_z_vec[(len(z_vec_original) - 1):] + z_vec_original[-1]
        new_v_vec = np.append(v_vec_original, v_vec_to_insert)
    return to_1D_vec(new_z_vec), to_1D_vec(new_v_vec)



def fix_potential_edges(z, v):
    '''

    Parameters
    ----------
    z : np.array
        Represents the spatial coords vector.
    v : np.array
        Represnts the v local potential vector.

    Returns
    -------
    new_z : np.array
        The new z coordinates with matching number of samples with respect with
        the fixed potential vector.
    new_v : np.array
        The new v potential vector after its edges were fixed to be well suitable
        to be stiched.
    '''
    # Let's define the form of the first and the last peak
    # These are the arrays for all the peaks (minimu, and maximum) for both local and global.
    # tot - means global and local. global - will be only global, local - will be only local
    def fix_density(z,v,new_v):
        N_fix = len(new_v) - len(v)
        diff_z = np.diff(z)[0]
        max_z = z[-1]
        new_z_end = max_z + N_fix * diff_z
        N_new = np.int64(len(new_v))
        new_z = np.linspace(z[0], new_z_end, N_new)
        new_z, new_v = interpolate_pchip(N_new, to_1D_vec(new_z), to_1D_vec(new_v))
        return new_z, new_v

    N_original = len(v)-1
    diff_z = np.diff(z)[0]
    max_z = z[-1]
    minima_tot = find_peaks_minima(z, v)
    maxima_tot = find_peaks_maxima(z, v)
    original_z,original_v = z,v # for debugging
    if len(minima_tot[:,0]) <1 or len(maxima_tot[:,0]) <1:
        return z,v
    minima_z_tot  = minima_tot[:, 0]
    minima_v_tot = minima_tot[:, 1]
    maxima_z_tot = maxima_tot[:, 0]
    maxima_v_tot = maxima_tot[:, 1]
    promin = get_prominence(z,v,num_of_min=1)
    minima_global = find_peaks_minima(z, v, ignore_local_minima = True,prominence=promin)
    maxima_global = find_peaks_maxima(z, v, ignore_local_maxima = True)
    if len(minima_global[:,0]) <1 or len(maxima_global[:,0]) <1:
        return z,v
    minima_z_global  = minima_global[:, 0]
    minima_v_global = minima_global[:, 1]
    maxima_z_global = maxima_global[:, 0]
    maxima_v_global = maxima_global[:, 1]
    if len(minima_z_global) >= 15 or len(maxima_z_global) >= 15:
        return z, v
    minima_z_local =  [i for i in minima_z_tot if i not in minima_z_global]
    minima_v_local =  [ minima_v_tot[n]  for n,i in enumerate(minima_z_tot) if i not in minima_z_global]
    maxima_z_local =  [i for i in maxima_z_tot if i not in maxima_z_global]
    maxima_v_local =  [ maxima_v_tot[n]  for n,i in enumerate(maxima_z_tot) if i not in maxima_z_global]

    main_peak_is_minima = False
    main_peak_is_maxima = False
    simple_peak = False
    # Checking for if the peak is a simple type of peak (sinusidual peak)
    if np.abs(len(minima_z_global)-len(minima_z_tot))<=1 and np.abs(len(maxima_z_global)-len(maxima_z_tot))<=1:
        simple_peak=True
    elif z[0] ==  minima_z_tot[0] or z[0] ==  maxima_z_tot[0]:
        if z[0] ==  minima_z_tot[0]:
            z = z[1:]
            minima_z_tot = minima_z_tot[1:]
        elif z[0] ==  maxima_z_tot[0]:
            z = z[1:]
            maxima_z_tot = maxima_z_tot[1:]
    if not simple_peak and np.abs(z[0] - minima_z_tot[0]) > np.abs(z[0] - maxima_z_tot[0]):
    # The beginning of the vector is closer to a maximum point
        main_peak_is_maxima = True
    elif not simple_peak:
    # The beginning of the vector is closer to a minimum point
        main_peak_is_minima = True
    if main_peak_is_maxima:
        (ind_maxima_first, pos_maxima_first),  (ind_minima_first, pos_minima_first) = find_adjacent_minima_maxima(z, v, minima_z_global[0], reverse=True)
        (ind_minima_sec, pos_minima_sec), (ind_maxima_sec, pos_maxima_sec) = find_adjacent_minima_maxima(z, v, minima_z_global[-1], reverse=False)
        ind_first_maxima,pos_first_maxima = find_closest_value_in_array(maxima_z_tot[0],z)
        z_to_be_inserted = z[ind_maxima_first:ind_minima_first+1][-1] - np.flip(z[ind_maxima_first:ind_minima_first+1])+z[0]
        z = np.delete(z ,np.s_[:ind_first_maxima+1] )
        z=np.append(z_to_be_inserted,z)
        v_to_be_inserted = np.flip(v[ind_maxima_first:ind_minima_first+1])
        v = np.delete(v, np.s_[:ind_first_maxima + 1])
        v = np.append(v_to_be_inserted,v)

        ind_last_maxima,pos_last_maxima = find_closest_value_in_array(maxima_z_tot[-1],z)
        try:
            z_to_be_inserted = z[ind_minima_sec:ind_maxima_sec+1]+z[ind_last_maxima]-z[ind_minima_sec:ind_maxima_sec+1][0]
        except IndexError:
            (ind_maxima_first, pos_maxima_first), (ind_minima_first, pos_minima_first) = find_adjacent_minima_maxima(z,v,minima_z_global[0],reverse=True,prominence=get_prominence(z,v,num_of_min=2,is_max = True))
            (ind_minima_sec, pos_minima_sec), (ind_maxima_sec, pos_maxima_sec) = find_adjacent_minima_maxima(z, v,minima_z_global[-1],reverse=False)
            ind_first_maxima, pos_first_maxima = find_closest_value_in_array(maxima_z_tot[0], z)
            z_to_be_inserted = z[ind_maxima_first:ind_minima_first + 1][-1] - np.flip(
                z[ind_maxima_first:ind_minima_first + 1]) + z[0]
            z = np.delete(z, np.s_[:ind_first_maxima + 1])
            z = np.append(z_to_be_inserted, z)
            v_to_be_inserted = np.flip(v[ind_maxima_first:ind_minima_first + 1])
            v = np.delete(v, np.s_[:ind_first_maxima + 1])
            v = np.append(v_to_be_inserted, v)
            try:
                z_to_be_inserted = z[ind_minima_sec:ind_maxima_sec + 1] + z[ind_last_maxima] - z[ind_minima_sec:ind_maxima_sec + 1][0]
            except IndexError:
                (ind_maxima_first, pos_maxima_first), (ind_minima_first, pos_minima_first) = find_adjacent_minima_maxima(z, v, minima_z_global[0],reverse=True,prominence=get_prominence(z, v,num_of_min=3,is_max=True))
                (ind_minima_sec, pos_minima_sec), (ind_maxima_sec, pos_maxima_sec) = find_adjacent_minima_maxima(z, v,minima_z_global[-1],reverse=False)
                ind_first_maxima, pos_first_maxima = find_closest_value_in_array(maxima_z_tot[0], z)
                z_to_be_inserted = z[ind_maxima_first:ind_minima_first + 1][-1] - np.flip(z[ind_maxima_first:ind_minima_first + 1]) + z[0]
                z = np.delete(z, np.s_[:ind_first_maxima + 1])
                z = np.append(z_to_be_inserted, z)
                v_to_be_inserted = np.flip(v[ind_maxima_first:ind_minima_first + 1])
                v = np.delete(v, np.s_[:ind_first_maxima + 1])
                v = np.append(v_to_be_inserted, v)
                try:
                    z_to_be_inserted = z[ind_minima_sec:ind_maxima_sec + 1] + z[ind_last_maxima] - z[ind_minima_sec:ind_maxima_sec + 1][0]
                except IndexError:
                    (ind_maxima_first, pos_maxima_first), (ind_minima_first, pos_minima_first) = find_adjacent_minima_maxima(z, v, minima_z_global[1],reverse=True,prominence=get_prominence(z,v,num_of_min=2,is_max = True))
                    (ind_minima_sec, pos_minima_sec), (ind_maxima_sec, pos_maxima_sec) = find_adjacent_minima_maxima(z,v,minima_z_global[-2],reverse=False)
                    ind_first_maxima, pos_first_maxima = find_closest_value_in_array(maxima_z_tot[0], z)
                    z_to_be_inserted = z[ind_maxima_first:ind_minima_first + 1][-1] - np.flip(z[ind_maxima_first:ind_minima_first + 1]) + z[0]
                    z = np.delete(z, np.s_[:ind_first_maxima + 1])
                    z = np.append(z_to_be_inserted, z)
                    v_to_be_inserted = np.flip(v[ind_maxima_first:ind_minima_first + 1])
                    v = np.delete(v, np.s_[:ind_first_maxima + 1])
                    v = np.append(v_to_be_inserted, v)
                try:
                    z_to_be_inserted = z[ind_minima_sec:ind_maxima_sec + 1] + z[ind_last_maxima] - z[ind_minima_sec:ind_maxima_sec + 1][0]
                except IndexError:
                    print('You had issue in fixing the edges')
                    raise ValueError
        z = np.delete(z ,np.s_[ind_last_maxima:])
        z=np.append(z,z_to_be_inserted)
        v_to_be_inserted = np.flip(v[ind_minima_sec:ind_maxima_sec+1])
        v = np.delete(v, np.s_[ind_last_maxima:])
        v = np.append(v,v_to_be_inserted)

    if main_peak_is_minima:
        (ind_minima_first, pos_minima_first),  (ind_maxima_first, pos_maxima_first) = find_adjacent_minima_maxima(z, v, minima_z_global[0], reverse=False)
        (ind_maxima_sec, pos_maxima_sec), (ind_minima_sec, pos_minima_sec) = find_adjacent_minima_maxima(z, v, minima_z_global[-1], reverse=True)
        ind_first_minima,pos_first_minima = find_closest_value_in_array(minima_z_tot[0],z)
        z_to_be_inserted = z[ind_minima_first:ind_maxima_first+1][-1] - np.flip(z[ind_minima_first:ind_maxima_first+1])
        z = np.delete(z ,np.s_[:ind_first_minima] )
        z=np.append(z_to_be_inserted,z)
        v_to_be_inserted = np.flip(v[ind_minima_first:ind_maxima_first+1])
        v = np.delete(v, np.s_[:ind_first_minima])
        v = np.append(v_to_be_inserted,v)

        ind_last_minima,pos_last_minima = find_closest_value_in_array(minima_z_tot[-1],z)
        z_to_be_inserted = z[ind_maxima_sec:ind_minima_sec+1]+z[ind_last_minima]-z[ind_maxima_sec:ind_minima_sec+1][0]
        z = np.delete(z ,np.s_[ind_last_minima:])
        z=np.append(z,z_to_be_inserted)
        v_to_be_inserted = np.flip(v[ind_maxima_sec:ind_minima_sec+1])
        v = np.delete(v, np.s_[ind_last_minima:])
        v = np.append(v,v_to_be_inserted)

    if simple_peak:
        minima = find_peaks_minima(z, v)
        maxima = find_peaks_maxima(z, v)
        if len(minima[:,0]) <1 or len(maxima[:,0]) <1:
            return z,v
        minima_z  = minima[:, 0]
        minima_v = minima[:, 1]
        maxima_z = maxima[:, 0]
        maxima_v = maxima[:, 1]
        first_maxima = maxima_z[0]
        first_maxima_index = np.int64([i for i in range(0, len(z)) if z[i] == first_maxima][0])
        last_maxima = maxima_z[-1]
        last_maxima_index = np.int64([i for i in range(0, len(z)) if z[i] == last_maxima][0])
        if np.abs(v[-1]) > np.abs(v[0]):

            v_vector_ending = v[last_maxima_index:][::-1]
            new_v = np.append(v_vector_ending, v[first_maxima_index + 1:])
        elif np.abs(v[-1]) < np.abs(v[0]):
            v_vector_starting = v[:first_maxima_index + 1][::-1]
            new_v = np.append(v[:last_maxima_index], v_vector_starting)
        else:
            new_v = v
        N_fix = len(new_v) - len(v)
        diff_z = np.diff(z)[0]
        max_z = z[-1]
        new_z_end = max_z + N_fix * diff_z
        N_new = np.int64(len(new_v))
        new_z = np.linspace(z[0], new_z_end, N_new)
        new_z, new_v = interpolate_pchip(N_new, to_1D_vec(new_z), to_1D_vec(new_v))

        middle_min_num = np.int64(np.round(len(minima_v) / 2))
        if new_v[0] > minima_v[middle_min_num] or new_v[0] > minima_v[middle_min_num - 1]:
            min_v = np.min([minima_v[middle_min_num - 1], minima_v[middle_min_num]])
            minima_z = find_peaks_minima(new_z,new_v)[:, 0]
            minima_v = find_peaks_minima(new_z,new_v)[:, 1]
            maxima_z = find_peaks_maxima(new_z,new_v)[:, 0]
            maxima_v = find_peaks_maxima(new_z,new_v)[:, 1]

            ind_min_v, pos_min_v = find_closest_value_in_array(min_v, new_v)
            next_maxima_z = maxima_z[maxima_z > new_z[ind_min_v]][0]
            next_maxima_v = maxima_v[maxima_z > new_z[ind_min_v]][0]
            ind_next_maxima, pos_next_maxima = find_closest_value_in_array(next_maxima_z, new_z)
            new_v_start_vec = new_v[ind_min_v:ind_next_maxima + 1]
            new_z_start_vec = np.abs(new_z[ind_min_v:ind_next_maxima + 1] - new_z[ind_min_v]) + new_z[0]
            first_maxima_z_ind, first_maxima_z_pos = find_closest_value_in_array(maxima_z[0], new_z)
            new_z = np.delete(new_z,np.s_[0:first_maxima_z_ind+1])
            new_v = np.delete(new_v, np.s_[0:first_maxima_z_ind+1])
            new_z = np.append(new_z_start_vec,new_z)
            new_v = np.append(new_v_start_vec, new_v)

            maxima_z = find_peaks_maxima(new_z,new_v)[:, 0]
            maxima_v = find_peaks_maxima(new_z,new_v)[:, 1]
            ind_last_maxima, pos_last_maxima = find_closest_value_in_array(maxima_z[-1],new_z)
            new_z = np.delete(new_z,np.s_[ind_last_maxima::])
            new_v = np.delete(new_v, np.s_[ind_last_maxima::])
            new_z = np.append(new_z,new_z_start_vec+pos_last_maxima-new_z_start_vec[0])
            new_v = np.append(new_v, new_v_start_vec[-1::-1])
            return new_z, new_v

    if len(v) - N_original >=0:
        N_fix = len(v) - N_original
        new_z_end = max_z + N_fix * diff_z
        N_new = np.int64(len(v))
    else:
        N_fix = N_original-len(v)
        new_z_end = max_z - N_fix * diff_z
        N_new = np.int64(len(v))
    new_z = np.linspace(z[0], new_z_end, N_new)
    new_z, new_v = interpolate_pchip(N_new, to_1D_vec(new_z), to_1D_vec(v))
    return new_z, new_v
# def fix_potential_edges(z, v):
#     '''
#
#     Parameters
#     ----------
#     z : np.array
#         Represents the spatial coords vector.
#     v : np.array
#         Represnts the v local potential vector.
#
#     Returns
#     -------
#     new_z : np.array
#         The new z coordinates with matching number of samples with respect with
#         the fixed potential vector.
#     new_v : np.array
#         The new v potential vector after its edges were fixed to be well suitable
#         to be stiched.
#     '''
#     minima = find_peaks_minima(z, v)
#     maxima = find_peaks_maxima(z, v)
#     if len(minima[:,0]) <1 or len(maxima[:,0]) <1:
#         return z,v
#     minima_z  = minima[:, 0]
#     minima_v = minima[:, 1]
#     maxima_z = maxima[:, 0]
#     maxima_v = maxima[:, 1]
#     first_maxima = maxima_z[0]
#     first_maxima_index = np.int64([i for i in range(0, len(z)) if z[i] == first_maxima][0])
#     last_maxima = maxima_z[-1]
#     last_maxima_index = np.int64([i for i in range(0, len(z)) if z[i] == last_maxima][0])
#     if np.abs(v[-1]) > np.abs(v[0]):
#
#         v_vector_ending = v[last_maxima_index:][::-1]
#         new_v = np.append(v_vector_ending, v[first_maxima_index + 1:])
#     elif np.abs(v[-1]) < np.abs(v[0]):
#         v_vector_starting = v[:first_maxima_index + 1][::-1]
#         new_v = np.append(v[:last_maxima_index], v_vector_starting)
#     else:
#         new_v = v
#     N_fix = len(new_v) - len(v)
#     diff_z = np.diff(z)[0]
#     max_z = z[-1]
#     new_z_end = max_z + N_fix * diff_z
#     N_new = np.int64(len(new_v))
#     new_z = np.linspace(z[0], new_z_end, N_new)
#     new_z, new_v = interpolate_pchip(N_new, to_1D_vec(new_z), to_1D_vec(new_v))
#
#     middle_min_num = np.int64(np.round(len(minima_v) / 2))
#     if new_v[0] > minima_v[middle_min_num] or new_v[0] > minima_v[middle_min_num - 1]:
#         min_v = np.min([minima_v[middle_min_num - 1], minima_v[middle_min_num]])
#         minima_z = find_peaks_minima(new_z,new_v)[:, 0]
#         minima_v = find_peaks_minima(new_z,new_v)[:, 1]
#         maxima_z = find_peaks_maxima(new_z,new_v)[:, 0]
#         maxima_v = find_peaks_maxima(new_z,new_v)[:, 1]
#
#         ind_min_v, pos_min_v = find_closest_value_in_array(min_v, new_v)
#         next_maxima_z = maxima_z[maxima_z > new_z[ind_min_v]][0]
#         next_maxima_v = maxima_v[maxima_z > new_z[ind_min_v]][0]
#         ind_next_maxima, pos_next_maxima = find_closest_value_in_array(next_maxima_z, new_z)
#         new_v_start_vec = new_v[ind_min_v:ind_next_maxima + 1]
#         new_z_start_vec = np.abs(new_z[ind_min_v:ind_next_maxima + 1] - new_z[ind_min_v]) + new_z[0]
#         first_maxima_z_ind, first_maxima_z_pos = find_closest_value_in_array(maxima_z[0], new_z)
#         new_z = np.delete(new_z,np.s_[0:first_maxima_z_ind+1])
#         new_v = np.delete(new_v, np.s_[0:first_maxima_z_ind+1])
#         new_z = np.append(new_z_start_vec,new_z)
#         new_v = np.append(new_v_start_vec, new_v)
#
#         maxima_z = find_peaks_maxima(new_z,new_v)[:, 0]
#         maxima_v = find_peaks_maxima(new_z,new_v)[:, 1]
#         ind_last_maxima, pos_last_maxima = find_closest_value_in_array(maxima_z[-1],new_z)
#         new_z = np.delete(new_z,np.s_[ind_last_maxima::])
#         new_v = np.delete(new_v, np.s_[ind_last_maxima::])
#         new_z = np.append(new_z,new_z_start_vec+pos_last_maxima-new_z_start_vec[0])
#         new_v = np.append(new_v, new_v_start_vec[-1::-1])
#
#     return new_z, new_v


def multiply_z_v_vecs(z_vec_original, v_vec_original, multi):
    '''

    Parameters
    ----------
    z_vec_original : np.array
        The spatial coordinates vector whom we wish to multiply.
    v_vec_original :  np.array
        The potential vector whom we wish to multiply.
    multi : int
        Describes how many time we would like to multiply the vector.

    Returns
    -------
    np.array, np.array
        The first array is the new multiplied spatial coordinates vector. The second array is the new multiplied local potential vector.
    '''

    multi = np.int64(multi)
    try:
        z_vec_original, v_vec_original = fix_potential_edges(z_vec_original, v_vec_original)
    except ValueError:
        pass
    z_vec_original = to_1D_vec(z_vec_original)
    v_vec_original = to_1D_vec(v_vec_original)

    assert len(z_vec_original) == len(
        v_vec_original), 'size of the coords vec must be the same as the potential vector.'
    z_max_initial = z_vec_original[-1]
    z_min_initial = z_vec_original[0]
    z_vec_new = np.copy(z_vec_original)
    v_vec_new = np.copy(v_vec_original)
    for i in range(1, multi + 1, 1):
        z_max = i * z_max_initial
        z_min = i * z_min_initial
        z_vec_new = np.append(z_vec_new, (z_max - z_min + z_vec_original))
        v_vec_new = np.append(v_vec_new, v_vec_original)
    return z_vec_new, v_vec_new


# def fit_sin(zz, vv, N=1):
#     '''
#
#     Fit sinusodial potential vector to the input spatial sequence coordinates.
#     Parameters
#     ----------
#     zz : 1D np.array
#         Represents the z coords vector.
#     vv : 1D np.array
#         Represents the v potential vector.
#     N : int.
#        Number os sinusiduals to approximate. suppose to suit the number of species in the material.
#     Returns
#     -------
#      Dictionary.
#          Contains fitting data: "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"
#
#      1D np.array
#         1D np.array of the new fitted v potential vector.
#     '''
#     Number_of_sinus = N
#     if Number_of_sinus == 1:
#         zz = np.array(zz)
#         vv = np.array(vv)
#         ff = np.fft.fftfreq(len(zz), (zz[1] - zz[0]))  # assume uniform spacing
#         Fvv = abs(np.fft.fft(vv))
#         guess_freq = abs(ff[np.argmax(Fvv[1:]) + 1])  # excluding the zero frequency "peak", which is related to offset
#         guess_amp = np.std(vv) * 2. ** 0.5
#         guess_offset = np.mean(vv)
#         guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])
#
#         def sinfunc(z, A, w, p, c):
#             return A * np.sin(w * z + p) + c
#
#         popt, pcov = curve_fit(sinfunc, zz, vv, p0=guess)
#         A, w, p, c = popt
#         f = w / (2. * np.pi)
#         fitfunc = lambda z: A * np.sin(w * z + p) + c
#         new_fitted_func = fitfunc(zz)
#         maximas_new_fitted_func = find_peaks_maxima(zz, new_fitted_func)[:, 1]
#         maximas_z_original = find_peaks_maxima(zz, vv)[:, 1]
#         if np.abs(maximas_new_fitted_func[0] - maximas_z_original[0]) > 0.01:
#             shift = np.abs(maximas_new_fitted_func[0] - maximas_z_original[0])
#             guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset + shift])
#             c = c + shift
#         return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1. / f, "fitfunc": fitfunc,
#                 "maxcov": np.max(pcov), "rawres": (guess, popt, pcov)}, fitfunc(zz)
#     elif Number_of_sinus == 2:
#         zz = np.array(zz)
#         vv = np.array(vv)
#         ff = np.fft.fftfreq(len(zz), (zz[1] - zz[0]))  # assume uniform spacing
#         Fvv = abs(np.fft.fft(vv))[1:]
#         f = np.argsort(Fvv[0:np.int64(np.floor(len(Fvv) / 2))])[::-1][:2]
#         guess_freq_1 = abs(ff[f[0] + 1])  # excluding the zero frequency "peak", which is related to offset
#         guess_freq_2 = abs(ff[f[1] + 1])
#         guess_amp_1 = Fvv[f[0]] / (len(vv) / 2)
#         guess_amp_2 = Fvv[f[1]] / (len(vv) / 2)
#         guess_offset = np.mean(vv)
#         guess = np.array(
#             [guess_amp_1, guess_amp_2, 2. * np.pi * guess_freq_1, 2. * np.pi * guess_freq_2, 0., 0., guess_offset])
#
#         def sinfunc_2(z, A, B, w_1, w_2, p_1, p_2, c):
#             return A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) + c
#
#         popt, pcov = curve_fit(sinfunc_2, zz, vv, p0=guess, maxfev=5000)
#         A, B, w_1, w_2, p_1, p_2, c = popt
#         f = w_1 / (2. * np.pi)
#         fitfunc_2 = lambda z: A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) + c
#         new_fitted_func = fitfunc_2(zz)
#         maximas_new_fitted_func = find_peaks_maxima(zz, new_fitted_func)[:, 1]
#         maximas_z_original = find_peaks_maxima(zz, vv)[:, 1]
#         if np.abs(maximas_new_fitted_func[0] - maximas_z_original[0]) > 0.01:
#             shift = np.abs(maximas_new_fitted_func[0] - maximas_z_original[0])
#             guess = np.array(
#                 [guess_amp_1, guess_amp_2, 2. * np.pi * guess_freq_1, 2. * np.pi * guess_freq_2, 0., 0., guess_offset])
#             c = c + shift
#         return {"amp_1": A, "amp_2": B, "omega_1": w_1, "omega_2": w_2, "phase_1": p_1, "phase_2": p_2, "offset": c,
#                 "freq": f, "period": 1. / f, "fitfunc": fitfunc_2, "maxcov": np.max(pcov),
#                 "rawres": (guess, popt, pcov)}, fitfunc_2(zz)
#
#
# def v_is_matching_moving_avg(v_original, v_to_compare):
#     '''
#     Parameters
#     ----------
#     v_original : 1D np.array
#         The potential vector we wish to compare respect to it.
#     v_to_compare : 1D np.array
#         The potential vector we wish to compare with. Usually will be the curve fitting result.
#
#     Returns
#     -------
#     flag : Boolean
#         Checks whether the two potential vectors are similar or not.
#
#     '''
#     i = 0
#     v_original = to_1D_vec(v_original)
#     v_to_compare = to_1D_vec(v_to_compare)
#     flag = True
#     while i < len(v_original) - 5 and flag:
#         temp_v_original = v_original[i:i + 10]
#         temp_v_to_compare = v_to_compare[i:i + 10]
#         moving_avg_v_original = np.average(temp_v_original)
#         moving_avg_v_to_compare = np.average(temp_v_to_compare)
#         if np.abs(moving_avg_v_original - moving_avg_v_to_compare) > 0.1:
#             flag = False
#         i += 1
#     return flag
#
#
# def fit_sum_of_sines_4(zz, vv):
#     zz = np.array(zz)
#     vv = np.array(vv)
#     ff = np.fft.fftfreq(len(zz), (zz[1] - zz[0]))  # assume uniform spacing
#     Fvv = abs(np.fft.fft(vv))[1:]
#     f = np.argsort(Fvv[0:np.int64(np.floor(len(Fvv) / 2))])[::-1][:5]
#     guess_freq_1 = abs(ff[f[0] + 1])  # excluding the zero frequency "peak", which is related to offset
#     guess_freq_2 = abs(ff[f[1] + 1])
#     guess_freq_3 = abs(ff[f[2] + 1])
#     guess_freq_4 = abs(ff[f[3] + 1])
#
#     guess_amp_1 = Fvv[f[0]] / (len(vv) / 2)
#     guess_amp_2 = Fvv[f[1]] / (len(vv) / 2)
#     guess_amp_3 = Fvv[f[2]] / (len(vv) / 2)
#     guess_amp_4 = Fvv[f[3]] / (len(vv) / 2)
#
#     guess_offset = np.mean(vv)
#
#     guess = np.array([guess_amp_1, guess_amp_2, guess_amp_3, guess_amp_4,
#                       2. * np.pi * guess_freq_1, 2. * np.pi * guess_freq_2,
#                       2. * np.pi * guess_freq_3, 2. * np.pi * guess_freq_4,
#                       0., 0., 0., 0.,
#                       guess_offset])
#
#     def sinfunc_4(z, A, B, C, D,
#                   w_1, w_2, w_3, w_4,
#                   p_1, p_2, p_3, p_4, c):
#         return (A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) +
#                 C * np.sin(w_3 * z + p_3) + D * np.sin(w_4 * z + p_4)
#                 + c)
#
#     popt, pcov = curve_fit(sinfunc_4, zz, vv, p0=guess, maxfev=5000)
#     A, B, C, D, w_1, w_2, w_3, w_4, p_1, p_2, p_3, p_4, c = popt
#
#     fitfunc_4 = lambda z: A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) + \
#                           C * np.sin(w_3 * z + p_3) + D * np.sin(w_4 * z + p_4) + c
#
#     return popt, fitfunc_4(zz)
#
#
# def v_is_matching_curve_fitting(z, v_original, v_to_compare):
#     '''
#     Parameters
#     ----------
#     z : 1D np.array
#        Coordinates vector.
#     v_original : 1D np.array
#        The potential vector we wish to compare respect to it.
#     v_to_compare : 1D np.array
#         The potential vector we wish to compare with. Usually will be the curve fitting result.
#
#     Returns
#     -------
#     flag : Boolean
#         Checks whether the two potential vectors are similar or not.
#
#     '''
#     dic_para_1, new_v_1 = fit_sin(z, v_original)
#     dic_para_2, new_v_2 = fit_sin(z, v_original, N=2)
#     popt_3, new_v_3 = fit_sum_of_sines_4(z, v_original)
#     popt_4, new_v_4 = fit_sum_of_sines_8(z, v_original)
#
#     r1 = r_sqrd(v_original, new_v_1)
#     r2 = r_sqrd(v_original, new_v_2)
#     r3 = r_sqrd(v_original, new_v_3)
#     r4 = r_sqrd(v_original, new_v_4)
#
#     if np.max(r1, r2, r3, r4) == r1:
#         original_fit = new_v_1
#     elif np.max(r1, r2, r3, r4) == r2:
#         original_fit = new_v_2
#     elif np.max(r1, r2, r3, r4) == r3:
#         original_fit = new_v_3
#     else:
#         original_fit = new_v_4
#
#     dic_para_1, new_v_1 = fit_sin(z, v_to_compare)
#     dic_para_2, new_v_2 = fit_sin(z, v_to_compare, N=2)
#     popt_3, new_v_3 = fit_sum_of_sines_4(z, v_to_compare)
#     popt_4, new_v_4 = fit_sum_of_sines_8(z, v_to_compare)
#
#     r1 = r_sqrd(v_original, new_v_1)
#     r2 = r_sqrd(v_original, new_v_2)
#     r3 = r_sqrd(v_original, new_v_3)
#     r4 = r_sqrd(v_original, new_v_4)
#
#     if np.max(r1, r2, r3, r4) == r1:
#         to_compare_fit = new_v_1
#     elif np.max(r1, r2, r3, r4) == r2:
#         to_compare_fit = new_v_2
#     elif np.max(r1, r2, r3, r4) == r3:
#         to_compare_fit = new_v_3
#     else:
#         to_compare_fit = new_v_4
#
#     return r_sqrd(original_fit, to_compare_fit) > 0.995
#
#
# def fit_sum_of_sines_8(zz, vv):
#     zz = np.array(zz)
#     vv = np.array(vv)
#     ff = np.fft.fftfreq(len(zz), (zz[1] - zz[0]))  # assume uniform spacing
#     Fvv = abs(np.fft.fft(vv))[1:]
#     f = np.argsort(Fvv[0:np.int64(np.floor(len(Fvv) / 2))])[::-1][:9]
#     guess_freq_1 = abs(ff[f[0] + 1])  # excluding the zero frequency "peak", which is related to offset
#     guess_freq_2 = abs(ff[f[1] + 1])
#     guess_freq_3 = abs(ff[f[2] + 1])
#     guess_freq_4 = abs(ff[f[3] + 1])
#     guess_freq_5 = abs(ff[f[4] + 1])
#     guess_freq_6 = abs(ff[f[5] + 1])
#     guess_freq_7 = abs(ff[f[6] + 1])
#     guess_freq_8 = abs(ff[f[7] + 1])
#
#     guess_amp_1 = Fvv[f[0]] / (len(vv) / 2)
#     guess_amp_2 = Fvv[f[1]] / (len(vv) / 2)
#     guess_amp_3 = Fvv[f[2]] / (len(vv) / 2)
#     guess_amp_4 = Fvv[f[3]] / (len(vv) / 2)
#     guess_amp_5 = Fvv[f[4]] / (len(vv) / 2)
#     guess_amp_6 = Fvv[f[5]] / (len(vv) / 2)
#     guess_amp_7 = Fvv[f[6]] / (len(vv) / 2)
#     guess_amp_8 = Fvv[f[7]] / (len(vv) / 2)
#
#     guess_offset = np.mean(vv)
#
#     guess = np.array([guess_amp_1, guess_amp_2, guess_amp_3, guess_amp_4,
#                       guess_amp_5, guess_amp_6, guess_amp_7, guess_amp_8,
#                       2. * np.pi * guess_freq_1, 2. * np.pi * guess_freq_2,
#                       2. * np.pi * guess_freq_3, 2. * np.pi * guess_freq_4,
#                       2. * np.pi * guess_freq_5, 2. * np.pi * guess_freq_6,
#                       2. * np.pi * guess_freq_7, 2. * np.pi * guess_freq_8,
#                       0., 0., 0., 0., 0., 0., 0., 0.,
#                       guess_offset])
#
#     def sinfunc_4(z, A, B, C, D, E, F, G, H,
#                   w_1, w_2, w_3, w_4,
#                   w_5, w_6, w_7, w_8,
#                   p_1, p_2, p_3, p_4,
#                   p_5, p_6, p_7, p_8,
#                   c):
#         return (A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) +
#                 C * np.sin(w_3 * z + p_3) + D * np.sin(w_4 * z + p_4) +
#                 E * np.sin(w_5 * z + p_5) + F * np.sin(w_6 * z + p_6) +
#                 G * np.sin(w_7 * z + p_7) + H * np.sin(w_8 * z + p_8) +
#                 + c)
#
#     popt, pcov = curve_fit(sinfunc_4, zz, vv, p0=guess, maxfev=100000)
#     A, B, C, D, E, F, G, H, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, c = popt
#
#     fitfunc_4 = lambda z: (A * np.sin(w_1 * z + p_1) + B * np.sin(w_2 * z + p_2) +
#                            C * np.sin(w_3 * z + p_3) + D * np.sin(w_4 * z + p_4) +
#                            E * np.sin(w_5 * z + p_5) + F * np.sin(w_6 * z + p_6) +
#                            G * np.sin(w_7 * z + p_7) + H * np.sin(w_8 * z + p_8) +
#                            + c)
#
#     return popt, fitfunc_4(zz)
#
#
# def r_sqrd(v_original, v_fitted):
#     return 1 - (np.sum(((v_original - v_fitted) ** 2)) / np.sum((v_original - np.mean(v_original)) ** 2))
#
#
# def fit_lmfit(zz, vv, N=1):
#     zz = np.array(zz)
#     vv = np.array(vv)
#     ff = np.fft.fftfreq(len(zz), (zz[1] - zz[0]))  # assume uniform spacing
#     Fvv = abs(np.fft.fft(vv))[1:]
#     f = np.argsort(Fvv[0:np.int64(np.floor(len(Fvv) / 2))])[::-1][:N + 1]
#
#     def sine_1(zz, amp, omega, phase, coeff):
#         return amp * np.sin(omega * zz + phase) + coeff
#
#     def sine(zz, amp, omega, phase):
#         return amp * np.sin(omega * zz + phase)
#
#     mod_1 = Model(sine_1, prefix='f_1_')
#     params = mod_1.make_params(amp=Fvv[f[0]] / (len(vv) / 2), omega=abs(ff[f[0] + 1]), phase=0.0, coeff=np.mean(vv))
#     params['f_1_amp'].min = 0.0
#     mod = mod_1
#     for i in range(2, N + 1):
#         mod_temp = Model(sine, prefix=f'f_{i}_')
#         param_temp = mod_temp.make_params(amp=Fvv[f[i - 1]] / (len(vv) / 2), omega=abs(ff[f[i - 1] + 1]), phase=0.0)
#         param_temp[f'f_{i}_amp'].min = 0.0
#
#         for j in param_temp.items():
#             params.add_many(j)
#         mod = mod_temp + mod
#     for j in params.keys():
#         params[j].init_value = None
#     Model_res = mod.fit(vv, params, zz=zz)
#     for j in params.keys():
#         try:
#             Model_res.params[j].init_value = Model_res.params[j].init_value.value
#
#         except:
#             pass
#
#     return Model_res

def is_peak_maximum(peaks, peak):
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
