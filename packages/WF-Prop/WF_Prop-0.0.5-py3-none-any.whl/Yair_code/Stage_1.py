

from Locpot_class import *
from Help_function_library_yair import *


class Stage_1:
    '''
    This class aimed to create the initial wavefunction in its most general form, when it is
    initialized within the range of one of the materials in the system.

    '''
    def __init__(self, locpot_vec, E0, sigma, z_original=None, Max_z_iterations=10,
                 Noriginal=None, allmin=None, To_plot=False, allmax=None):
        '''

        Parameters
        ----------
        locpot_vec : `numpy.ndarray`, (N,2)
                This is a 2 column matrix. The first colmn is ``z``, the spacial coordinates vector and second is ``v``, the local potential vector.
        E0 : float
                The initial energy of the wave-function. Accounted to the total energy of an electron at the bottom of the cunduction band (CBM).
        sigma : float
                The standard deviation of the guassian electron wave-pocket.
        z_original : np.array, array_like, optional, defualt: None
                The original, initial spacial coordinates vector.
        Max_z_iterations : int, optional, defualt: 10
                The maximum number of the iterations that the loop will be going through until convergence of the drid density.
        Noriginal : int, optional, defualt: None
                The initial/ original number of spacial steps, the number of `dx`'s in the spacial coordinates vector. If not
                supplied, it will take the value of ``len(z_original)``
        allmin : `numpy.ndarray`, (N,2), defualt: None
                This is a matrix with 2 columns. The first column holds the minimum points position, and the second column
                holds the minimum points height. If not supplied it will take the matrix the resultd from
                ``find_peaks_minima(self.locpot_vec[:, 0], self.locpot_vec[:, 1])``.
        To_plot : bool, optional, defulat: False
                A flag to determine whether to plot or not.
        allmax : `numpy.ndarray`, (N,2), defualt: None
                This is a matrix with 2 columns. The first column holds the maximum points position, and the second column
                holds the maximum points height. If not supplied it will take the matrix the resultd from
                ``find_peaks_maxima(self.locpot_vec[:, 0], self.locpot_vec[:, 1])``.
        '''
        self.locpot_vec = locpot_vec
        self.E0 = E0
        self.Max_z_iterations = Max_z_iterations
        self.Noriginal = Noriginal
        if self.Noriginal is None:
            self.Noriginal = len(self.locpot_vec[:, 0])
        self.L = self.locpot_vec[len(self.locpot_vec[:, 0]) - 1, 0]  # determined by the
        # last position in the locpot of the whole system
        self.allmin = allmin
        if self.allmin is None:
            self.allmin = find_peaks_minima(self.locpot_vec[:, 0], self.locpot_vec[:, 1])
        self.allmax = allmax
        if self.allmax is None:
            self.allmax = find_peaks_maxima(self.locpot_vec[:, 0], self.locpot_vec[:, 1])
        self.z_original = z_original
        if self.z_original is None:
            self.z_original = self.locpot_vec[:, 0]
        self.alpha = 1.3
        self.delta_z_step = None
        if self.L is not None and self.Noriginal is not None and self.delta_z_step is None:
            self.delta_z_step = self.L / (self.Noriginal - 1)
        self.sigma = sigma  # uncertainty in position
        self.cons = Constants()
        self.To_plot = To_plot

    def initial_wavefunc_energies(self, N=None, Multi = 5):
        '''

        Class method of Stage1. Calculate the initial Wavefunction

        Parameters
        ----------
        N : int/float, optional, defualt: None
                It can be delivered in order the determine the number of the samples
                that the wavefunction will be constructed based on it.
        Multi : int/float, optional, defualt: 5
                If the initial unit is too small, you can choose
                how many times to mulyiply it in order to produce the initial wavefucntion
                matched the larger unit cell.

        Returns
        -------
        np.array, np.array, np.array, np.array, np.array, int
                zz - the new coords divided into N segments.
                vv - the new potential vector divided into N segments.
                psi0 - the initial wave function. (N,)
                T0 - initial kinteic energy. Float
                v0 - potential expectation value. Float.
                N - The number of the partition.

       '''
        if N is None:
            N = self.Noriginal
        self.L = cons.A2m(self.L)
        self.delta_z_step = self.L / N
        self.delta_z_step = self.cons.A2m(self.delta_z_step)
        self.z_original = self.cons.A2m(self.z_original)
        self.sigma = self.cons.A2m(self.sigma)
        # self.dz = self.find_peak_half_max_width()
        self.E0 = self.cons.eV2J(self.E0)
        zz, vv = interpolate_cubic(N, self.locpot_vec[:, 0], self.locpot_vec[:, 1])
        vv = self.cons.eV2J(vv)

        # =============================================================================
        #      finding x0 - the initial position of an electron at a minimum point
        #      inside a material - far from the interface
        # =============================================================================
        mid_min = np.int64(np.fix(len(self.allmin[:, 0]) / 2)) + np.mod(len(self.allmin[:, 0]), 2) - 1
        mid_min = self.allmin[mid_min][0]
        mid_min = self.cons.A2m(mid_min)
        z0 = [i for i in self.z_original if i == mid_min][0]
        zz, initial_wave_func = get_psi0(0.1, self.sigma, z0, zz)  # k0 does not affect the V_expec
        v0 = potential_expectation_nadav(initial_wave_func, np.diff(zz)[0], vv)
        v0 = cons.eV2J(v0)
        # =============================================================================
        #         finding initial momentum k0 from solving the equa (1) from the doc development.
        # =============================================================================
        T0 = self.E0 - v0
        gauss_wave_function = lambda z: gaussian_function(z, 0.1, cons.m2A(self.sigma), cons.m2A(z0))
        # k0 does not affect the normalization factor.
        A = normalize_wave_function(gauss_wave_function,units='Meter')
        try:
            k0 = initial_momentum_yair(self.sigma, self.E0, self.L, z0, A, T0)
        except ValueError:
            allmax = find_peaks_maxima(self.locpot_vec[:, 0], self.locpot_vec[:, 1], ignore_local_maxima=True)
            maxima = [i for i in range(len(self.locpot_vec[:, 0])) if self.locpot_vec[:, 0][i] in allmax[:, 0]]
            widths, width_heights, left_ips, right_ips = ss.peak_widths(self.locpot_vec[:, 1], maxima, rel_height=0.5)
            max_index = len(self.locpot_vec[:, 0]) - 1
            max_coord = self.locpot_vec[:, 0][-1]
            new_left_ips = []
            new_right_ips = []
            new_widths = []
            for i in range(len(left_ips)):
                new_left_ips.append((left_ips[i] * max_coord) / max_index)
                new_right_ips.append((right_ips[i] * max_coord) / max_index)
                new_widths.append(((right_ips[i] * max_coord) / max_index) - (left_ips[i] * max_coord) / max_index)
            anotations = []
            count = 0
            new_left_ips = np.array(new_left_ips)
            new_right_ips = np.array(new_right_ips)
            new_widths = np.array(new_widths)
            self.sigma = np.average(new_widths)
            try:
                k0 = initial_momentum_yair(self.sigma, self.E0, self.L, z0, A, T0)
            except ValueError:
                k0 = initial_momentum_yair(self.sigma, self.E0, self.L*3, z0+self.L*2, A, T0)

        # =============================================================================
        #         calculate the initial wave function vector
        # =============================================================================
        zz, initial_wave_func = get_psi0(k0, self.sigma, z0, zz)

        return np.squeeze(zz), np.squeeze(vv), k0, np.squeeze(initial_wave_func), \
               np.squeeze(T0), np.squeeze(v0), np.squeeze(N)

    def calculate_E0(self, zz, vv, psi0, N=None):
        '''
        Class method of Stage1. Calculating E0 per each N partition of space(z)

        Parameters
        ----------
        zz : np.array
                Vector of the spacial grid. (spacial coordinates)
        vv : np.array
                Vector of the local potential.
        psi0 : np.array
                The wave-function vector.
        N : int, optional, defualt: None
                The number of spacial steps, the number of `dx`'s.
         '''
        zz = to_column_vec(zz)
        zz = self.cons.A2m(zz)
        vv = to_column_vec(vv)
        vv = self.cons.eV2J(vv)
        psi0 = to_column_vec(psi0)
        self.L = self.cons.A2m(self.L)
        if N is None:
            N = self.Noriginal
        T0num = kinetic_energy_expectation_value(psi0, zz)

        dz = np.diff(to_1D_vec(zz))[0]
        # calculationg the average potential energy for uniform deltaz
        # v0num = potential_expectation_nadav(psi0, dz, vv)

        v0num = np.real(dz * psi0.T @ np.conj(to_column_vec(to_1D_vec(vv) * to_1D_vec(psi0))))
        # [J]
        v0num = np.squeeze(v0num)

        # calculationg the average total energy
        E0num = T0num + v0num  # [J]

        return np.squeeze(E0num), np.squeeze(T0num), np.squeeze(v0num)

    def converge_main_axis_grid(self, tol = 0.001):
        '''
        Converges the spacial grid of the system according to total energy difference of the tol parameter supplied
        as an input. The difference relates to two consecutive iterations. It also demands that the spacial spacing not
        be less than tol*sigma.

        Parameters
        ----------
        tol : float, optional, defualt: 0.001
                It refers to tolerance. And it can make the condition for convergence
                more or less strict.

        Returns
        -------
        zz_convg : np.array
                The converged spacial grid vector.
        vv_convg : np.array
                The converged local potential vector.
        psi0_convg : np.array
                The converged wave function values vector.
        grid_density : float
                The converged spacial grid density. It is defined as the number of the spacial points divided by the system length.
        psi0_dic : dict
                It holds all the necessary parameters that relate to the converged system and the convereged wave-function.
                psi0_dic = {'k0' : , 'sigma':  , 'E0':  ,'zz': zz_convg, 'vv':vv_convg,'N': N_convg,'psi0':psi0_convg}
        '''
        N = np.fix(self.Noriginal)
        E0num = np.array([[], []]).T
        T0num = np.array([[], []]).T
        v0num = np.array([[], []]).T
        T0 = np.array([[], []]).T
        v0 = np.array([[], []]).T
        k0 = np.array([[], []]).T

        # calculating the first two E0num
        for i in range(0, 2):
            # calculating the initial wavefunction and potential energy according to N
            zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = self.initial_wavefunc_energies(N=N)
            if N != N_new:
                N = N_new

            # calculating the initial numerical total energy according to N
            E0num_run, T0num_run, v0num_run = self.calculate_E0(zz, vv, psi0, N=N)
            k0_run = np.float64(k0_initial)
            # saving the initials energies per number of steps
            E0num = np.vstack([E0num, [E0num_run, N]])
            T0num = np.vstack([T0num, [T0num_run, N]])
            v0num = np.vstack([v0num, [v0num_run, N]])
            T0 = np.vstack([T0, [T0_run, N]])
            v0 = np.vstack([v0, [v0_run, N]])
            k0 = np.vstack([k0, [k0_run, N]])
            N = N * self.alpha
            N = np.round(N)

        iteration = 1
        self.delta_z_step = self.L / N
        flag = False
        while (not (np.abs(self.delta_z_step) < tol * self.cons.A2m(self.sigma) and self.cons.J2eV(np.abs((E0num[iteration][0]-E0num[iteration-1][0]))) < tol)) and iteration < self.Max_z_iterations:
            flag = True
            zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = self.initial_wavefunc_energies(N=N)
            if N != N_new:
                N = N_new
            # calculating the initial numerical total energy according to N
            E0num_run, T0num_run, v0num_run = self.calculate_E0(zz, vv, psi0, N=N)
            k0_run = k0_initial
            k0_run = np.float64(k0_initial)
            # saving the initials energies per number of steps
            E0num = np.vstack([E0num, [E0num_run, N]])
            T0num = np.vstack([T0num, [T0num_run, N]])
            v0num = np.vstack([v0num, [v0num_run, N]])
            T0 = np.vstack([T0, [T0_run, N]])
            v0 = np.vstack([v0, [v0_run, N]])
            k0 = np.vstack([k0, [k0_run, N]])
            N_1 = N * self.alpha
            N_1 = np.round(N_1)
            self.delta_z_step = self.L / N_1

            iteration += 1
            if iteration == self.Max_z_iterations - 1:
                print('maximum z-direction convergence iterations was reached')
                break
            else:
                if  np.abs(self.delta_z_step) < tol * self.cons.A2m(self.sigma) and self.cons.J2eV(np.abs((E0num[iteration][0]-E0num[iteration-1][0]))) < tol:
                    print('convergence limit was reached')
                    break
                else:
                    N = N_1

        if not flag:
            N = N  / self.alpha
            N = np.round(N)
        self.delta_z_step = self.L / N
        psi0_convg = psi0
        E0_convg = E0num[-1, 0] / self.cons.eV2J(1)
        N_convg = N
        deltaz_convg = self.delta_z_step
        zz_convg = zz
        # kk_convg = kk
        vv_convg = vv
        grid_density = N / self.cons.m2A(zz_convg[-1])
        psi0_dic = {'k0' :k0[-1,0], 'sigma': self.sigma, 'E0': E0_convg,'zz': zz_convg, 'vv':vv_convg,'N': N_convg,'psi0':psi0_convg}
        if np.shape(zz_convg)[0] != N_convg and not ( np.shape(zz_convg)[0] - 1 <= N_convg <= np.shape(zz_convg)[0] + 1) :
            print('Z coordinates grid is not consistent with the N samples converged value.')
            #  if np.shape(kk)[0] != N_convg:
            print('k coordinates grid is not consistent with the N samples converged value.')
        if np.shape(vv_convg)[0] != N_convg and not ( np.shape(vv_convg)[0] - 1 <= N_convg <= np.shape(vv_convg)[0] + 1) :
            print('V potential values number of measurements is not consistent with the N samples converged value.')


        if self.To_plot:
##################################
### This part is only for plotting.
##################################
            font = {'family': 'serif', 'size': 15}
            plt.rc('font', **font)
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'initial Wave function and probabilty, $| \psi_0 |^2$')
            ax = plt.subplot(gs[0])
            ax.plot(self.cons.m2A(zz_convg), np.real(psi0_convg) * 1E-5, label=r'$real(\psi_0) $')
            ax.plot(self.cons.m2A(zz_convg), np.abs(psi0_convg ** 2) * 1E-10, linewidth=2, label=r'$| \psi_0 |^2$')
            ax.grid()
            ax.set_xlabel(r'Z axis, [$\AA$]', fontsize=14)
            ax.set_ylabel(r'$| \psi_0 |^2$, real($\psi_0$)', fontsize=14)
            ax.legend(fancybox=True, shadow=False, prop={'size': 14})
            plt.savefig(sys.argv[0].strip(".py") + ".pdf", format="pdf")

            font = {'family': 'serif', 'size': 15}
            plt.rc('font', **font)
            gs = GridSpec(1, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Original and Spline Potential energy , $V(z)$')
            ax_1 = plt.subplot(gs[0])
            ax_1.plot(self.cons.m2A(zz_convg), self.cons.J2eV(vv_convg), label='Spline')
            ax_1.plot(self.cons.m2A(self.locpot_vec[:, 0]), self.cons.J2eV(self.locpot_vec[:, 1]), '--',
                      linewidth=2, label='Original')
            ax_1.grid()
            ax_1.set_xlabel(r'Z axis, [$\AA$]', fontsize=14)
            ax_1.set_ylabel(r'Potential Energy, V(z), [eV]', fontsize=14)
            ax_1.legend(fancybox=True, shadow=False, prop={'size': 14})
            plt.savefig(sys.argv[0].strip(".py") + ".pdf", format="pdf")

            plt.rc('font', **font)
            gs = GridSpec(3, 1)
            fig = plt.figure(figsize=(16, 11))
            fig.suptitle(r'Convergence plots Vs N , #samples')
            Ax_i = []
            for i in range(0, 3, 1):
                Ax_i.append(plt.subplot(gs[i]))

            Ax_i[2].set_xlabel(r"Samples#, N")
            Ax_i[0].set_ylabel(r"Initial Total energy, $E_0$ [eV]", fontsize=9)
            Ax_i[1].set_ylabel(r"Initial Kinetic energy, $T_0$ [eV]", fontsize=9)
            Ax_i[2].set_ylabel(r"Initiail Potential energy energy,$V_0$ [eV]", fontsize=9)

            Ax_i[0].plot(E0num[:, 1], self.cons.J2eV(E0num[:, 0]), 'b', label='E0num')
            tx = np.average(E0num[:, 1])
            ty = np.average(self.cons.J2eV(E0num[:, 0]))
            Ax_i[0].annotate(r"$E_0$ = {} [eV], input as $E_c$".format(format(self.cons.J2eV(self.E0), ".3f")),
                             xy=(tx, ty), xycoords='data')
            Ax_i[0].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            Ax_i[0].yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

            Ax_i[1].plot(T0num[:, 1], self.cons.J2eV(T0num[:, 0]), 'r', label='T0num')
            Ax_i[1].plot(T0[:, 1], self.cons.J2eV(T0[:, 0]), color='green', linestyle='dashed',
                         label='T0 - calc from E0-V0')
            Ax_i[1].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            Ax_i[1].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

            Ax_i[2].plot(v0num[:, 1], self.cons.J2eV(v0num[:, 0]), 'r', label='V0num')
            Ax_i[2].plot(v0[:, 1], self.cons.J2eV(v0[:, 0]), color='green', linestyle='dashed',
                         label='V0 - calc as exp-Value')
            Ax_i[2].ticklabel_format(useOffset=True, useMathText=True, style='sci')
            Ax_i[2].yaxis.set_major_formatter(FormatStrFormatter('%.5f'))

            for i in range(0, 3, 1):
                Ax_i[i].grid()
                Ax_i[i].legend(fancybox=True, shadow=False, prop={'size': 14})
            plt.show()

        return zz_convg, vv_convg, psi0_convg, grid_density, psi0_dic

    def get_psi_dic(self):
        '''

        Returns
        -------
        dict
            It retruns a initial wave function parameters in a dictionary for the next stage.
        '''
        N = np.fix(self.Noriginal)
        zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = self.initial_wavefunc_energies(N=N)
        grid_density = N / self.cons.m2A(zz[-1])
        psi0_dic = {'k0': k0_initial, 'sigma': self.sigma, 'E0': self.E0, 'zz': zz, 'vv': vv, 'N': N,
                    'psi0': psi0}
        return psi0_dic



    def set_To_plot(self, To_plot):
        '''
        A class method to set the ``To_plot`` attribute.

        Parameters
        ----------
        To_plot : bool
            It gets True or False whether to plot or not.

        This is a class method that enables to turn on plotting options or
        to turn them off. True = for turning on, False = for turning off.
        '''
        self.To_plot = To_plot


def main():
    pass


if __name__ == '__main__':
    main
