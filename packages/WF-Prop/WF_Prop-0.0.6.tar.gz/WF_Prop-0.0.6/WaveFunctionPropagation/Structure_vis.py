import numpy as np

from Locpot_class import *
from Help_function_library_yair import *
from scipy.fft import fft, ifft, fftfreq, fft2, ifft2, fftshift, ifftshift
from matplotlib import animation
from matplotlib.animation import PillowWriter
import matplotlib
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import product, combinations
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

class structure_visualiztion:
    def __init__(self, structure = None,structure_file_name = None, structure_file_directory= None,D3_plot = True,label = False):
        self.structure_file_name = structure_file_name
        self.structure_file_directory = structure_file_directory
        self.structure = structure
        if not (self.structure_file_name is None or self.structure_file_directory is None):
            self.structure_path = os.path.join(self.structure_file_directory,  self.structure_file_name)
            self.structure = Structure.from_file(self.structure_path)
        else:
            self.structure = structure
        self.D3_plot = D3_plot
        self.cart_coords = self.structure.cart_coords
        self.frac_coords = self.structure.frac_coords
        self.lattice_constants = (self.structure.lattice.a,self.structure.lattice.b,self.structure.lattice.c)
        self.boundaries = ([0,self.lattice_constants[0]],[0,self.lattice_constants[1]],[0,self.lattice_constants[2]])
        self.atomic_radius = None
        self.atom_symbols = None
        self.is_set_boundaries = False
        self.Matrix = None
        self.label = label
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')


    def set_relative_radii(self):
        coords_matrix = self.cart_coords
        relative_radii = np.asarray([i.atomic_radius for i in self.structure.species], dtype = float)
        set_atomic_radius = np.asarray([i.atomic_radius for i in self.structure.types_of_species], dtype = float)
        relative_radii = np.float64(relative_radii/np.sum(set_atomic_radius))*5000
        self.atomic_radius = relative_radii


    def set_atomic_symbol(self):
        coords_matrix = self.cart_coords
        atoms_symbol = np.asarray([i.name for i in self.structure.species], dtype = str)
        self.atom_symbols = atoms_symbol

    def set_label(self,flag):
        if type(flag) == bool:
            self.label = flag

    def visualize(self):
        if not self.is_set_boundaries:

            self.ax.set_xlabel('x axis in Angstrum')
            self.ax.set_ylabel('y axis in Angstrum')
            self.ax.set_zlabel('z axis in Angstrum')
            coords_matrix = self.cart_coords
            relative_radii = np.asarray([i.atomic_radius for i in self.structure.species], dtype = float)
            atoms_symbol = np.asarray([i.name for i in self.structure.species], dtype = str)
            atoms_species = self.structure.symbol_set
            set_atomic_radius = np.asarray([i.atomic_radius for i in self.structure.types_of_species], dtype = float)
            relative_radii = np.float64(relative_radii/np.sum(set_atomic_radius))*5000

            colors = ["red", "green", "blue", "purple", "yellow", "orange", "dark", "magenta"]
            color_of_atom = {}

            for i in range(len(colors)):
                if i < len(atoms_species):
                    color_of_atom.update({atoms_species[i]: colors[i]})

            for i in atoms_species:
                temp_indices = (atoms_symbol == i)
                temp_coords = coords_matrix[temp_indices]
                # for j in range(len(temp_coords[:,0])):
                self.ax.scatter(temp_coords[:,0],temp_coords[:,1],temp_coords[:,2], c = color_of_atom[i],
                                   s=relative_radii[temp_indices], norm=True, label=i, alpha= 0.7,edgecolor ='gray')

                if self.label:
                    anotations = []
                    for i in range(len(temp_coords[:, 0])):
                        anotations.append('{} {}'.format(atoms_symbol[i], i))
                    for i, label in enumerate(anotations):
                        self.ax.text(temp_coords[:, 0][i], temp_coords[:, 1][i], temp_coords[:, 2][i], label)

            a = self.boundaries[0]
            b = self.boundaries[1]
            c = self.boundaries[2]
            for s, e in combinations(np.array(list(product(a, b, c))), 2):
                if np.sum(np.abs(s - e)) == a[1] - a[0] or np.sum(np.abs(s - e)) == b[1] - b[0] or np.sum(np.abs(s - e)) == c[1] - c[0]:
                    self.ax.plot3D(*zip(s, e), color="gray")

            self.ax.set_xlim(0,self.lattice_constants[0])
            self.ax.set_ylim(0, self.lattice_constants[1])
            self.ax.set_zlim(0, self.lattice_constants[2])
            self.ax.set_box_aspect((self.lattice_constants[0], self.lattice_constants[1], self.lattice_constants[2]))
            self.ax.legend(markerscale=0.2)
        else:

            self.ax.set_xlabel('x axis in Angstrum')
            self.ax.set_ylabel('y axis in Angstrum')
            self.ax.set_zlabel('z axis in Angstrum')
            coords_matrix = self.Matrix
            relative_radii = np.float64(coords_matrix[:,3])
            atoms_symbol = coords_matrix[:,4]
            atoms_species = self.structure.symbol_set
            set_atomic_radius = np.asarray([i.atomic_radius for i in self.structure.types_of_species], dtype=float)
            relative_radii = np.float64(relative_radii / np.sum(set_atomic_radius))

            colors = ["red", "green", "blue", "purple", "yellow", "orange", "dark", "magenta"]
            color_of_atom = {}

            for i in range(len(colors)):
                if i < len(atoms_species):
                    color_of_atom.update({atoms_species[i]: colors[i]})

            for i in atoms_species:
                temp_indices = (atoms_symbol == i)
                temp_coords = coords_matrix[temp_indices]
                # for j in range(len(temp_coords[:,0])):
                self.ax.scatter(np.float64(temp_coords[:, 0]), np.float64(temp_coords[:, 1]), np.float64(temp_coords[:, 2]), c=color_of_atom[i],
                           s=np.float64(relative_radii[temp_indices]), norm=True, label=i, alpha=0.7, edgecolor='gray')

                if self.label:
                    anotations = []
                    for j in range(np.shape(temp_coords)[0]):
                        anotations.append('{} {}'.format(temp_coords[j][4], j))
                    for j, label in enumerate(anotations):
                        self.ax.text(np.float64(temp_coords[:, 0])[j], np.float64(temp_coords[:, 1])[j],
                                np.float64(temp_coords[:, 2])[j], label,fontsize= 9,fontfamily= 'serif')

            a = np.float64(self.boundaries[0])
            b = np.float64(self.boundaries[1])
            c = np.float64(self.boundaries[2])
            for s, e in combinations(np.array(list(product(a, b, c))), 2):
                if np.sum(np.abs(s - e)) == a[1] - a[0] or np.sum(np.abs(s - e)) == b[1] - b[0] or np.sum(
                        np.abs(s - e)) == c[1] - c[0]:
                    self.ax.plot3D(*zip(s, e), color="gray")


            self.ax.set_xlim(0, a[1])
            self.ax.set_ylim(0, b[1])
            self.ax.set_zlim(0, c[1])
            self.ax.set_box_aspect((a[1], b[1], c[1]))
            self.ax.legend(markerscale=0.2)

    def set_boundaries(self,bounds = ([0,1], [0,1], [0,1])):
        self.set_relative_radii()
        self.set_atomic_symbol()
        temp_atoms_to_mult = np.copy(self.cart_coords)
        temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
        temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
        added_atoms =np.array([[],[],[],[],[]]).T
        for n,i in enumerate(bounds):
            if i[0] < 0:
                if n == 0:
                    temp_atoms_to_mult = np.copy(self.cart_coords)
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
                else:
                    temp_atoms_to_mult = np.copy(constant_matrix)
                if i[0] < -1:
                    frac_num = i[0]%1
                    comp = np.int64(np.ceil(i[0]))
                    temp_lat_par = self.lattice_constants[n]*i[0]
                else:
                    comp = np.int64(np.floor(i[0]))
                    temp_lat_par = self.lattice_constants[n] * i[0]
                for j in range(1,-comp+2):
                    if n == 0:
                        temp_array = np.copy(self.cart_coords)
                        temp_array = np.column_stack((temp_array,self.atomic_radius))
                        temp_array = np.column_stack((temp_array, self.atom_symbols))
                    else:
                        temp_array = np.copy(constant_matrix)
                    temp_array[:,n] =  np.float64(temp_array[:,n]) - j*self.lattice_constants[n]
                    temp_atoms_to_mult = np.append(temp_atoms_to_mult,temp_array,axis=0)
                for j in temp_atoms_to_mult :
                    if np.float64(j[n]) >= temp_lat_par:
                        added_atoms =np.append(added_atoms,j[np.newaxis],axis=0)
            elif i[0] > 0:
                if n == 0:
                    temp_atoms_to_mult = np.copy(self.cart_coords)
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
                else:
                    temp_atoms_to_mult = np.copy(constant_matrix)
                if i[0] > 1:
                    frac_num = i[0]%1
                    comp = np.int64(np.floor(i[0]))
                    temp_lat_par = self.lattice_constants[n]*i[0]
                else:
                    comp = np.int64(np.ceil(i[0]))
                    temp_lat_par = self.lattice_constants[n] * i[0]
                for j in range(1,comp+2):
                    if n == 0 :
                        temp_array = np.copy(self.cart_coords)
                        temp_array = np.column_stack((temp_array,self.atomic_radius))
                        temp_array = np.column_stack((temp_array, self.atom_symbols))
                    else:
                        temp_array = np.copy(constant_matrix)
                    temp_array[:,n] =  np.float64(temp_array[:,n]) + j*self.lattice_constants[n]
                    temp_atoms_to_mult = np.append(temp_atoms_to_mult,temp_array,axis=0)
                for j in temp_atoms_to_mult :
                    if np.float64(j[n]) >= temp_lat_par:
                        added_atoms=np.append(added_atoms,j[np.newaxis],axis=0)

            if i[1] < 0:
                if n == 0 :
                    temp_atoms_to_mult = np.copy(self.cart_coords)
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
                else:
                    temp_atoms_to_mult = np.copy(constant_matrix)
                if i[1] < -1:
                    frac_num = i[1]%1
                    comp = np.int64(np.ceil(i[1]))
                    temp_lat_par = self.lattice_constants[n]*i[1]
                else:
                    comp = np.int64(np.floor(i[1]))
                    temp_lat_par = self.lattice_constants[n] * i[1]
                for j in range(1,-comp+2):
                    if n == 0 :
                        temp_array = np.copy(self.cart_coords)
                        temp_array = np.column_stack((temp_array, self.atomic_radius))
                        temp_array = np.column_stack((temp_array, self.atom_symbols))
                    else:
                        temp_array = np.copy(constant_matrix)
                    temp_array[:,n] =  np.float64(temp_array[:,n]) - j*self.lattice_constants[n]
                    temp_atoms_to_mult = np.append(temp_atoms_to_mult,temp_array,axis=0)
                for j in temp_atoms_to_mult :
                    if np.float64(j[n]) <= temp_lat_par:
                        added_atoms=np.append(added_atoms,j[np.newaxis],axis=0)
            elif i[1] > 0:
                if n == 0 :
                    temp_atoms_to_mult = np.copy(self.cart_coords)
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
                    temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
                else:
                    temp_atoms_to_mult = np.copy(constant_matrix)
                if i[1] > 1:
                    frac_num = i[1]%1
                    comp = np.int64(np.floor(i[1]))
                    temp_lat_par = self.lattice_constants[n]*i[1]
                else:
                    comp = np.int64(np.ceil(i[1]))
                    temp_lat_par = self.lattice_constants[n] * i[1]
                for j in range(1,comp+2):
                    if n == 0:
                        temp_array = np.copy(self.cart_coords)
                        temp_array = np.column_stack((temp_array, self.atomic_radius))
                        temp_array = np.column_stack((temp_array, self.atom_symbols))
                    else:
                        temp_array = np.copy(constant_matrix)
                    temp_array[:,n] =  np.float64(temp_array[:,n]) + j*self.lattice_constants[n]
                    temp_atoms_to_mult = np.append(temp_atoms_to_mult,temp_array,axis=0)
                for j in temp_atoms_to_mult :
                    if np.float64(j[n]) <= temp_lat_par:
                        added_atoms=np.append(added_atoms,j[np.newaxis],axis=0)
            if  n == 0:
                temp_atoms_to_mult = np.copy(self.cart_coords)
                temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atomic_radius))
                temp_atoms_to_mult = np.column_stack((temp_atoms_to_mult, self.atom_symbols))
                temp_atoms_to_mult = np.append(temp_atoms_to_mult, added_atoms, axis=0)
            else:
                temp_atoms_to_mult = np.copy(constant_matrix)
                temp_atoms_to_mult = np.append(temp_atoms_to_mult, added_atoms, axis=0)

            final_matrix = np.array([[],[],[],[],[]]).T
            for p in temp_atoms_to_mult:
                if not find_element_in_matrix(p, final_matrix):
                    final_matrix = np.append(final_matrix,p[np.newaxis],axis=0)
            constant_matrix = np.copy(final_matrix)
        final_matrix = np.array([[], [], [], [], []]).T
        for p in constant_matrix:
            if not find_element_in_matrix(p, final_matrix):
                final_matrix = np.append(final_matrix, p[np.newaxis], axis=0)
        self.is_set_boundaries = True
        self.Matrix =  final_matrix
        #self.boundaries = ([bounds[0][0]*self.lattice_constants[0],bounds[0][1]*self.lattice_constants[0]],
                            #[bounds[1][0]*self.lattice_constants[1],bounds[1][1]*self.lattice_constants[1]],
                             #[bounds[2][0]*self.lattice_constants[2],bounds[2][1]*self.lattice_constants[2]])
        return self.Matrix

    def color_atom(self,atom):
        for i in range(np.shape(atom)[0]):
            x,y,z = atom
        self.ax.scatter(x,y,z,color = 'yellow',s=np.float64(np.float64(self.Matrix[:,3])[np.float64(self.Matrix[:,2]) == np.float64(z)][0])*0.75, norm=True)

    def choose_atoms_by_coordinates(self,coordinates):
        for i in range(np.shape(coordinates)[0]):
            x, y, z = i
            self.color_atom(self, [x,y,z])

    def choose_atoms_by_index(self, indice):
        if not self.Matrix is None:
            mat = self.Matrix
            print('The extended matrix is not necssary has the same indice as you think')
        else:
            mat = self.cart_coords
        mat = mat[indice]
        for i in mat:
            x, y, z = i
            self.color_atom(self, [x, y, z])

def find_element_in_matrix(element, matrix):
    conc_falg = False
    for i in matrix:
        if np.all(i == element):
            conc_falg = True
            break
    return conc_falg

if __name__ == '__main__':
    vis = structure_visualiztion(structure_file_name='CONTCAR',
                                 structure_file_directory=r'C:\Users\user\OneDrive - Technion\Master degree\Tasks\Semester_3\Interfaces\GaN-AlN\Interface\One_unit_Cell\Strained\long_lat')
    # vis.set_label(True)
    a = vis.set_boundaries(([0, 1.1], [0, 1.1], [-0.01, 1.1]))
    vis.visualize()
    vis.color_atom([0.036059638990142605,0.03604613307155137,13.336259436731707])
    vis.ax.view_init(elev=2., azim=90)


