import numpy as np

from Locpot_class import *
from Help_function_library_yair import *
from scipy.fft import fft, ifft, fftfreq, fft2, ifft2, fftshift, ifftshift
from matplotlib import animation
from matplotlib.animation import PillowWriter



class Stage_2:
    '''
    This class aimed to locate the initial wavefunction we created at stage_1,
    on the relevant material from stage_1, in the middle of the material in the interface system.

    '''


    def __init__(self, Locp, grid_density, psi0_dic, allmin=None, allmax=None, To_plot=False,Nt = 500, dt = 0.01 ,multi_left = 2, multi_right = 2, is2d = False, Has_interface = True,limits_for_itself=None,ref_point = None):
        '''**Initilization**:

        Parameters
        ----------
        Locp : Locpot_yair.object
                Locpot object that holds the information about the interface system.
        grid_density : float
                grid density factor calculated in stage_1
        psi0_dic : dict
                psi0 parameters given in a dictionary form. Necessary to reconstruct the initial wave function in the
                interface system.
        allmin : np.array, array_like, optional, default: None
                Not necessary for the intialization. Holds all the minimum peaks of the local potential.
        allmax : np.array, array_like, optional, default: None
                Not necessary for the intialization. Holds all the maximum peaks of the local potential.
        To_plot : bool, optional, default: False
                A flag to determine whether to plot when this option is availale.
        Nt : int
                The number of time steps we would like to have in the propagation proccess.
        dt : float
                The size of the time step in ``sec``.
        multi_left : int, optional, default: 2
                How many times we wish add a unit cell length to the left side of the interface.
                Namely, for ``multi_left = 2``, we are adding ``2*a_left`` to the locpot vector.
        multi_right : int, optional, default: 2
                How many times we wish add a unit cell length to the right side of the interface.
                Namely, for ``multi_right = 2``, we are adding ``2*a_right`` to the locpot vector.
        Has_interface : bool, optional, default: True
                A flag indicates whether the system conatains an interface or not.
                For a surface, it is recomended to relate the vaccum as the interface.
        limits_for_itself : list [float, float], optional, default: None
                This parameter is an optional for flexibility for chosing the range of where the pick the bulk-like potential.
                This should be input as a list of two floats, the first one is for the left limit and the second one is for the left limit.
                Should be given as the same units of the spatial coordainates vector, ``z``.
        ref_point : float, optional, default: None
                If the current system does not have an interface, and we want to treat it as it as a reference point for later calculations.
        '''
        self.Has_interface = Has_interface
        self.locp = Locp
        self.locp.set_locpot_bulk_materials()
        self.is2d = is2d
        self.converged_locpot_vec = None
        self.elongated_locpot_vec = None
        self.current_locpot_vec = self.locp.locpot_vec
        self.L_original = self.locp.locpot_vec[len(self.locp.locpot_vec[:, 0]) - 1, 0]  # determined by the
        # last position in the locpot of the whole system
        self.Nt = Nt
        self.dt = dt
        self.allmin = allmin
        if self.allmin is None:
            self.allmin = find_peaks_minima(self.locp.locpot_vec[:, 0], self.locp.locpot_vec[:, 1])
        self.allmax = allmax
        if self.allmax is None:
            self.allmax = find_peaks_maxima(self.locp.locpot_vec[:, 0], self.locp.locpot_vec[:, 1])
        self.alpha = 1.3
        self.cons = Constants()
        self.To_plot = To_plot
        self.psi0_dic = psi0_dic
        self.grid_density = grid_density # [samples/A]
        self.N = 0
        self.multi_left = multi_left
        self.multi_right = multi_right
        self.index_original_interface, self.original_interface = self.locp.find_interface()
        self.index_new_interface, self.new_interface = None , None
        self.update_converged_spatial_grid(update_converged_vec=True,update_interface=True)
        self.psi0 = None
        self.limits_for_itself=limits_for_itself
        self.ref_point = ref_point



    def elongate_interface_potential(self, from_iteslf = False,side_from_itself = 'both',interface_position = None, manual = False, z_in = None, v_in = None, multi_manual = 1,
                                      pos_to_insert = None,locpot_vector = None, To_update = True,original_interface = None):
        r"""

        Parameters
        ----------
        from_iteslf : bool, optional, default: False
                This flag indicates whether to take the bulk-like potential that is going to be
                multiplied and then inserted - from itself - namely - from the middle of the local potnetial - far from the
                interface positions (since it satisfies periodic condition). Otherwise - it is taken from outer-scope file -
                supplied in the same directory and is referred to the bulk-material locpot file - obtained from VASP.
        side_from_itself : {'both', 'right', 'left'}, optional, default: 'both'
                Choices in brackets. This flag is being active only when the flag ``from_iteslf=True``.
        from_iteslf : bool, optional, default: True
                It indicates where we wish to elngate our local potential vector. -> From both side, or only from only one side
                of the interface.
        interface_position : np.float, optional, default: None
                Enables to input the interface position manually. It refers to the spaciol coordinates.
                If your system does not have an interface, you should supply this argument with ''0''.
        manual : bool, optional, default: False
                Enables the user to elongate its locpot vector's system manually.
                If this flag is turned on by supplying ``manual = True``, the user must also supply ``z_in`` and ``v_in`` vectors.
        z_in : np.array, array_like, optional, default: None
                When the user decides on elongating manually its locpot vector's system,
                he should supplied also ``z_in`` and ``v_in`` as the spatial grid\coordinates vector and the local potential vector
                respectively.
        v_in : np.array, array_like, optional, default: None
                When the user decides on elongating manually its locpot vector's system,
                he should supplied also ``z_in`` and ``v_in`` as the spatial grid\coordinates vector and the local potential vector
                respectively.
        multi_manual : int, optional, default: 1
                When the user decides on elongating manually its locpot vector's system,
                it enables him to determine how many times to multiply the inserted locpot vector. This flag is also used
                in the case when to option of ``from_itself`` is turned on.
        pos_to_insert : float, optional, default: None
                When this argument is supplied, is enables determine the position where
                to insert the locpot vector during the elongation proccess.
        locpot_vector : `numpy.ndarray`, (N, 2), optional, default: None
                The first column is the spatial grid/coordinates vector, and the second vector is local potential.
                It enables to elongate a locpot vector that is not related
                to the class instance attributes.
        To_update : bool, optional, default: True
                A flag indicates if the changes that have being made are going to be updated as the instance attributes.
        original_interface : float, optional, default: None
                If specified, all the extention procedure will be considering this interface position during all the procedure.

        Returns
        -------
        Elongated locpot_vec : numpy.ndarray, (N, 2)
                It consists of 2 columns. First column is the spatial coordinates, the second column is the local potential values.
        """
        if not self.is2d:
            if not from_iteslf:
                if not manual:
                    if self.Has_interface:
                        elongated_locpot_vec,delta_left,delta_right = self.locp.elongate_locpot(multi_left = self.multi_left, multi_right= self.multi_right,return_left_increment=True,return_right_increment=True)
                    else:
                        if pos_to_insert is None:
                            elongated_locpot_vec,delta_left,temp_point = self.locp.elongate_locpot( manual=True, pos_to_insert = self.current_locpot_vec[:,0][-1], z_to_insert_manual = self.current_locpot_vec[:,0], v_to_insert_manual = self.current_locpot_vec[:,1],return_left_increment=True)
                        else:
                            elongated_locpot_vec,delta_left,temp_point = self.locp.elongate_locpot(manual=True, pos_to_insert=
                            pos_to_insert, z_to_insert_manual=self.current_locpot_vec[:, 0],
                                                                             v_to_insert_manual=self.current_locpot_vec[:, 1],return_left_increment=True)
                    if To_update:
                        self.elongated_locpot_vec = elongated_locpot_vec
                        self.elongated_locpot_vec = self.update_converged_spatial_grid(vecor_to_update=self.elongated_locpot_vec,update_converged_vec= False, update_interface=False)
                        if self.Has_interface:
                            if not self.new_interface is None:
                                index_interface, interface_pos = self.index_new_interface, self.new_interface
                            else:
                                index_interface, interface_pos = find_closest_value_in_array(self.original_interface,self.elongated_locpot_vec[:,0])
                            interface_pos = interface_pos + delta_left
                            # index_interface, interface_pos = self.locp.find_interface(x=self.elongated_locpot_vec[:, 0],
                            #                                                       y=self.elongated_locpot_vec[:, 1])
                            if self.original_interface - self.original_interface * 0.1 <= interface_pos <= self.original_interface + self.original_interface * 0.1:
                                self.index_original_interface, self.original_interface = find_closest_value_in_array(interface_pos,
                                                                             self.converged_locpot_vec[:, 0])
                                self.index_new_interface, self.new_interface =  self.index_original_interface, self.original_interface
                            else:
                                self.index_new_interface, self.new_interface = find_closest_value_in_array(interface_pos,self.elongated_locpot_vec[:,0])
                        else:
                            if not self.ref_point is None:
                                if self.ref_point >= pos_to_insert:
                                    self.ref_point += delta_left
                        self.current_locpot_vec = self.elongated_locpot_vec
                        return  self.elongated_locpot_vec
                    else:
                        elongated_locpot_vec = self.update_converged_spatial_grid(
                            vecor_to_update=elongated_locpot_vec, update_converged_vec=False,
                            update_interface=False)
                        return elongated_locpot_vec
                else:
                    ## manual, but not from itself.
                    if z_in is None or v_in is None:
                        print('You chose manual elongation. However you did not supplied coordinates and local potential vectors.')
                        return None
                    else:
                        if pos_to_insert is None:
                            pos_to_insert = z_in[-1]
                        if locpot_vector is None:
                            if not self.current_locpot_vec is None:
                                elongated_locpot_vec, delta, ref_pos= self.locp.elongate_locpot(manual = True, pos_to_insert = pos_to_insert,
                                    multi_manual= multi_manual, z_to_insert_manual = z_in, v_to_insert_manual = v_in,locpot_vec=self.current_locpot_vec,return_left_increment=True)
                            else:
                                elongated_locpot_vec, delta, ref_pos = self.locp.elongate_locpot(manual = True, pos_to_insert = pos_to_insert,
                                    multi_manual= multi_manual, z_to_insert_manual = z_in, v_to_insert_manual = v_in,return_left_increment=True)
                        else:
                            elongated_locpot_vec, delta, ref_pos = self.locp.elongate_locpot(manual = True, pos_to_insert = pos_to_insert,
                                multi_manual= multi_manual, z_to_insert_manual = z_in, v_to_insert_manual = v_in,locpot_vec=locpot_vector,return_left_increment=True)

                        if To_update:
                            self.elongated_locpot_vec = elongated_locpot_vec
                            self.elongated_locpot_vec = to_2_column_mat(self.elongated_locpot_vec)
                            self.elongated_locpot_vec = self.update_converged_spatial_grid(
                                vecor_to_update=self.elongated_locpot_vec, update_converged_vec=False,
                                update_interface=False)
                            if self.Has_interface:
                                if not original_interface is None:
                                    index_interface, interface_pos = find_closest_value_in_array(
                                        cons.m2A(original_interface), cons.m2A(self.elongated_locpot_vec[:, 0]))
                                elif not self.new_interface is None:
                                    index_interface, interface_pos = self.index_new_interface, self.new_interface
                                else:
                                    index_interface, interface_pos = find_closest_value_in_array(
                                        self.original_interface, self.elongated_locpot_vec[:, 0])
                                if cons.m2A(ref_pos) <= cons.m2A(interface_pos):
                                    interface_pos = cons.m2A(interface_pos) + cons.m2A(delta)
                                # index_interface, interface_pos = self.locp.find_interface(x=self.elongated_locpot_vec[:, 0],
                                #                                                       y=self.elongated_locpot_vec[:, 1])
                                if cons.m2A(self.original_interface - self.original_interface * 0.1) <= cons.m2A(interface_pos) <= cons.m2A(self.original_interface + self.original_interface * 0.1):
                                    self.index_original_interface, self.original_interface = find_closest_value_in_array(cons.m2A(interface_pos),cons.m2A(self.converged_locpot_vec[:, 0]))
                                    self.index_new_interface, self.new_interface = self.index_original_interface, self.original_interface
                                else:
                                    self.index_new_interface, self.new_interface = find_closest_value_in_array(cons.m2A(interface_pos), cons.m2A(self.elongated_locpot_vec[:, 0]))
                                    self.new_interface = cons.A2m( self.new_interface)
                            else:
                                if not self.ref_point is None:
                                    if self.ref_point >= pos_to_insert:
                                        self.ref_point += delta
                            self.current_locpot_vec = self.elongated_locpot_vec
                            return self.elongated_locpot_vec
                        else:
                            elongated_locpot_vec = self.update_converged_spatial_grid(
                                vecor_to_update=elongated_locpot_vec, update_converged_vec=False,
                                update_interface=False)
                            return elongated_locpot_vec

            else:
                ## from itself. Namely - searching for bulk-like potential form, and then inserting it for enlongating the locpot.
                if not locpot_vector is None:
                    z = locpot_vector[:,0]
                    v = locpot_vector[:,1]
                else:
                    z = self.current_locpot_vec[:,0]
                    v = self.current_locpot_vec[:,1]
                if self.Has_interface:
                    if interface_position is None:
                        if self.new_interface is None:
                            ind_interface, interface_position  = self.locp.find_interface(x=z,y=v)
                        else:
                            ind_interface, interface_position = self.index_new_interface,self.new_interface

                z = cons.A2m(z)
                original_z_length = z[-1] - z[0]

                if self.Has_interface:
                    interface_position = cons.m2A(interface_position)
                ## both sides elongation
                if self.Has_interface:
                    if side_from_itself == 'both':
                        if not self.limits_for_itself is None:
                            z_right,v_right,start_position_right = find_bulk_like_potential(z,v,interface_position,num_of_peaks = 3,
                                                right = True,limits=self.limits_for_itself)
                            z_left,v_left,start_position_left = find_bulk_like_potential(z, v, interface_position, num_of_peaks = 3,
                                                left = True,limits=self.limits_for_itself)
                        else:
                            z_right,v_right,start_position_right = find_bulk_like_potential(z,v,interface_position,num_of_peaks = 3,
                                                right = True)
                            z_left,v_left,start_position_left = find_bulk_like_potential(z, v, interface_position, num_of_peaks = 3,
                                                left = True)
                        z_right, v_right = adjust_grid_density(self.grid_density,z_right, v_right)
                        z_right = cons.m2A(z_right)
                        z_left, v_left = adjust_grid_density(self.grid_density, z_left, v_left)
                        z_left = cons.m2A(z_left)
                        init_len = cons.m2A(self.current_locpot_vec[:,0][-1])
                        elongated_locpot_vec = self.locp.elongate_locpot(manual=True, pos_to_insert=start_position_left,
                            multi_manual=multi_manual,locpot_vec=to_2_column_mat(self.current_locpot_vec) ,z_to_insert_manual=z_left,v_to_insert_manual=v_left)
                        differ = to_2_column_mat(elongated_locpot_vec)[:,0][-1] - init_len
                        elongated_locpot_vec = self.locp.elongate_locpot(manual=True, pos_to_insert=start_position_right+differ,
                            multi_manual=multi_manual, z_to_insert_manual=z_right+differ,v_to_insert_manual=v_right,
                            locpot_vec=to_2_column_mat(elongated_locpot_vec))
                    ## only left side elongation
                    elif side_from_itself == 'left':
                        if not self.limits_for_itself is None:
                            z_left, v_left, start_position_left = find_bulk_like_potential(z, v, interface_position,num_of_peaks = 3,
                                                                                           left=True,limits=self.limits_for_itself)
                            z_left, v_left = adjust_grid_density(self.grid_density, z_left, v_left)
                        else:
                            z_left, v_left, start_position_left = find_bulk_like_potential(z, v, interface_position,num_of_peaks = 3,
                                                                                           left=True)
                            z_left, v_left = adjust_grid_density(self.grid_density, z_left, v_left)
                        elongated_locpot_vec = self.locp.elongate_locpot(manual=True, pos_to_insert=start_position_left,
                            multi_manual=multi_manual,z_to_insert_manual=z_left, v_to_insert_manual=v_left,locpot_vec=to_2_column_mat(self.current_locpot_vec))
                    ## only right side elongation
                    elif side_from_itself == 'right':
                        if not self.limits_for_itself is None:
                            z_right, v_right, start_position_right = find_bulk_like_potential(z, v, interface_position,num_of_peaks = 3,
                                                                                              right=True,limits=self.limits_for_itself)
                            z_right, v_right = adjust_grid_density(self.grid_density, z_right, v_right)
                        else:
                            z_right, v_right, start_position_right = find_bulk_like_potential(z, v, interface_position,num_of_peaks = 3,
                                                                                              right=True)
                            z_right, v_right = adjust_grid_density(self.grid_density, z_right, v_right)
                        elongated_locpot_vec = self.locp.elongate_locpot(manual=True, pos_to_insert=start_position_right,
                            multi_manual=multi_manual,z_to_insert_manual=z_right,v_to_insert_manual=v_right,locpot_vec=to_2_column_mat(self.current_locpot_vec))
                else:
                # Namely - does not have an interface, handling manually, elongating from itself:
                    if self.limits_for_itself is None:
                    # If limits for allocating the range of the calculation were not supplied:
                        z, v = multiply_z_v_vecs(z, v,multi=multi_manual)
                        z, v = adjust_grid_density(self.grid_density, z, v)
                        elongated_locpot_vec = to_2_column_mat(np.column_stack((z,v)))
                    else:
                    # Performimg the elongation on a region within the system, defined by limits for allocating the desired range to look for bulk like locpot.
                        z,v,start_position = find_bulk_like_potential(z,v,0,num_of_peaks = 3,
                                            limits=self.limits_for_itself)
                        z, v = adjust_grid_density(self.grid_density, z, v)
                        z = cons.A2m(z)
                        v = cons.eV2J(v)
                        elongated_locpot_vec,delta,temp_point= self.locp.elongate_locpot(manual=True, pos_to_insert=start_position,
                            multi_manual=multi_manual,z_to_insert_manual=z, v_to_insert_manual=v,locpot_vec=to_2_column_mat(self.current_locpot_vec),return_left_increment = True)

                ## for all cases (from itself elongation) - updating elongated vector of the class instance.
                if To_update:
                    if self.Has_interface:
                        if not self.new_interface is None:
                            index_interface, interface_pos = self.index_new_interface, self.new_interface
                        else:
                            index_interface, interface_pos = find_closest_value_in_array(
                                self.original_interface, elongated_locpot_vec[:, 0])
                        if side_from_itself == 'both':
                            interface_pos = interface_pos + differ
                        elif side_from_itself == 'left':
                            interface_pos = cons.m2A(interface_pos) + cons.m2A(elongated_locpot_vec[:,0][-1] - elongated_locpot_vec[:,0][0]) - cons.m2A(original_z_length)
                    self.elongated_locpot_vec = to_2_column_mat(elongated_locpot_vec)
                    self.elongated_locpot_vec = self.update_converged_spatial_grid(
                        vecor_to_update=to_2_column_mat(self.elongated_locpot_vec), update_converged_vec=False, update_interface=False)
                    if self.Has_interface:
                        #interface_position = np.abs((self.elongated_locpot_vec[:,0][-1] - self.elongated_locpot_vec[:,0][0]) - original_z_length) + interface_position
                        index_interface, interface_pos = find_closest_value_in_array(interface_pos,cons.m2A(self.elongated_locpot_vec[:,0]))
                        if cons.m2A(self.original_interface - self.original_interface * 0.1) <= interface_pos <= cons.m2A(self.original_interface + self.original_interface * 0.1):
                            self.index_original_interface, self.original_interface = find_closest_value_in_array(interface_pos ,
                                     cons.m2A(self.converged_locpot_vec[:,0]))
                            self.index_new_interface, self.new_interface = self.index_original_interface, self.original_interface
                        else:
                            self.index_new_interface, self.new_interface = index_interface, interface_pos
                        self.current_locpot_vec = self.elongated_locpot_vec
                    else:
                        if not self.ref_point is None:
                            if self.ref_point >= pos_to_insert:
                                self.ref_point += delta
                    self.current_locpot_vec=self.elongated_locpot_vec
                    return self.elongated_locpot_vec
                else:
                    elongated_locpot_vec = to_2_column_mat(elongated_locpot_vec)
                    elongated_locpot_vec = self.update_converged_spatial_grid(
                        vecor_to_update=to_2_column_mat(elongated_locpot_vec), update_converged_vec=False,
                        update_interface=False)
                    return elongated_locpot_vec
        else:
            print('2D cases have not been programmed yet')

    def update_converged_spatial_grid(self, vecor_to_update = None, update_converged_vec = True,update_interface = False):
        '''
        **Calculate spatial grid applying the converged grid density, for the interface system.**

        Parameters
        ----------
        vecor_to_update : `numpy.ndarray`, (N, 2), optional, default: None
                This is a 2 column matrix. First colmn is ``z``, the spatial coordinates vector and second is ``v``, the local potential vector.
                If we wish apply this method on not related vector, not an object attribute.
        update_converged_vec : bool, optional, default: True
                A flag indicates whether to update the instance attribute with the new converged
                vector we obatin through this method.
        update_interface : bool, optional, default: False
                A flag indicates whether to update the instance attribute of the new interface found with the
                new interface position as we get by applying this method.

        Returns
        -------
        None
        '''
        if vecor_to_update is None:
            self.locp.locpot_vec = to_2_column_mat(self.locp.locpot_vec)
            vec_to_be_conv = self.locp.locpot_vec
        else:
            vec_to_be_conv = vecor_to_update
            vec_to_be_conv = to_2_column_mat(vec_to_be_conv)
        vec_to_be_conv[:,0] = cons.A2m(vec_to_be_conv[:,0])
        L = vec_to_be_conv[-1,0]
        self.N = L * self.grid_density
        self.N = np.int64(self.N)
        if self.N == 0:
            L = cons.m2A(L)
            self.N = L * self.grid_density
            self.N = np.int64(self.N)
        if self.N == 0:
            self.grid_density = self.grid_density*(1/cons.A2m(1))
            self.N = L * self.grid_density
            self.N = np.int64(self.N)
        z,v = interpolate_pchip(self.N,vec_to_be_conv)
        if update_converged_vec:
            self.converged_locpot_vec = np.vstack((z,v))
            self.converged_locpot_vec = to_2_column_mat(self.converged_locpot_vec)
            if not self.current_locpot_vec is None:
                try:
                    if self.elongated_locpot_vec is None and len(self.current_locpot_vec[:,0]) < len(self.converged_locpot_vec[:,0]):
                        self.current_locpot_vec = self.converged_locpot_vec
                except IndexError:
                    if self.elongated_locpot_vec is None:
                        self.current_locpot_vec = self.converged_locpot_vec
            else:
                self.current_locpot_vec = self.converged_locpot_vec

        if self.Has_interface:
            if update_interface:
                index_interface, interface_pos = self.locp.find_interface(x = z, y = v )
                if self.original_interface - self.original_interface * 0.1 <= interface_pos <= self.original_interface + self.original_interface * 0.1:
                    self.index_original_interface, self.original_interface = find_closest_value_in_array(interface_pos,z)
        return to_2_column_mat(np.column_stack((z,v)))

    def find_initial_position_to_center_psi0(self, init_side = 'Left', manual = False,manual_pos = None, index = False ):
        '''

        Parameters
        ----------
        init_side : str, {'Left', 'Right'}, Optional, default: 'Left'
                The Choices are in the brackets. Determines what side of the interface to look for the inialization position.
        manual : int or float, optional, default: None
                It can be int for index insertion or a float for position insertion.
                Instead for automatically look for initial position, you can supply it directly via this argument.
                Also it assume that it is given as a spatial position.
        manual_pos: int or float, optional, default: None
                If specified, this will be the actual position that corresponding the local potential vector - where the wave-function will be initialized at.
        index : bool, optional, default: False
                If it is ``True``, then the manual argument will be read as index instead of spatial position.
        Returns
        -------
        z0_position, z0_index : float, int
                The position and the matching index in the interfce system locpot vector,
                where psi0 will be initialized at. By default it will be at the middle of the left-side material.
        '''
        locpot_vec = self.get_most_relevant_z_coordinate_vec()
        locpot_vec = to_2_column_mat(locpot_vec)

        if self.Has_interface:
            if self.new_interface is None:
                interface_pos= self.original_interface
            else:
                interface_pos = self.new_interface
        z0 = 0
        if not manual:
            if self.Has_interface:
                if init_side == 'Left':
                    # z_left =  [i for i in self.locp.locpot_vec[:, 0] if i <= interface_pos]
                    all_min = self.allmin[:, :][self.allmin[:, 0] < interface_pos]
                    if len(all_min) == 0:
                        interface_pos = cons.m2A(interface_pos)
                        all_min = self.allmin[:, :][self.allmin[:, 0] < interface_pos]
                    mid_min = np.int64(np.fix(len(all_min[:, 0]) / 2)) + np.mod(len(all_min[:, 0]), 2) - 1
                    mid_min = all_min[mid_min,0]
                    mid_min = self.cons.m2A(mid_min)
                    z0_index, z0 = find_closest_value_in_array(mid_min, locpot_vec[:,0])
                elif init_side == 'Right':
                    #z_right =  self.allmin[:, :][self.allmin[:, 0] > interface_pos]
                    all_min = self.allmin[:, :][self.allmin[:, 0] > interface_pos]
                    mid_min = np.int64(np.fix(len(all_min[:, 0]) / 2)) + np.mod(len(all_min[:, 0]), 2) - 1
                    mid_min = all_min[mid_min,0]
                    mid_min = self.cons.m2A(mid_min)
                    z0_index, z0 = find_closest_value_in_array(mid_min, locpot_vec[:,0])
            else:
                all_min = self.allmin[:, :]
                mid_min = np.int64(np.fix(len(all_min[:, 0]) / 2)) + np.mod(len(all_min[:, 0]), 2) - 1
                mid_min = all_min[mid_min, 0]
                mid_min = self.cons.m2A(mid_min)
                z0_index, z0 = find_closest_value_in_array(mid_min, locpot_vec[:, 0])

        else:
            all_min = self.allmin[:, :]
            if not index:
                if manual_pos is None:
                    print('You chose manual initializztion, however you did not supplied an initialization position')
                    return None
                else:
                    z0_index, z0 = find_closest_value_in_array(manual_pos,all_min[:,0])
            else:
                manual_pos = np.int64(manual_pos)
                if 0 <= manual_pos <= len(locpot_vec[:, 0]) -1:
                    z0 = locpot_vec[:, 0][ manual_pos]
                    z0_index, z0 = find_closest_value_in_array(z0, all_min[:, 0])
                else:
                    print('Your index is out of the range')
                    return None
        return z0_index, z0

    def find_new_interface(self):
        '''
        **After updating our spcial grid, and applying the grid density that we calculated at `stage_1`,
        this method aims to point out the new interface of the updated locpot vector.**

        Returns
        -------
        The new interface position. (in Angstrum).
        '''
        if self.Has_interface:
            left_material = Locpot_yair(self.locp.locpot_bulk_materials[0], is_bulk_material= True)
            z_added = (left_material.locpot_vec[:,0][-1] - left_material.locpot_vec[:,0][0]) * self.multi_left * 2
            N_added = np.int64(z_added  * self.grid_density)
            index_new_interface, new_interface = self.locp.find_interface(self.converged_locpot_vec[:,0],self.converged_locpot_vec[:,1])
            temp_index, temp_pos = find_closest_value_in_array(self.original_interface, self.converged_locpot_vec[:,0])
            temp_index =  temp_index + N_added

            index_new_interface, new_interface = self.locp.find_interface(self.converged_locpot_vec[index_new_interface:temp_index, 0],
                                                                          self.converged_locpot_vec[index_new_interface:temp_index, 1])

            self.index_new_interface, self.new_interface = index_new_interface, new_interface
            return index_new_interface, new_interface
        else:
            return  len(self.converged_locpot_vec[:,0]) -1 , self.converged_locpot_vec[:,0][-1]

    def initialize_psi0(self,init_side = 'Left',manual_center = False,manual_z0 = None, manual_z = None, manual_v = None,To_update = True, manual_psi_dic=None):
        '''

        Parameters
        ----------
        init_side : str, {'Left', 'Right'}, optional, default: 'Left'
                Enables to choose from what side of the interface to initialize the wave function.
        manual_center : bool, optional, default: False
                Enables th choose whether to initialize the wave function at a certain ``z`` coordinate as an input from the user.
        manual_z0 : float, optional, default: None
                Manual input for initializing the wave function at a certain desired location. The wave function will be centered at z0_manual.
        manual_z, manual_v : np.array, array_like, optional, default: None
                Enables flexibility in initializing `psi0` at a given locpot vector, as ``z_input`` and ``v_input``.
        To_update : bool, optional, default: True
                A flag to indicate if the changes that have being made are going to be updated as the instance attributes.
        manual_psi_dic : dict, optional, default: None
                The dictionary has to be from the structure of : `{'sigma': np.float , 'k0': np.float, ... }`
                It enables to initilize the psi0 as we wish by giving it an input for the relevant parameters.

        Returns
        -------
        psi0 : np.array, array_like
                Wave-function values vector.
        locpot : numpy.ndarray, (N,2)
                The corresponding spatial coordinates vector
        '''
        if not manual_center:
            if self.Has_interface:
                z0 = self.find_initial_position_to_center_psi0(init_side=init_side)[1]
            else:
                z0 = self.find_initial_position_to_center_psi0()[1]
        else:
            if manual_z0 is None:
                print('You did not supplied manual z0 to center the initial wacve function. It works '
                      'as it was not manually set')
                if self.Has_interface:
                    z0 = self.find_initial_position_to_center_psi0(init_side=init_side)[1]
                else:
                    z0 = self.find_initial_position_to_center_psi0()[1]

            else:
                if self.Has_interface:
                    z0 = self.find_initial_position_to_center_psi0(init_side=init_side,manual=True,manual_pos=manual_z0)[1]
                else:
                    z0 = self.find_initial_position_to_center_psi0(manual=True,manual_pos=manual_z0)[1]

        if not manual_psi_dic is None:
            sigma = manual_psi_dic['sigma']
            k0 = manual_psi_dic['k0']
        else:
            sigma = self.psi0_dic['sigma']
            k0 = self.psi0_dic['k0']
        if  manual_z is None or manual_v is None:
            z,v = self.get_most_relevant_z_coordinate_vec()
        else:
            z = manual_z
            v = manual_v
        psi0 = get_psi0(k0, sigma, z0, z, units='Angstrum')[1]
        if To_update:
            self.psi0 = get_psi0(k0, sigma, z0, z, units='Angstrum')[1]
            self.psi0_dic['z0']=z0
        return psi0

    def get_most_relevant_z_coordinate_vec(self):
        '''

        Returns
        -------
        z, v : np.array, np.array
                z coordinate vector and v potential vector. It chooses the most relvant z and v vectors according to the steps that
                have already taken when running this function.
        '''
        # This function aims to return the latest and most updated/relevant lopot vector (local potential and spatial
        # coordinates grid vector.
        z = []
        v = []
        if not (self.elongated_locpot_vec is None):
            if len(self.elongated_locpot_vec[:,0]) > len(self.current_locpot_vec[:,0]):
                z = self.elongated_locpot_vec[:,0]
                v = self.elongated_locpot_vec[:,1]
            else:
                z = self.current_locpot_vec[:,0]
                v = self.current_locpot_vec[:,1]
        elif not (self.converged_locpot_vec is None):
            if len(self.converged_locpot_vec[:,0]) > len(self.current_locpot_vec[:,0]):
                z = self.converged_locpot_vec[:,0]
                v = self.converged_locpot_vec[:, 1]
            else:
                z = self.current_locpot_vec[:,0]
                v = self.current_locpot_vec[:,1]
        else:
            z = self.current_locpot_vec[:, 0]
            v = self.current_locpot_vec[:, 1]
        z,v = smooth_function(z,v)
        self.current_locpot_vec = np.column_stack((z,v))
        self.allmin = find_peaks_minima(self.current_locpot_vec[:, 0],self.current_locpot_vec[:, 1])
        self.allmax = find_peaks_maxima(self.current_locpot_vec[:, 0],self.current_locpot_vec[:, 1])
        return z, v

    def calculate_E0(self, psi = None, z_in = None, v_in = None):
        '''

        Parameters
        ----------
        psi : np.array, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
        z_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,0]` attribute of `Stage_2` instance.
                Vector of the spatial grid. (spatial coordinates)
        v_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,1]` attribute of `Stage_2` instance.
                Vector of the local potential.

        Returns
        -------
        E0 : float
                The expectation values of the total energy.
        T0 : float
                The expectation values of the kinetic energy.
        V0 : float
                The expectation values of the potnetial energy and potential energy, in [Joul].

        '''
        # input verification
        # ---------------------------------------------------------
        if not (z_in is None or v_in is None):
            z = z_in
            v = v_in
        else:
            z,v = self.get_most_relevant_z_coordinate_vec()
        z = to_column_vec(z)
        z = self.cons.A2m(z)
        v = to_column_vec(v)
        v = self.cons.eV2J(v)
        if not psi is None:
            psi0 = psi
        elif self.psi0 is None:
            self.initialize_psi0()
            psi0 = np.copy(self.psi0)
        else:
            psi0 = np.copy(self.psi0)
        psi0 = to_column_vec(psi0)
        psi0 = force_psi_units(psi0,units = 'Meter')
        L = self.cons.A2m(z[-1] - z[0])
        N = len(z)
        # ---------------------------------------------------------
        T0num = kinetic_energy_expectation_value(psi0, z) # Calculate the kinetic energy expectation value.
        dz = np.diff(to_1D_vec(z))[0] # Getting dz (or the difference at each consecutive spatial grid points).
        # calculationg the average potential energy for uniform deltaz
        v0num = np.real(dz * psi0.T @ np.conj(to_column_vec(to_1D_vec(v) * to_1D_vec(psi0)))) # Calculate the potential energy expectation value.

        # [J]
        v0num = np.squeeze(v0num) # Deleting any redundant axis/columns of the vector.
        # Finally calcualting the total energy expectation value.
        E0num = T0num + v0num  # [J]
        return np.float64(np.squeeze(E0num)), np.float64(np.squeeze(T0num)), np.float64(np.squeeze(v0num))

    def propagate_psi(self, psi = None, Nt = None,dt = None, z_in = None, v_in = None, path_to_save = None):
        '''

        Parameters
        ----------
        psi : np.array, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
        Nt : int, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
                The number of time-steps.
        dt : float, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance
                The size of each time step the wave-function is propagated.
        z_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,0]` attribute of `Stage_2` instance.
                Vector of the spatial grid. (spatial coordinates)
        v_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,1]` attribute of `Stage_2` instance.
                Vector of the local potential.
        path_to_save : string, optional, default:None
                The absolute path to save the figure obtained from the calculation

        Returns
        -------
        None
            This method was built mainly to produce the simulation animation. If ``To_plot`` is not set to `True`,
            then this function does not take any action.
        '''
        # input verification
        #---------------------------------------------------------
        if Nt is None:
            Nt = self.Nt
        if dt is None:
            dt = self.dt
        dt = cons.fs2sec(dt)
        z = self.cons.A2m(self.current_locpot_vec[:,0])
        v = self.cons.eV2J(self.current_locpot_vec[:,1])
        z_check, v_check = self.get_most_relevant_z_coordinate_vec()
        z_check = self.cons.A2m(z_check)
        v_check = self.cons.eV2J(v_check)
        assert np.all(z == z_check) and np.all(v == v_check)
        if psi is None:
            psi = self.psi0
        if not (z_in is None or v_in is None):
            z = z_in
            v = v_in
        if not len(psi) == len(v):
            self.psi0 = self.initialize_psi0()
        assert len(psi) == len(v)
        z = self.cons.A2m(z)
        v = self.cons.eV2J(v)
        psi = force_psi_units(psi, units='Meter')
        # ---------------------------------------------------------
        # Creating K grid
        kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
        kk = to_1D_vec(kk)

        # wave_funcs = np.zeros((self.Nt, len(psi)), dtype=np.cdouble)
        # wave_funcs[0, :] = psi
        # for q in range(1, Nt):
        #     wave_funcs[q, :] = run_one_time_step(wave_funcs[q-1, :], dt, v, kk)
        # Temporary structure to store the last two propagation-step of the wave-function.
        # It has two rows, and the number of columns is as the length of the wave-function vector.
        wave_funcs = np.zeros((2, len(psi)), dtype=np.cdouble)

        # Store at the first row the current/initial wave funtion vector.
        wave_funcs[0, :] = psi

        # It enables to plot. In this case' it turned on the simulation animation production.
        if self.To_plot :
            print('Creating propagation animation...')

            # Creating plotting objects.

            fig, axes = plt.subplots(2, 1, figsize=(8, 8))
            ax = axes[0]

            # Creating empty lines and text-box to be later updated at each propagation step
            # which will be equivalent to be updated at each frame of the simulation animation.
            line1, = ax.plot([], [], 'r-', lw=2, markersize=8, label=r'$| \psi(t)) |^2$')
            line2, = ax.plot([], [], 'b--', lw=2, markersize=8, label=r'$real(\psi(t))) $')
            time_text = ax.text(0.1, 0.1, '', fontsize=15,
                                bbox=dict(facecolor='white', edgecolor='black'),
                                transform=ax.transAxes)

            # Setting axes labels.
            ax.set_xlim(0, 1e10*z[-1])
            ax.set_ylim(-0.6, 0.7)
            pxlabel = 'Position z [A]'
            ptitle = r'Interface system $\left| \psi(z,t) \right\rangle$'
            my_fps = 20
            # animating function
            def animate(j):
                nonlocal wave_funcs
                # For the first step, propagate the initial wave-function.
                if j == 0:
                    line1.set_data(z * 1e10, np.abs(wave_funcs[0, :]**2)*1e-10)
                    line2.set_data(z * 1e10, np.real(wave_funcs[0, :])*1e-5)
                    time_text.set_text('t={:.2f}'.format(j/my_fps))

                else:
                    # For all the other steps, propagate the last propagated wave function (from previous step)
                    # and store it at the second row of the storage-structure we created above.
                    # After updaing the lines (which are objects to be plotted at the same frame of the anumation
                    # update this propagation step with the first row, so the next step will act on it.
                    wave_funcs[1, :] = run_one_time_step(wave_funcs[0, :], dt, v,z, kk)
                    line1.set_data(z * 1e10, np.abs(wave_funcs[1, :]**2)*1e-10)
                    line2.set_data(z * 1e10, np.real(wave_funcs[1, :])*1e-5)
                    time_text.set_text('t={:.2f}'.format(j/my_fps))
                    wave_funcs[0, :] = wave_funcs[1, :]

            # I Decided that each animation should last 10 seconds in real time.


            ax.set_ylabel('$|\psi(z,t)|^2 ,\psi(z,t) $', fontsize=20)
            ax.legend(loc='lower right')
            ax.set_title(ptitle)

            # If we have interface in our system, it plots vertical line at the exact position of the interface.
            if self.Has_interface:
                if not self.new_interface is None:
                    ax.axvline(self.new_interface, ymin=-0.7, ymax=1)
                    ax.annotate('Interface position', xy=(self.new_interface + 0.5, 0.5),  xycoords='data',transform=ax.transAxes)
                else:
                    ax.axvline(self.original_interface, ymin=-0.7, ymax=1)
                    ax.annotate('Reference Point', xy=(self.original_interface + 0.5, 0.5), xycoords='data',
                                transform=ax.transAxes)

            elif not (self.ref_point is None or self.ref_point == 0 or self.ref_point ==
                      self.current_locpot_vec[:, 0][-1]):
                ax.axvline(self.ref_point, ymin=-0.7, ymax=1)
                ax.annotate('Reference Point', xy=(self.ref_point + 0.5, 0.5),  xycoords='data',transform=ax.transAxes)
            else:
                ax.axvline(self.original_interface, ymin=-0.7, ymax=1)
                ax.annotate('Reference Point', xy=(self.original_interface + 0.5, 0.5),  xycoords='data',transform=ax.transAxes)

            ax2 = axes[1]

            # Plotting the local potential vs the spatial grid/coordinates below the plot of the wave-function propagation
            ax2.plot( z*1e10, self.cons.J2eV(v),label = 'Local potential')
            if self.Has_interface:
                if not z_in is None or not v_in is None:
                    ind_interface, inter_position = find_interface(z_in,v_in)
                    ax2.axvline( cons.m2A(inter_position), ymin=np.min(self.cons.J2eV(v)) - 0.1,
                                ymax=np.max(self.cons.J2eV(v)) + 0.1)
                if not self.new_interface is None:
                     ax2.axvline(self.new_interface,ymin=np.min(self.cons.J2eV(v))-0.1,ymax=np.max(self.cons.J2eV(v))+0.1)
                else:
                    ax2.axvline(self.original_interface, ymin=np.min(self.cons.J2eV(v)) - 0.1,
                                ymax=np.max(self.cons.J2eV(v)) + 0.1)
            elif not (self.ref_point is None or self.ref_point == 0 or self.ref_point == self.current_locpot_vec[:,0][-1]):
                ax2.axvline(self.ref_point, ymin=np.min(self.cons.J2eV(v)) - 0.1,
                            ymax=np.max(self.cons.J2eV(v)) + 0.1)
            ax2.set_xlabel(pxlabel,fontsize=20)
            ax2.set_ylabel('$V(z) [eV]$', fontsize=20)
            ax2.legend(loc='lower right')
            ax2.set_xlim(0, z[-1]*1e10)
            ax2.set_ylim(np.min(self.cons.J2eV(v))-0.1,np.max(self.cons.J2eV(v))+0.1 )
            plt.tight_layout()
            ani = animation.FuncAnimation(fig, animate, frames=np.int64(Nt), interval=5)
            if path_to_save is None:
                ani.save('ani.gif', writer='pillow', fps=my_fps, dpi=300)
            else:
                ani.save("/".join(
                list(os.path.join(path_to_save, 'Propagation Animation.gif').split(
                    "\\"))), writer='pillow', fps=my_fps, dpi=300,savefig_kwargs={'transparent':True})
            print('Propagation Animation creation has been completed successfully!')
        return

    def set_To_plot(self, To_plot):
        '''

        Parameters
        ----------
        To_plot : bool
                The input from the user, this method aims to set the ``To_plot`` attribute of the instance
                and enables the plotting feature that implemented in some of the class methods.

        Returns
        -------
        None
        '''
        self.To_plot = To_plot

    def cumulative_probabilty_through_interface(self,psi = None, Nt = None,dt = None, z_in = None, v_in = None,  check_pos = None, path_to_save = None):
        '''

        Parameters
        ----------
        psi : np.array, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
        Nt : int, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
                The number of time-steps.
        dt : float, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance
                The size of each time step the wave-function is propagated.
        z_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,0]` attribute of `Stage_2` instance.
                Vector of the spatial grid. (spatial coordinates)
        v_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,1]` attribute of `Stage_2` instance.
                Vector of the local potential.
        check_pos : float, optional, default: None
                In cases where we don't have an interface and we wish supply a position
                where the cumulative probability is ggoing to be calculated.
        path_to_save : string, optional, default:None
                The absolute path to save the figure obtained from the calculation


        Returns
        -------
        results: numpy.ndarray, (N,2)
                This is a 2 columns vector, the first column vector represents the # of the time step.
                The second column vector represents the cumulative probabilty through interface.
        '''
        # input verification
        #---------------------------------------------------------
        if Nt is None:
            Nt = self.Nt
        if dt is None:
            dt = self.dt
        dt = cons.fs2sec(dt)
        z = self.cons.A2m(self.current_locpot_vec[:,0])
        v = self.cons.eV2J(self.current_locpot_vec[:,1])
        z_check, v_check = self.get_most_relevant_z_coordinate_vec()
        z_check = self.cons.A2m(z_check)
        v_check = self.cons.eV2J(v_check)
        assert np.all(z == z_check) and np.all(v == v_check)
        if psi is None:
            if not self.psi0 is None:
                 psi = self.psi0
            else:
                self.initialize_psi0()
                psi = self.psi0

        if not (z_in is None or v_in is None):
            z = z_in
            v = v_in
        assert len(psi) == len(v)
        z = self.cons.A2m(z)
        v = self.cons.eV2J(v)
        psi = force_psi_units(psi, units='Meter')
        psi = to_1D_vec(psi)
        if self.Has_interface:
            if not self.new_interface is None:
                interface_pos = self.new_interface
            else:
                interface_pos = self.original_interface
            interface_pos = self.cons.A2m(interface_pos)
        else:
            if check_pos is None:
                check_pos = len(z)/2
            check_pos = self.cons.A2m(check_pos)
            interface_pos = check_pos
        # ---------------------------------------------------------
        # Creating K grid.
        kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
        kk = to_1D_vec(kk)
        # Creating initial structure to store all the calculation being made at each step later via the loop.
        results = np.zeros((np.int64(Nt),2),dtype = complex)

        # Temporary variable to store the wave-function at each step.
        temp_psi = psi
        for i in range(np.int64(Nt)):
            # if this is the first appearance of the loop, propagate the initial wave-function.
            if i == 0:
                results[i, :] = [i, cumulative_probabilty(psi, z, interface_pos, np.diff(z)[0])]
                temp_psi = run_one_time_step(psi,dt , v, z , kk)
            # Except for the first step of the loop, propagate one-step the current wave-function stored at the temp_psi.
            else:
                results[i, :] = [i, cumulative_probabilty(temp_psi, z, interface_pos, np.diff(z)[0])]
                temp_psi = run_one_time_step(temp_psi,dt , v, z , kk)
        # If we enables to plot, this section is aiming to plot.
        if self.To_plot:
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Cumulative Probabilty Through the interface vs simulation time')
            ax = plt.subplot(gs[0])
            ax.ticklabel_format(useOffset=False, useMathText=True, style='sci')
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            ax.set_xlabel('Time simulation, in secs')
            ax.set_ylabel('Cumulative probabilty through the interface')
            plat_val = plateau_val(np.float64(np.real((results[:,0]))*dt), np.real(results[:,1]))
            if plat_val == 0 or plat_val < 0.1:
                 plat_val = np.real(results[: , 1][-1])
            ax.plot(np.real(np.float64(results[: , 0])), np.real(results[:,1]),label = 'Cumulative probailty through the interface is = {:.4f}'.format(np.real(plat_val)))
            ax.grid()
            ax.legend()
            if path_to_save is None:
                plt.savefig('cumulative probability through the interface vs simulation time' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("/".join(
                    list(os.path.join(path_to_save, 'cumulative probability through the interface vs simulation time').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)


        return results

    def converge_system_size(self ,psi = None, Nt = None,dt = None, z_in = None, v_in = None, To_update = True,
                             Elongate_from_itself = True, Multi = 2, iteration_num = 1, init_side = 'Left',
                             manual_center = False,manual_z0 = None, manual_z = None, manual_v = None,manual_psi_dic=None,path_to_save = None):
        '''
        More accurate name - converge simulation overall time
        Parameters
        ----------
        psi : np.array, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
        Nt : int, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
                The number of time-steps.
        dt : float, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance
                The size of each time step the wave-function is propagated.
        z_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,0]` attribute of `Stage_2` instance.
                Vector of the spatial grid. (spatial coordinates)
        v_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,1]` attribute of `Stage_2` instance.
                Vector of the local potential.
        To_update : bool, optional, default: True
                A flag that indicates whether to update the instance attributes with the calculated converged parameters.
        Elongate_from_itself : bool, optional, default: True
                A flag that tells from where to take the bulk-like potential to be
                inserted during the elongation proccess.
        Multi : int, optional, default: 2
                A flag that tells how many time to multiply the inserted potenial during the elongation proccess.
        iteration_num : int, optional, default: 20
                How many iteration the convergence proccess will be hold.
                manual_center : bool, optional, default: False
                Enables th choose whether to initialize the wave function at a certain ``z`` coordinate as an input from the user.
                manual_center : bool, optional, default: False
                Enables th choose whether to initialize the wave function at a certain ``z`` coordinate as an input from the user.
        init_side : str, {'Left', 'Right'}, optional, default: 'Left'
                For the psi0 initialization. Enables to choose from what side of the interface to initialize the wave function.
        manual_center : bool, optional, default: False
                For the psi0 initialization. Enables th choose whether to initialize the wave function at a certain ``z`` coordinate as an input from the user.
        manual_z0 : float, optional, default: None
                For the psi0 initialization. Manual input for initializing the wave function at a certain desired location. The wave function will be centered at z0_manual.
        manual_z, manual_v : np.array, array_like, optional, default: None
                For the psi0 initialization. Enables flexibility in initializing `psi0` at a given locpot vector, as ``z_input`` and ``v_input``.
        manual_psi_dic : dict, optional, default: None
                For the psi0 initialization. The dictionary has to be from the structure of : `{'sigma': np.float , 'k0': np.float, ... }`
                It enables to initilize the psi0 as we wish by giving it an input for the relevant parameters.
        path_to_save : string, optional, default:None
                The absolute path to save the figure obtained from the calculation
        Returns
        -------
        converged_z : np.array
                The converged vector of the spatial grid. (spatial coordinates)
        converged_v : np.array
                The converged vector of the local potential
        converged_psi : np.array
                The converged wave-function vector.
        converged_Nt : int
                The converged time steps that were being made.
        results: numpy.ndarray, (N,2)
                This is a 2 columns vector, the first column vector represents the # of the time step.
                The second column vector represents the cumulative probabilty through interface.
        simulation_time : float
                The total time of the simulation. It is given in units of seconds. It is the multiplication of ``Nt*dt``.
        '''
        # input verification
        #---------------------------------------------------------
        if Nt is None:
            Nt = self.Nt
            Nt = np.int64(Nt)
        if dt is None:
            dt = self.dt
        dt = cons.fs2sec(dt)
        overall_time = Nt * dt
        z = self.cons.A2m(self.current_locpot_vec[:,0])
        v = self.cons.eV2J(self.current_locpot_vec[:,1])
        z_check, v_check = self.get_most_relevant_z_coordinate_vec()
        z_check = self.cons.A2m(z_check)
        v_check = self.cons.eV2J(v_check)
        assert np.all(z == z_check) and np.all(v == v_check)
        if psi is None:
            if self.psi0 is None:
                self.initialize_psi0(init_side= init_side, manual_center= manual_center,manual_z0 = manual_z0, manual_z = manual_z, manual_v = manual_v,manual_psi_dic=manual_psi_dic)
            psi = self.psi0
        if not (z_in is None or v_in is None):
            z = self.cons.A2m(z_in)
            v = self.cons.eV2J(v_in)
        assert len(psi) == len(v)
        psi = force_psi_units(psi, units='Meter')
        psi = to_1D_vec(psi)
        converged_z = z
        converged_v = v
        converged_z = cons.A2m(converged_z)
        converged_v = cons.eV2J(converged_v)
        converged_psi = psi
        converged_psi = self.initialize_psi0(manual_z=converged_z, manual_v=converged_v,manual_center= True,manual_z0 = self.psi0_dic['z0'], manual_psi_dic=self.psi0_dic)
        converged_psi = force_psi_units(converged_psi,units='Meter')
        converged_Nt = Nt
        converged_overall_time = overall_time
        # ---------------------------------------------------------
        # Creating K grid
        kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
        kk = to_1D_vec(kk)

        # First calculation of cumulative_probabilty_through_interface before entering the loop
        temp_flag = self.To_plot
        self.set_To_plot(To_plot=False)
        print('-----------------------------------------')
        print('-----------------------------------------')
        print('Stage_2 converge system size')
        print('First Cumulutive probabilty through the interface calculation')
        results = self.cumulative_probabilty_through_interface(psi = converged_psi, Nt = converged_Nt,dt = dt, z_in = converged_z, v_in = converged_v)
        print('Finished First Cumulutive probabilty through the interface calculation')
        self.set_To_plot(To_plot=temp_flag)
        iteration = 0  # Counter for the iterations that are going to be performed.
        plt.xlabel('simulation time in sec')
        plt.ylabel('cumulative probabilty')
        alter_flag = True # True for elongating the locpot, Flase for enlarging Nt.
        if reach_plateau(results[:,0],results[:,1]): # If the initial state of our system has reached plateau,
                                                     # There is no need to enter the loop.

            print('..............................')
            print('The cumulative probability through the interface has reached plateau before entering the loop.')
            reach_plat = True
            plt.plot(results[:,0]*dt, results[:,1],label='iteration = {}, Nt = {}, length_z = {:.2f} nm'.format(iteration,converged_Nt,cons.m2A(converged_z[-1])/10))
            plt.legend()
            plt.show()
            if path_to_save is None:
                plt.savefig('cumulative probability through the interface vs dt' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("_".join(
                    list(os.path.join(path_to_save, 'cumulative probability through the interface vs dt').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)
        elif converged_z[-1] > cons.A2m(500): # I decided not to elongate the system longer than 50 nm. However, it does not tell that we reached plateau.
            print('Stage_2 converge system size')
            print('..............................')
            print('The length of the interface system is longer than the limit of 50 nm before entering the loop.')

            reach_plat = False
        else:
            reach_plat = False
        # entering loop: conditions: have not arraived plateau, have not exceeded the limit of 50 nm system,
        # and not got over the specified iterations number.
        if not reach_plat:
            print('Stage_2 converge system size')
            print('..............................................................')
        while (not reach_plateau(results[:,0],results[:,1])) and converged_z[-1] <= cons.A2m(500) and iteration <= iteration_num:
            if iteration == 0:
                print('Enering The main loop')
            #if alter_flag: # Alternating procedure at each iteration. One time the system coordinates elongation, the
                # other time increasing Nt, and then vice versa.
            #alter_flag = False
            #mat= self.elongate_interface_potential(from_iteslf=Elongate_from_itself,
            #                        side_from_itself='right',locpot_vector=to_2_column_mat(np.column_stack((converged_z, converged_v))))
            # converged_z, converged_v = mat.T
            # converged_z = cons.A2m(converged_z)
            # converged_v = cons.eV2J(converged_v)
            # # if we reached more then 10 iterations, and have not yet to go over 50 nm system length,
            # # it should elongate the system one more time at this current iteration.
            # if iteration >=10 and converged_z[-1] >= cons.A2m(500) :
            #     mat = self.elongate_interface_potential(from_iteslf=Elongate_from_itself,
            #                                                                  side_from_itself='right',
            #                                                                  locpot_vector=to_2_column_mat(
            #                                                                      np.column_stack(
            #                                                                          (converged_z, converged_v))))
            #     converged_z, converged_v = mat.T
            #     converged_z = cons.A2m(converged_z)
            #     converged_v = cons.eV2J(converged_v)

        # else:
        #     # Increasing Nt by the factor of alpha.
            converged_overall_time = self.alpha * converged_overall_time

            converged_Nt = np.int64(np.round(converged_overall_time / dt))
        #     alter_flag = True

            # Adapt the length of the wave-function vector to the new length of the coordinate vector and
            # the locpot vector. Then re-calculate cumulative_probabilty_through_interface.
            converged_psi = self.initialize_psi0(manual_z=converged_z, manual_v=converged_v, manual_center=True,
                                                 manual_z0=self.psi0_dic['z0'], manual_psi_dic=self.psi0_dic)
            temp_flag = self.To_plot
            self.set_To_plot(To_plot=False)
            results = self.cumulative_probabilty_through_interface(psi=converged_psi, Nt=converged_Nt, dt=dt,
                                                                   z_in=converged_z, v_in=converged_v)
            self.set_To_plot(To_plot=temp_flag)
            plt.plot(results[:,0]*dt, results[:,1],label='iteration = {}, Nt = {}, length_z = {:.2f} nm'.format(iteration,converged_Nt,cons.m2A(converged_z[-1])/10))
            print('iteration number {}'.format(iteration))
            print('Nt is = {}'.format(converged_Nt))
            print('Overall simulation time is = {} sec'.format(converged_overall_time))
            print('length of z is nm= {:.2f}'.format((cons.m2A(converged_z[-1]))/10))
            print('--------------------------------------------------------------')
            iteration +=1

            if reach_plateau(results[:,0],results[:,1]):
                print('Reached plateau...')
                print('==============================================================')
                reach_plat = True
            elif converged_z[-1] >= cons.A2m(500):
                print('--------------------------------------------------------------')
                print('Exceeded 50 nm system length')
                print('--------------------------------------------------------------')
            elif iteration > iteration_num:
                print('Got over {} iterations'.format(iteration))
                print('==============================================================')

        # If we have not reached plateau, and still have not gone over the specified number of iterations,
        # enter this loop, while increasing only Nt by the factor of alpha.
        if reach_plat == False and iteration < iteration_num:
            while (not reach_plateau(results[:,0],results[:,1])) and iteration <= iteration_num:
                converged_overall_time = self.alpha * converged_overall_time
                converged_Nt = np.int64(np.round(converged_overall_time / dt))
                #converged_Nt = np.int64(self.alpha * converged_Nt)
                converged_psi = self.initialize_psi0(manual_z=converged_z, manual_v=converged_v, To_update=False)
                temp_flag = self.To_plot
                self.set_To_plot(To_plot=False)
                results = self.cumulative_probabilty_through_interface(psi=converged_psi, Nt=converged_Nt, dt=dt,
                                                                       z_in=converged_z, v_in=converged_v)
                self.set_To_plot(To_plot=temp_flag)
                plt.plot(results[:, 0]*dt , results[:, 1],
                         label='iteration = {}, Nt = {}, length_z = {:.2f} nm'.format(iteration, converged_Nt,
                                                                                      cons.m2A(converged_z[-1]) / 10))

                print('iteration number {}'.format(iteration))
                print('Nt is = {}'.format(converged_Nt))
                print('Overall simulation time is = {} sec'.format(converged_overall_time))
                print('length of z is nm= {:.2f}'.format((cons.m2A(converged_z[-1])) / 10))
                print('--------------------------------------------------------------')
                iteration += 1
                if reach_plateau(results[:, 0], results[:, 1]):
                    print('Reached plateau...')
                    print('==============================================================')
                    reach_plat = True
                elif iteration > iteration_num:
                    print('Got over {} iterations'.format(iteration))
                    print('==============================================================')
        plt.legend()
        plt.show()
        if path_to_save is None:
            plt.savefig('cumulative probability through the interface vs dt' + ".svg", format="svg", dpi=300)
        else:
            plt.savefig("_".join(
                list(os.path.join(path_to_save, 'cumulative probability through the interface vs dt').split(
                    "\\"))) + ".svg",
                        format="svg", dpi=300)
        if To_update:
            self.psi0 = converged_psi
            self.Nt = converged_Nt
            converged_z = to_1D_vec(converged_z)
            converged_v = to_1D_vec(converged_v)
            self.current_locpot_vec = to_2_column_mat(np.column_stack((converged_z, converged_v)))
        return converged_z, converged_v, converged_psi, converged_Nt, results, self.cons.fs2sec(converged_Nt*dt)


    def converge_time_step(self,psi = None, Nt = None,dt = None,time_sim = None, z_in = None, v_in = None, To_update = True, To_plot = False, iterations = 8, check_pos = None, tol = 0.005,path_to_save = None):
        '''

        Parameters
        ----------
        psi : np.array, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
        Nt : int, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance.
                The number of time-steps.
        dt : float, optional, default: None
                If not supplied, the default is the wave-function vector attribute of `Stage_2` instance
                The size of each time step the wave-function is propagated.
        time_sim : float, optional, default: None
                If not supplied, it will be calculated from the product ``Nt*dt``.
                However, it is supplied, it will be taken into account, and the dt will be taken into account too. Then Nt will be recalculated.
        z_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,0]` attribute of `Stage_2` instance.
                Vector of the spatial grid. (spatial coordinates)
        v_in : np.array, optional, default: None
                If not supplied, the default is taken from `locpot_vec[:,1]` attribute of `Stage_2` instance.
                Vector of the local potential.
        To_update : bool, optional, default: True
                A flag that indicates whether to update the instance attributes with the calculated converged parameters.
        To_plot : bool, optional, defulat: False
                A flag to determine whether to plot or not.
        iterations : int, optional, default: 40
                A flag the enables the user define how many times the converges test will run.
        check_pos : float, optional, default: None
                In cases where we do not have an interface and we wish supply a position
                where the cumulative probability is ggoing to be calculated at.
        tol : float, optional, default: 0.005
                The tolerance value which will be used as the criteria for the convergence test main loop. It compares the relevant values between two consecutive iterations and demands that the difference between them won't exceeed the tolerance value.
        path_to_save : string, optional, default:None
                The absolute path to save the figure obtained from the calculation
        Returns
        -------
        dt : float
                The converged size of the time step.
        Nt : int
                The converged number of the time steps that were being made through the simulation.
        Total_Energy : list, [[],[],[],[np.array]]
                 The first cell is the totoal magnitude at the end of the simulation, the second cell hold the first energy value
                 at the beginning of the simulation, and the third cell holds the size of the time_step = dt at each iteration.
                 The last cell hold the array with all the calculated energies along the convergence test.
        Kinetic_Energy : list, [[],[],[],[np.array]]
                The same data structure as the Total_Energy.
        Potential_Energy : list, [[],[],[],[np.array]]
                The same data structure as the Total_Energy.
        prob_current : list, [[],[],[],[np.array]]
                The same data structure as the Total_Energy.
        Cumulative_Prob : list, [[],[],[],[np.array]]
                The same data structure as the Total_Energy.
        '''

        #%% input verification
        if Nt is None:
            Nt = self.Nt
        if dt is None:
            dt = self.dt
        dt = cons.fs2sec(dt)
        if time_sim is None:
            time_sim = Nt*dt
        else:
            time_sim = self.cons.fs2sec(time_sim)
            Nt = np.int64(time_sim/dt)
        if not (z_in is None or v_in is None):
            z = z_in
            v = v_in
        else:
            z = self.cons.A2m(self.current_locpot_vec[:,0])
            v = self.cons.eV2J(self.current_locpot_vec[:,1])

        if psi is None:
            if self.psi0 is None:
                self.initialize_psi0()
            psi = self.psi0
        assert len(psi) == len(v)
        z = self.cons.A2m(z)
        v = self.cons.eV2J(v)
        psi = force_psi_units(psi, units='Meter')
        psi = to_1D_vec(psi)
        # Check whetehr our system contains an interface.
        if self.Has_interface:
            if not self.new_interface is None:
                interface_pos = self.new_interface
            else:
                interface_pos = self.original_interface
            interface_pos = self.cons.A2m(interface_pos)
        else:
            if check_pos is None:
                check_pos = len(z)-1
            check_pos = self.cons.A2m(check_pos)
            interface_pos = check_pos
        z_ind, interface_pos = find_closest_value_in_array(interface_pos, z)
        interface_pos = cons.A2m(interface_pos)
        z_axis = z == interface_pos
        # ---------------------------------------------------------

        # Creating K grid
        kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
        kk = to_1D_vec(kk)
        iteration = 0
        # A data structure that holds the wave-function vector of the last step and of the current step.
        Wave_function = np.zeros((2, len(psi)),dtype=complex)




        # %% A function to help integrating thourgh the convergence
        def integrate_trapz(vector, df):
            vector = np.asarray(vector,dtype=complex)
            df = np.float64(df)
            return np.real(np.float64(np.trapz(to_1D_vec(vector),dx = df)))


        #%%  A data structure holds calculations being made at each iteration - Energy_<> Vs dt - the time steps.
        # First cell is the Totoal magnitude at the end of the simulation, the second cell hold the first energy value
        # at the beginning of the simulation, and the third cell holds the size of the time_step = dt at each iteration.
        # The last cell hold the list with all the calculated energies along the convergence test.
        temp_dt = dt/self.alpha
        temp_Nt = np.int64(time_sim/temp_dt)
        Nt = np.int64(Nt)
        Kinetic_Energy = [[[],np.zeros((Nt,1),dtype=complex)],[[],np.zeros((temp_Nt,1),dtype=complex)]]
        Potential_Energy = [[[],np.zeros((Nt,1),dtype=complex)],[[],np.zeros((temp_Nt,1),dtype=complex)]]
        Total_Energy = [[[],np.zeros((Nt,1),dtype=complex)],[[],np.zeros((temp_Nt,1),dtype=complex)]]
        Kinetic_Energy_temp, Potential_Energy_temp,  Total_Energy_temp = [], [], []

        # %% A data structure holds calculations being made at each iteration - Probabilty current Vs dt - the time steps. The
        # equivalent values regarding the above data structures.
        prob_current = [[[],np.zeros((Nt,1),dtype=complex)],[[],np.zeros((temp_Nt,1),dtype=complex)]]
        Cumulative_Prob = [[[], np.zeros((Nt,1),dtype=complex)],[[],np.zeros((temp_Nt,1),dtype=complex)]]
        prob_current_temp, Cumulative_Prob_temp = [],[]
        temp_psi = psi

        # %% First and second iterations before entering the loop:

        # iteration = 0:
        iteration = 0
        prob_current[0][0] = dt
        Total_Energy[0][0] = dt
        Cumulative_Prob[0][0] = dt
        Kinetic_Energy[0][0] = dt
        Potential_Energy[0][0] = dt
        # iteration = 1:
        prob_current[1][0] = dt/self.alpha
        Total_Energy[1][0] = dt/self.alpha
        Cumulative_Prob[1][0] = dt/self.alpha
        Kinetic_Energy[1][0] = dt/self.alpha
        Potential_Energy[1][0] = dt/self.alpha

        # The first two iterations we are being performed outside the main 'while' loop since the 'while condition' takes into account
        # the last two iterations.

        # A varibale that helps to correct the overall time simulation at the first
        # two iterations.
        temp_count = [Nt, temp_Nt]

        #%% Printing during the first two iterations.
        print('Stage_2 converge Time step')
        print('..............................')
        for j in range(2):
            for i in range(np.int64(temp_count[j])):
                # if this is the first appearance of the loop, propagate the initial wave-function.
                if i == 0:
                    Wave_function[0, :] = psi
                    prob_current_temp = np.squeeze(calculate_probability_current(Wave_function[0, :],kk)[z_axis])
                    Cumulative_Prob_temp = cumulative_probabilty(Wave_function[0, :], z, interface_pos, np.diff(z)[0])
                    Total_Energy_temp, Kinetic_Energy_temp, Potential_Energy_temp  = self.calculate_E0(Wave_function[0, :],
                                                                                                      z_in=z, v_in=v)
                    prob_current[iteration][1][i] = prob_current_temp
                    Cumulative_Prob[iteration][1][i] = Cumulative_Prob_temp
                    Kinetic_Energy[iteration][1][i] = Kinetic_Energy_temp
                    Total_Energy[iteration][1][i] = Total_Energy_temp
                    Potential_Energy[iteration][1][i] = Potential_Energy_temp

                    Wave_function[1, :] = run_one_time_step(Wave_function[0, :], dt, v, z, kk)
                # Except for the first step of the loop, propagate one-step the current wave-function stored at the temp_psi.
                else:
                    Wave_function[0, :] = Wave_function[1, :]
                    prob_current_temp = np.squeeze(calculate_probability_current(Wave_function[0, :],kk)[z_axis])
                    Cumulative_Prob_temp = cumulative_probabilty(Wave_function[0, :], z, interface_pos, np.diff(z)[0])
                    Total_Energy_temp, Kinetic_Energy_temp, Potential_Energy_temp = self.calculate_E0(Wave_function[0, :],
                                                                                                      z_in=z, v_in=v)
                    prob_current[iteration][1][i] = prob_current_temp
                    Cumulative_Prob[iteration][1][i] = Cumulative_Prob_temp
                    Kinetic_Energy[iteration][1][i] = Kinetic_Energy_temp
                    Total_Energy[iteration][1][i] = Total_Energy_temp
                    Potential_Energy[iteration][1][i] = Potential_Energy_temp
                    Wave_function[1, :] = run_one_time_step(Wave_function[0, :], dt, v, z, kk)

            print("Iteration Number {}".format(iteration))
            print('dt = {:.4e} fsec'.format(self.cons.sec2fs(dt)))
            print("The difference in Total Energy between the final propagation step and the first propagation step is = {:.3f} eV".format(cons.J2eV(np.abs(Total_Energy[iteration][1][-1] - Total_Energy[iteration][1][4]))))
            if iteration == 0:
                print(r'First Value for probabilty current  = {:.4e} e/A'.format(integrate_trapz(prob_current[iteration][1],prob_current[iteration][0])))
            elif iteration == 1:
                print("Probabilty current difference between the last two iterations = {:.4e}".format(
                    np.abs(integrate_trapz(prob_current[iteration][1],prob_current[iteration][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]))))
            # ax_0.plot(np.arange(0,Total_Energy[iteration][0]*len(Total_Energy[iteration][1]),Total_Energy[iteration][0]),
            #           cons.J2eV(Total_Energy[iteration][1]), '--', linewidth=2,label=r'iteration number {}'.format(iteration))
            # ax_0_1.plot(prob_current[iteration][0]*np.arange(0,len(prob_current[iteration][1]),1),
            #           prob_current[iteration][1], '--', linewidth=2,label=r'iteration number {}'.format(iteration))
            # plt.legend()
            # plt.show()
            print("-----------------------------------------------------------------------------")

            # %% Setting last the dynamic variables after the first two iterations before enetering the main loop,
            former_dt = dt
            dt = dt  / self.alpha
            former_Nt = Nt
            Nt = np.int64(time_sim / dt)
            Wave_function = np.zeros((2, len(psi)),dtype=complex)
            temp_psi = psi
            iteration = 1
            if np.abs(integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]) - integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0])) <= tol and np.abs(Total_Energy[iteration-1][1][-1] - Total_Energy[iteration-1][1][4]) <= self.cons.eV2J(tol):
                print(r'Probability current got converged. Its difference between the last two iterations = {:.4e} e/A'.format(np.abs(integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]))))
                print("=======================================================================")
                print('Total energy conserved. Its difference between the final propagation step and the first propagation step is = {:.4e} eV'.format(
                    np.abs(cons.J2eV(np.abs(Total_Energy[iteration-1][1][-1] - Total_Energy[iteration-1][1][4])))))
                print('Final dt is {:.4e} fsec'.format(self.cons.sec2fs(dt)))
                print("=======================================================================")
                if self.To_plot:
                    font = {'family': 'serif', 'size': 15}
                    plt.rc('font', **font)
                    gs = GridSpec(1, 1)
                    fig = plt.figure(figsize=(16, 11))
                    fig.suptitle(r'Cumulative Probabilty Through the interface')
                    ax = plt.subplot(gs[0])
                    ax.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Cumulative_Prob])),
                            np.array([np.real(i[1][-1]) for i in Cumulative_Prob]), 'o', linewidth=2,
                            label=r'Cumulative Probabilty')
                    ax.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Cumulative_Prob])),
                            np.array([np.real(i[1][-1]) for i in Cumulative_Prob]), '--', linewidth=2)
                    ax.grid()
                    ax.set_xlabel(r'dt, [$fsec$]', fontsize=14)
                    ax.set_ylabel(r'Cumulative Probabilty', fontsize=14)
                    ax.legend(fancybox=True, shadow=False, prop={'size': 14})
                    ax.ticklabel_format(useOffset=False, useMathText=True, style='sci')
                    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                    if path_to_save is None:
                        plt.savefig('Cumulative probabilty vs dt' + ".svg", format="svg",dpi=300)
                    else:
                        plt.savefig("_".join(
                            list(
                                os.path.join(path_to_save, 'Cumulative probabilty vs dt').split(
                                "\\")))+ ".svg",
                                    format="svg", dpi=300)

                    font = {'family': 'serif', 'size': 15}
                    plt.rc('font', **font)
                    gs = GridSpec(1, 1)
                    fig = plt.figure(figsize=(16, 11))
                    fig.suptitle(r'Probabilty current through the interface')
                    ax_1 = plt.subplot(gs[0])

                    ax_1.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in prob_current])),
                              np.array([np.real(integrate_trapz(i[1], i[0])) for i in prob_current]), 'o', linewidth=2,
                              label=r'Probabilty current $\frac{e}{\AA}$')
                    ax_1.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in prob_current])),
                              np.array([np.real(integrate_trapz(i[1], i[0])) for i in prob_current]), '--', linewidth=2)
                    ax_1.grid()
                    ax_1.set_xlabel(r'dt, [$fsec$]', fontsize=14)
                    ax_1.set_ylabel(r'Probabilty current, $\frac{e}{\AA}$', fontsize=14)
                    ax_1.legend(fancybox=True, shadow=False, prop={'size': 14})
                    # ax_1.ticklabel_format(useOffset=True, useMathText=True, style='sci')
                    # ax_1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
                    if path_to_save is None:
                        plt.savefig('Probabilty current vs dt' + ".svg", format="svg",dpi=300)
                    else:
                        plt.savefig("_".join(
                            list(
                                os.path.join(path_to_save, 'Probabilty current vs dt').split(
                                "\\"))) + ".svg",
                                    format="svg", dpi=300)

                    font = {'family': 'serif', 'size': 15}
                    plt.rc('font', **font)
                    gs = GridSpec(1, 1)
                    fig = plt.figure(figsize=(16, 11))
                    fig.suptitle(r'Probabilty current at the interface Vs time')
                    ax_2 = plt.subplot(gs[0])

                    # ax_2.ticklabel_format(useOffset=True, useMathText=True, style='sci')
                    # ax_2.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                    ax_2.plot(np.array(self.cons.sec2fs(prob_current[-1][0] * np.arange(0, former_Nt))),
                              np.array(prob_current[-1][1]), linewidth=2,
                              label=r'Probabilty current $J_{{z=z_{{interface}}}}$, Transmission coefficient is : {:.3f} $\frac{{e}}{{\AA}}$'.format(
                                  integrate_trapz(np.array(prob_current[-1][1]), prob_current[-1][0])))
                    # ax_2.plot(np.array(self.cons.sec2fs(prob_current[-1][0] * np.arange(0,Nt))), np.array(prob_current[-1][1]), '--',linewidth=2)
                    ax_2.grid()
                    ax_2.set_xlabel(r'Time of simulation, [$fsec$]', fontsize=14)
                    ax_2.set_ylabel(r'Probabilty current, $J_{z=z_{interface}}$  $\frac{e}{\AA}$', fontsize=14)
                    ax_2.legend(fancybox=True, shadow=False, prop={'size': 14})
                    if path_to_save is None:
                        plt.savefig('Probabilty current vs Time of simulation' + ".svg", format="svg",dpi=300)
                    else:
                        plt.savefig("_".join(
                            list(
                                os.path.join(path_to_save, 'Probabilty current vs Time of simulation').split(
                                "\\"))) + ".svg",
                                    format="svg", dpi=300)

                    plt.rc('font', **font)
                    gs = GridSpec(3, 1)
                    fig = plt.figure(figsize=(16, 11))
                    fig.suptitle(r'Convergence plots Vs dt , time-steps')
                    Ax_i = []
                    for i in range(0, 3, 1):
                        Ax_i.append(plt.subplot(gs[i]))

                    Ax_i[2].set_xlabel(r" dt, time step in fsec")
                    Ax_i[0].set_ylabel(r"$Total  Energy_{final-initial}$,  $E_{tot}$ [eV]", fontsize=9)
                    Ax_i[1].set_ylabel(r"$Kinetic  energy_{final-initial}$,  $T_{kin}$ [eV]", fontsize=9)
                    Ax_i[2].set_ylabel(r"$Potential  energy_{final-initial}$,  $V_{pot}$ [eV]", fontsize=9)

                    # Ax_i[0].ticklabel_format(useOffset=True, useMathText=True, style='sci')
                    # Ax_i[0].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                    Ax_i[0].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Total_Energy])), self.cons.J2eV(
                        np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Total_Energy])), 'o', color='blue',
                                 label='Total Energy')
                    Ax_i[0].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Total_Energy])),
                                 self.cons.J2eV(
                                     np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Total_Energy])), '--',
                                 color='blue')

                    # Ax_i[1].ticklabel_format(useOffset=True, useMathText=True, style='sci')
                    # Ax_i[1].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                    Ax_i[1].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Kinetic_Energy])), self.cons.J2eV(
                        np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Kinetic_Energy])), 'o', color='red',
                                 label='Kinetic Energy')
                    Ax_i[1].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Kinetic_Energy])),
                                 self.cons.J2eV(
                                     np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Kinetic_Energy])), '--',
                                 color='red')

                    # Ax_i[2].ticklabel_format(useOffset=True, useMathText=True, style='sci')
                    # Ax_i[2].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                    Ax_i[2].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Potential_Energy])), self.cons.J2eV(
                        np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Potential_Energy])), 'o',
                                 color='green',
                                 label='Potential Energy')
                    Ax_i[2].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Potential_Energy])),
                                 self.cons.J2eV(
                                     np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Potential_Energy])),
                                 '--', color='green')

                    for i in range(0, 3, 1):
                        Ax_i[i].grid()
                        Ax_i[i].legend(fancybox=True, shadow=False, prop={'size': 14})
                    plt.show()
                    if path_to_save is None:
                        plt.savefig('Convergence test energies vs time' + ".svg", format="svg",dpi=300)
                    else:
                        plt.savefig("_".join(
                            list(
                                os.path.join(path_to_save,'Convergence test energies vs time' ).split(
                                "\\"))) + ".svg",
                                    format="svg", dpi=300)


                if To_update:
                    self.dt = dt
                    self.Nt = Nt
                return dt, Nt, Total_Energy, Kinetic_Energy, Potential_Energy, prob_current, Cumulative_Prob


        #%%  Entering the main 'while' loop with iteration equals to 2.
        iteration = 2

        while iteration < iterations and (not(np.abs(integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]) - integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0])) <= tol and np.abs(Total_Energy[iteration-1][1][-1] - Total_Energy[iteration-1][1][4]) <= self.cons.eV2J(tol))) :
            # Before we propagating the wave function, we would like to save the magnitude of dt in the current iteration.

            if iteration == 1:
                prob_current[1][0] = dt
                Total_Energy[1][0] = dt
                Cumulative_Prob[1][0] = dt
                Kinetic_Energy[1][0] = dt
                Potential_Energy[1][0] = dt
            else:
                prob_current.append([dt, np.zeros((Nt,1),dtype=complex)])
                Total_Energy.append([dt, np.zeros((Nt,1),dtype=complex)])
                Cumulative_Prob.append([dt, np.zeros((Nt,1),dtype=complex)])
                Kinetic_Energy.append([dt, np.zeros((Nt,1),dtype=complex)])
                Potential_Energy.append([dt, np.zeros((Nt,1),dtype=complex)])

            # For each time-step size, we propagate the wave-function Nt times. We want to check whether the energy and the transmision coeffient are getting converged
            # for increasin the dt magnitude.
            for i in range(Nt):
                # if this is the first appearance of the loop, propagate the initial wave-function.
                if i == 0:
                    Wave_function[0, :] = psi
                    prob_current_temp = np.squeeze(calculate_probability_current(Wave_function[0, :],kk)[z_axis])
                    Cumulative_Prob_temp = cumulative_probabilty(Wave_function[0, :], z, interface_pos, np.diff(z)[0])
                    Total_Energy_temp, Kinetic_Energy_temp, Potential_Energy_temp = self.calculate_E0(Wave_function[0, :],z_in=z,v_in=v)

                    prob_current[iteration][1][i] = prob_current_temp
                    Cumulative_Prob[iteration][1][i] = Cumulative_Prob_temp
                    Kinetic_Energy[iteration][1][i] = Kinetic_Energy_temp
                    Total_Energy[iteration][1][i] = Total_Energy_temp
                    Potential_Energy[iteration][1][i] = Potential_Energy_temp

                    Wave_function[1, :] = run_one_time_step(Wave_function[0, :],dt , v, z , kk)

                # Except for the first step of the loop, propagate one-step the current wave-function stored at the temp_psi.
                else:
                    Wave_function[0, :] =  Wave_function[1, :]
                    prob_current_temp = np.squeeze(calculate_probability_current(Wave_function[0, :],kk)[z_axis])
                    Cumulative_Prob_temp = cumulative_probabilty(Wave_function[0, :], z, interface_pos, np.diff(z)[0])
                    Total_Energy_temp, Kinetic_Energy_temp, Potential_Energy_temp = self.calculate_E0(Wave_function[0, :],z_in=z,v_in=v)

                    prob_current[iteration][1][i] = prob_current_temp
                    Cumulative_Prob[iteration][1][i] = Cumulative_Prob_temp
                    Kinetic_Energy[iteration][1][i] = Kinetic_Energy_temp
                    Total_Energy[iteration][1][i] = Total_Energy_temp
                    Potential_Energy[iteration][1][i] = Potential_Energy_temp

                    Wave_function[1, :] = run_one_time_step(Wave_function[0, :], dt, v, z, kk)

            # Before we decreasing dt for the next iteration, we should check whether the next loop will be performed.
            print("Iteration Number {}".format(iteration))
            print('dt = {:.4e} fsec'.format(self.cons.sec2fs(dt)))
            print("The difference in Total Energy between the final propagation step and the first propagation step is = {:.4e} eV".format(cons.J2eV(np.abs(Total_Energy[iteration][1][-1] - Total_Energy[iteration][1][4]))))
            print(r'Probabilty current difference between the last two iterations = {:.4e} e/A'.format(np.abs(integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]))))
            print("-----------------------------------------------------------------------------")

            if   iteration < iterations and (not(np.abs(integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0])) <= tol and np.abs(Total_Energy[iteration-1][1][-1] - Total_Energy[iteration-1][1][4]) <= self.cons.eV2J(tol))) :
                dt = dt  / self.alpha
                Nt = np.int64(time_sim / dt)
                Wave_function = np.zeros((2, len(psi)),dtype=complex)
                temp_psi = psi
                iteration +=1
        dt = dt  * self.alpha
        Nt = np.int64(time_sim / dt)
        if not iteration  < iterations:
            print('Got over {} interations'.format(iteration))
            print("=======================================================================")
        elif not np.abs((integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]))) > tol:
            print(r'Probability current got converged. Its difference between the last two iterations = {:.4e} e/A'.format(np.abs(integrate_trapz(prob_current[iteration-2][1],prob_current[iteration-2][0]) - integrate_trapz(prob_current[iteration-1][1],prob_current[iteration-1][0]))))
            print("=======================================================================")
            print('Total energy conserved. Its difference between the final propagation step and the first propagation step is = {:.4e} eV'.format(
                np.abs(cons.J2eV(np.abs(Total_Energy[iteration-1][1][-1] - Total_Energy[iteration-1][1][4])))))
            print('Final dt is {:.4e} fsec'.format(self.cons.sec2fs(dt)))
            print("=======================================================================")
        # If we enabled the plotting option for this class instance, namely : self.To_plot = True
        if self.To_plot:
            font = {'family': 'serif', 'size': 15}
            plt.rc('font', **font)
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Cumulative Probabilty Through the interface')
            ax = plt.subplot(gs[0])
            ax.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Cumulative_Prob])),np.array([np.real(i[1][-1]) for i in Cumulative_Prob]),'o', linewidth=2,
                    label=r'Cumulative Probabilty')
            ax.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Cumulative_Prob])),np.array([np.real(i[1][-1]) for i in Cumulative_Prob]),'--', linewidth=2)
            ax.grid()
            ax.set_xlabel(r'dt, [$fsec$]', fontsize=14)
            ax.set_ylabel(r'Cumulative Probabilty', fontsize=14)
            ax.legend(fancybox=True, shadow=False, prop={'size': 14})
            ax.ticklabel_format(useOffset=False, useMathText=True, style='sci')
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            if path_to_save is None:
                plt.savefig('Cumulative probabilty vs dt' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("_".join(
                    list(
                        os.path.join(path_to_save, 'Cumulative probabilty vs dt').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)


            font = {'family': 'serif', 'size': 15}
            plt.rc('font', **font)
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Probabilty current through the interface')
            ax_1 = plt.subplot(gs[0])

            ax_1.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in prob_current])) ,np.array([np.real(integrate_trapz(i[1],i[0])) for i in prob_current]),'o', linewidth=2, label=r'Probabilty current $\frac{e}{\AA}$')
            ax_1.plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in prob_current])),
                      np.array([np.real(integrate_trapz(i[1],i[0])) for i in prob_current]), '--', linewidth=2)
            ax_1.grid()
            ax_1.set_xlabel(r'dt, [$fsec$]', fontsize=14)
            ax_1.set_ylabel(r'Probabilty current, $\frac{e}{\AA}$', fontsize=14)
            ax_1.legend(fancybox=True, shadow=False, prop={'size': 14})
           # ax_1.ticklabel_format(useOffset=True, useMathText=True, style='sci')
           # ax_1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
            if path_to_save is None:
                plt.savefig('Probabilty current vs dt' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("_".join(
                    list(
                        os.path.join(path_to_save, 'Probabilty current vs dt').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)


            font = {'family': 'serif', 'size': 15}
            plt.rc('font', **font)
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Probabilty current at the interface Vs time')
            ax_2 = plt.subplot(gs[0])

            #ax_2.ticklabel_format(useOffset=True, useMathText=True, style='sci')
            #ax_2.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            ax_2.plot( np.array(self.cons.sec2fs(prob_current[-1][0]*np.arange(0,Nt))) ,np.array(prob_current[-1][1]), linewidth=2, label=r'Probabilty current $J_{{z=z_{{interface}}}}$, Transmission coefficient is : {:.3f} $\frac{{e}}{{\AA}}$'.format(integrate_trapz(np.array(prob_current[-1][1]),prob_current[-1][0])))
            #ax_2.plot(np.array(self.cons.sec2fs(prob_current[-1][0] * np.arange(0,Nt))), np.array(prob_current[-1][1]), '--',linewidth=2)
            ax_2.grid()
            ax_2.set_xlabel(r'Time of simulation, [$fsec$]', fontsize=14)
            ax_2.set_ylabel(r'Probabilty current, $J_{z=z_{interface}}$  $\frac{e}{\AA}$', fontsize=14)
            ax_2.legend(fancybox=True, shadow=False, prop={'size': 14})
            if path_to_save is None:
                plt.savefig('Probabilty current vs Time of simulation' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("_".join(
                    list(
                        os.path.join(path_to_save, 'Probabilty current vs Time of simulation').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)


            plt.rc('font', **font)
            gs = GridSpec(3, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Convergence plots Vs dt , time-steps')
            Ax_i = []
            for i in range(0, 3, 1):
                Ax_i.append(plt.subplot(gs[i]))

            Ax_i[2].set_xlabel(r" dt, time step in fsec")
            Ax_i[0].set_ylabel(r"$Total  Energy_{final-initial}$,  $E_{tot}$ [eV]", fontsize=9)
            Ax_i[1].set_ylabel(r"$Kinetic  energy_{final-initial}$,  $T_{kin}$ [eV]", fontsize=9)
            Ax_i[2].set_ylabel(r"$Potential  energy_{final-initial}$,  $V_{pot}$ [eV]", fontsize=9)

            #Ax_i[0].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            #Ax_i[0].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            Ax_i[0].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Total_Energy])),self.cons.J2eV(np.array([(np.real(i[1][-1])-np.real(i[1][0])) for i in Total_Energy])),'o', color='blue', label='Total Energy')
            Ax_i[0].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Total_Energy])),
                         self.cons.J2eV(np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Total_Energy])),'--', color='blue')


            #Ax_i[1].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            #Ax_i[1].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            Ax_i[1].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Kinetic_Energy])),self.cons.J2eV(np.array([(np.real(i[1][-1])-np.real(i[1][0])) for i in Kinetic_Energy])),'o', color='red', label='Kinetic Energy')
            Ax_i[1].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Kinetic_Energy])),
                         self.cons.J2eV(np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Kinetic_Energy])),'--', color='red')


            #Ax_i[2].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            #Ax_i[2].yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
            Ax_i[2].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Potential_Energy])),self.cons.J2eV(np.array([(np.real(i[1][-1])-np.real(i[1][0])) for i in Potential_Energy])),'o', color='green',
                         label='Potential Energy')
            Ax_i[2].plot(self.cons.sec2fs(np.array([np.real(i[0]) for i in Potential_Energy])),
                         self.cons.J2eV(np.array([(np.real(i[1][-1]) - np.real(i[1][0])) for i in Potential_Energy])), '--',color='green')


            for i in range(0, 3, 1):
                Ax_i[i].grid()
                Ax_i[i].legend(fancybox=True, shadow=False, prop={'size': 14})
            plt.show()
            if path_to_save is None:
                plt.savefig('Convergence test energies vs time' + ".svg", format="svg", dpi=300)
            else:
                plt.savefig("_".join(
                    list(
                        os.path.join(path_to_save, 'Convergence test energies vs time').split(
                        "\\"))) + ".svg",
                            format="svg", dpi=300)

        if To_update:
            self.dt = dt
            self.Nt = Nt
        print("--------------------------------")
        print("--------------------------------")
        print('Final dt = {:.5e} sec'.format(cons.fs2sec(self.dt)))
        print('Final k0 = {:.5e} 1/Ang'.format(self.psi0_dic['k0']))
        print('Final sigma = {:.5g} Ang'.format(cons.m2A(self.psi0_dic['sigma'])))
        print('E0  = {:.5g} eV'.format(cons.J2eV(self.psi0_dic['E0'])))
        print('N = {:.5g} partitions'.format((self.psi0_dic['N'])))
        print('Nt = {:.5g} time steps'.format(self.Nt))
        print("--------------------------------")
        print("--------------------------------")
        return dt, Nt, Total_Energy, Kinetic_Energy,Potential_Energy,prob_current, Cumulative_Prob


    def model_interface(self, interface_initial_pos, interface_final_pos,region_initial_pos,region_final_pos,Delta_pos, z_in = None, v_in = None,interface_pos=None,path_to_save = None):
        '''

        Parameters
        ----------
        interface_initial_pos :
        interface_final_pos :
        region_initial_pos :
        region_final_pos :
        Delta_pos :
        z_in :
        v_in :
        interface_pos :
        path_to_save :

        Returns
        -------

        '''
        interface_initial_pos = cons.m2A( interface_initial_pos)
        interface_final_pos = cons.m2A(interface_final_pos)
        interface_pos = cons.m2A( interface_pos)
        region_initial_pos = cons.m2A(region_initial_pos)
        region_final_pos = cons.m2A(region_final_pos)
        Delta_pos = cons.m2A(Delta_pos)

        if z_in is None or v_in is None:
            z, v = self.current_locpot_vec.T
        else:
            z,v = z_in, v_in
        z = cons.m2A( z)
        v = cons.J2eV(v)
        ind_interface_initial_pos, interface_initial_pos = find_closest_value_in_array(interface_initial_pos,z)
        ind_interface_final_pos, interface_final_pos = find_closest_value_in_array(interface_final_pos, z)
        new_z_interface = np.array(z[(interface_initial_pos <= z) & (z <= interface_final_pos)])
        new_v_interface = np.array(v[(interface_initial_pos <= z) & (z <= interface_final_pos)])
        ind_region_initial_pos, region_initial_pos = find_closest_value_in_array(region_initial_pos,z)
        ind_region_final_pos, region_final_pos = find_closest_value_in_array(region_final_pos, z)
        new_z_region = np.array(z[(region_initial_pos <= z) & (z <= region_final_pos)])
        new_v_region = np.array(v[(region_initial_pos <= z) & (z <= region_final_pos)])

        ind_Delta, Delta_pos = find_closest_value_in_array(Delta_pos, z)
        # ind_sigma, sigma_pos = find_closest_value_in_array(sigma_pos, z)
        sigma_pos = interface_final_pos
        ind_phi,phi_pos = find_closest_value_in_array(np.max(np.array(v[(region_initial_pos <= z) & (z <= region_final_pos)])), v)
        phi_pos = z[ind_phi]
        phi_height = np.float(v[ind_phi])
        Delta_height = np.float(v[ind_Delta])

        z_left_region = np.array(new_z_region[ (new_z_region <= new_z_interface[0]) ])
        v_left_region = np.array(new_v_region[ (new_z_region <= new_z_interface[0]) ])
        z_right_region = np.array(new_z_region[ (new_z_region >= new_z_interface[-1])])
        v_right_region = np.array(new_v_region[ (new_z_region >= new_z_interface[-1])])

        left_region_maxima = find_peaks_maxima(z_left_region,v_left_region,ignore_local_maxima=True)
        left_region_average_maxima_height = np.average(cons.J2eV(left_region_maxima[:,1][-2::]))
        right_region_maxima = find_peaks_maxima(z_right_region,v_right_region,ignore_local_maxima=True)
        right_region_average_maxima_height = np.average(cons.J2eV(right_region_maxima[:,1][0:2]))

        left_region_minima = find_peaks_minima(z_left_region,v_left_region,ignore_local_minima=True)
        left_region_average_minima_height = np.average(cons.J2eV(left_region_minima[:,1][-2::]))
        right_region_minima = find_peaks_minima(z_right_region,v_right_region,ignore_local_minima=True)
        right_region_average_minima_height = np.average(cons.J2eV(right_region_minima[:,1][0:2]))


        first_two_maxima_from_left =  left_region_maxima[-2::]
        first_two_maxima_from_right = right_region_maxima[0:2]
        first_two_minima_from_left =  left_region_minima[-2::]
        first_two_minima_from_right = right_region_minima[0:3]



        if phi_height < left_region_average_maxima_height:
            highest_height = left_region_average_maxima_height
        else:
            highest_height =phi_height
        E0 = cons.J2eV(self.psi0_dic['E0'])
        phi_value = np.abs(E0 - highest_height)
        E4 = np.abs(phi_height -  left_region_average_maxima_height)
        E3 = np.abs(left_region_average_maxima_height - left_region_average_minima_height)
        Delta_value = np.abs(Delta_height - left_region_average_minima_height )
        #sigma_width = np.abs(Delta_pos - sigma_pos)
        sigma_width = np.abs(interface_initial_pos - sigma_pos)
        sigma_height  =  np.float(v[ind_interface_final_pos])
        E1 = np.abs(highest_height -  right_region_average_maxima_height)
        E2 = np.abs(right_region_average_maxima_height - right_region_average_minima_height)
        E0 = np.max(new_v_region) + 0.5
        fig, ax = plt.subplots(1, 1, figsize=(14, 14), sharex=True)
        ax.grid(True)
        ax.plot(new_z_region,new_v_region,'black')
        plt.rcParams['font.size'] = 16

        #E3
        if first_two_minima_from_left[:,0][0] <  first_two_maxima_from_left[:,0][0]:
            left_side_left = first_two_minima_from_left[:,0][0]
            left_side_right = first_two_maxima_from_left[:,0][0]
        else:
            left_side_left = first_two_maxima_from_left[:,0][0]
            left_side_right = first_two_minima_from_left[:,0][0]
        if first_two_minima_from_right[:,0][1] <  first_two_maxima_from_right[:,0][1]:
            right_side_left = first_two_minima_from_right[:,0][1]
            right_side_right = first_two_maxima_from_right[:,0][1]
        else:
            right_side_left = first_two_maxima_from_right[:,0][1]
            right_side_right = first_two_minima_from_right[:,0][1]
        try:
            d_space_right = np.abs(first_two_minima_from_right[:,0][1]-first_two_minima_from_right[:,0][0])
        except IndexError:
            d_space_right = 0
        try:
            d_space_left = np.abs(first_two_minima_from_left[:,0][1]-first_two_minima_from_left[:,0][0])
        except IndexError:
            d_space_left = 0
        ax.hlines(left_region_average_minima_height,first_two_minima_from_left[:,0][0],Delta_pos,color='g', linestyles = 'dashdot',alpha=0.7,lw=1,zorder=0)
        # E4
        #ax.hlines(left_region_average_maxima_height, left_side_left-0.3,  left_side_right+0.3 , linestyles='dashdot',color='g',lw=1,alpha=0.7,zorder=0)
        # phi
        ax.hlines(highest_height, left_side_left, right_side_right, linestyles='dashdot',color='g',lw=1,alpha=0.7,zorder=0)
        if phi_height < highest_height:
            ax.hlines(phi_height, left_side_left, right_side_right, linestyles='dashdot',color='g',lw=1, alpha=0.7,
                      zorder=0)
        #E1
        ax.hlines(right_region_average_maxima_height, right_side_left-0.3, right_side_right+0.3, linestyles='dashdot',lw=0.8,alpha=0.7,zorder=0)
        #E2
        ax.hlines(right_region_average_minima_height, right_side_left-0.3, right_side_right+0.3, linestyles='dashdot',color='g',lw=1,alpha=0.7,zorder=0)
        #intertface
        ax.axvline(interface_pos, color='darkblue',lw=3,alpha=0.7,zorder=0)
        #regions separation
        ax.axvline(x=interface_initial_pos, color='b',lw=1.5,alpha=0.7,zorder=0)
        ax.axvline(x= interface_final_pos, color='b', lw=1.5, alpha=0.7, zorder=0)
        #delta
        ax.vlines(Delta_pos, sigma_height, Delta_height,linestyles=  'dashdot',color='g',lw=1,alpha=0.7,zorder=0)


        ax.axhline(E0, lw=2,alpha=0.7,color='aqua',zorder=0)

        ax.annotate('',
                    xy=(Delta_pos, left_region_average_minima_height), xycoords='data',
                    xytext=(Delta_pos, Delta_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=0.7,alpha=0.7,zorder=0),
                    )

        ax.annotate(u'Δ',
                    xy=(Delta_pos-0.3, ((left_region_average_minima_height+Delta_height)/2)-0.1), xycoords='data',
                    xytext=(Delta_pos-0.3,((left_region_average_minima_height+Delta_height)/2)-0.1), textcoords='data',
                    )

        ax.annotate('',
                    xy=(first_two_minima_from_left[:,0][0], left_region_average_minima_height), xycoords='data',
                    xytext=(first_two_minima_from_left[:,0][0], left_region_average_maxima_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2,alpha=0.7,zorder=0),
                    )
        ax.annotate(r'$E_3$',
                    xy=(first_two_minima_from_left[:,0][0]-0.3, (left_region_average_minima_height+left_region_average_maxima_height)/2), xycoords='data',
                    xytext=(first_two_minima_from_left[:,0][0]-0.3, (left_region_average_minima_height+left_region_average_maxima_height)/2), textcoords='data',
                    )

        ax.annotate('',
                    xy=(first_two_minima_from_left[:,0][0]+0.1,left_region_average_maxima_height), xycoords='data',
                    xytext=(first_two_minima_from_left[:,0][0]+0.1, phi_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2,alpha=0.7,zorder=0),
                    )
        ax.annotate(r'$E_4$',
                    xy=(first_two_minima_from_left[:,0][0]+0.2,-np.abs(left_region_average_maxima_height+phi_height)/2), xycoords='data',
                    xytext=(first_two_minima_from_left[:,0][0]+0.2, -np.abs(left_region_average_maxima_height+phi_height)/2), textcoords='data',
                    )
        ax.annotate('',
                    xy=(phi_pos+0.1, highest_height), xycoords='data',
                    xytext=(phi_pos+0.1, E0), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2,alpha=0.7,zorder=0),
                    )
        ax.annotate(r'$\Phi$',
                    xy=(phi_pos+0.18, (E0+highest_height)/2), xycoords='data',
                    xytext=(phi_pos+0.18,(E0+highest_height)/2), textcoords='data',
                    )

        ax.annotate("",
                    xy=(first_two_minima_from_right[:,0][1], right_region_average_minima_height), xycoords='data',
                    xytext=(first_two_minima_from_right[:,0][1], right_region_average_maxima_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2,alpha=0.7,zorder=0),
                    )
        ax.annotate(r'$E_2$',
                    xy=(first_two_minima_from_right[:,0][1]+0.07, -np.abs(right_region_average_minima_height+right_region_average_maxima_height)/2), xycoords='data',
                    xytext=(first_two_minima_from_right[:,0][1]+0.07, -np.abs(right_region_average_minima_height+right_region_average_maxima_height)/2), textcoords='data',
                    )
        ax.annotate('',
                    xy=(first_two_minima_from_right[:,0][1], right_region_average_maxima_height), xycoords='data',
                    xytext=(first_two_minima_from_right[:,0][1], highest_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=1,alpha=0.7,zorder=0),
                    )
        ax.annotate(r'$E_1$',
                    xy=(first_two_minima_from_right[:,0][1]+0.1, (highest_height+right_region_average_maxima_height)/2), xycoords='data',
                    xytext=(first_two_minima_from_right[:,0][1]+0.1, (highest_height+right_region_average_maxima_height)/2), textcoords='data',
                    )

        ax.annotate('',
                    xy=(interface_initial_pos, sigma_height), xycoords='data',
                    xytext=(sigma_pos, sigma_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2),
                    )
        ax.annotate(r'$\sigma$',
                    xy=((sigma_pos+interface_initial_pos)/2, sigma_height-0.2), xycoords='data',
                    xytext=((sigma_pos+interface_initial_pos)/2, sigma_height-0.2), textcoords='data',

                    )
        ax.annotate('',
                    xy=(first_two_minima_from_right[:,0][1],right_region_average_minima_height), xycoords='data',
                    xytext=(first_two_minima_from_right[:,0][2], right_region_average_minima_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2),
                    )
        ax.annotate(r'$\ d_{(001)} $',
                    xy=((first_two_minima_from_right[:,0][1]+first_two_minima_from_right[:,0][2])/2,  right_region_average_minima_height-0.2), xycoords='data',
                    xytext=((first_two_minima_from_right[:,0][1]+first_two_minima_from_right[:,0][2])/2,  right_region_average_minima_height-0.2), textcoords='data',

                    )
        ax.annotate('',
                    xy=(first_two_minima_from_left[:,0][0],left_region_average_minima_height), xycoords='data',
                    xytext=(first_two_minima_from_left[:,0][1], left_region_average_minima_height), textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="arc3",  color='r', lw=2),
                    )
        ax.annotate(r'$\ d_{(001)} $',
                    xy=((first_two_minima_from_left[:,0][0]+first_two_minima_from_left[:,0][1])/2,  left_region_average_minima_height-0.2), xycoords='data',
                    xytext=((first_two_minima_from_left[:,0][0]+first_two_minima_from_left[:,0][1])/2,  left_region_average_minima_height-0.2), textcoords='data',

                    )

        ax.axvspan(0,new_z_interface[0],facecolor='lightslategray', alpha=0.25)
        ax.axvspan(new_z_interface[0], new_z_interface[-1], facecolor='lightblue', alpha=0.25)
        ax.axvspan(new_z_interface[-1],z_right_region[-1], facecolor='steelblue', alpha=0.25)
        ax.set_xlabel('z axis ' +  r'$[\AA]$')
        ax.set_xlim(new_z_region[0],new_z_region[-1])
        ax.set_ylim(np.min(v)-0.6,E0+0.6)
        ax.set_ylabel('Local potential Energy, eV')
        plt.tight_layout()
        plt.subplots_adjust(left=0.133, right=0.934, bottom=0.164, top=0.961, wspace=0.085)
        if path_to_save is None:
            plt.savefig('Interface model new' + ".svg", format="svg", dpi=300)
        else:
            plt.savefig("_".join(
                list(
                    os.path.join(path_to_save, 'Interface model new').split(
                        "\\"))) + ".svg",
                        format="svg", dpi=300)
        plt.show()
        dic_to_return =  {'phi':phi_value, 'E1':E1, 'E2':E2,'E3':E3,'E4':E4,'Delta': Delta_value, 'sigma':sigma_width,  'd(001)_left':d_space_left,'d(001)_right':d_space_right,'interface_position':interface_pos}
        print('----------------------------------------------------------')
        print('phi = {:.4g} ev'.format(phi_value) )
        print('E1 = {:.4g} ev'.format(E1))
        print('E2 = {:.4g} ev'.format(E2))
        print('E3 = {:.4g} ev'.format(E3))
        print('E4 = {:.4g} ev'.format(E4))
        print('Delta = {:.4g} ev'.format(Delta_value))
        print('sigma = {:.3g} Ang'.format(sigma_width))
        print('d(001) left = {:.3g} Ang'.format(d_space_left))
        print('d(001) right = {:.3g} Ang'.format(d_space_right))
        print('interface position = {:.4g} Ang'.format(interface_pos))
        print('----------------------------------------------------------')
        return dic_to_return

    def update_ref_point(self,ref_point):
        '''

        Parameters
        ----------
        ref_point : float
            The new reference point you wish to update for.

        Returns
        -------
        None
            Just update class object property.
        '''
        ref_point =np.float64(ref_point)
        ref_point = cons.m2A(ref_point)
        self.ref_point = ref_point
