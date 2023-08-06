# from Locpot_class import *
# from pymatgen.io.vasp.outputs import Locpot
# from pymatgen.core.structure import Structure, Lattice
# from Stage_1 import *
# from Stage_2 import *
# import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import math
# import os
# import PySimpleGUI as sg
#
# if __name__ == '__main__':
#      Locp = Locpot_yair(
#      Locpot_Full_path=r"C:\Users\user\OneDrive - Technion\Master degree\my_seminar\New Interfaces\Si-GaAs\Interface\average\LOCPOT",
#         axis_index=2, Has_interface=False)
# #     Locp.averaging_along_axis(to_plot=True,to_plot_atoms=True)
#
#     zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
#     except AssertionError:
#         if not Locp.locpot_bulk_materials == []:
#             zz, vv = Locpot_yair(input_locpot=Locp.locpot_bulk_materials[0]).locpot_vec.T
#             zz, vv = multiply_z_v_vecs(zz, vv, 10)
#             zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
#         else:
#             zz, vv = Locpot_yair(input_locpot=Locp).locpot_vec.T
#             zz, vv = multiply_z_v_vecs(zz, vv, 10)
#             zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
# #     # zz_convg, vv_convg, psi0_convg, grid_density, psi0_dic = stg1.converge_main_axis_grid(tol=0.01)
# #     # psi0_dic = stg1.get_psi_dic()
# #     # grid_density = np.float64(len(zz_convg) / (zz_convg[-1] - zz_convg[0]))
# #     #
# #     # minima = find_peaks_minima(Locp.locpot_vec[:, 0], Locp.locpot_vec[:, 1], ignore_local_minima=True)
# #     # minima_z = cons.A2m(minima[:, 0])
# #     # minima_v = minima[:, 1]
# #     # ind_start, pos_start = find_closest_value_in_array(74.584, minima_z)
# #     # ind_start, pos_start = find_closest_value_in_array(pos_start, cons.A2m(Locp.locpot_vec[:, 0]))
# #     # ind_final, pos_final = find_closest_value_in_array(83.16, minima_z)
# #     # ind_final, pos_final = find_closest_value_in_array(pos_final, cons.A2m(Locp.locpot_vec[:, 0]))
# #     # z_in = Locp.locpot_vec[:, 0][ind_start:ind_final]
# #     # v_in = Locp.locpot_vec[:, 1][ind_start:ind_final]
# #     # z_in, v_in = fix_potential_edges(z_in, v_in)
# #     # side = 'right'
# #     # right_multi = 20
# #     # left_multi = 1
# #     # manual_multi = right_multi
# #     # stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=True, To_plot=True, multi_left=left_multi,
# #     #                multi_right=right_multi,
# #     #                Nt=500, dt=0.1e-17)
# #     # init_len = cons.m2A(stg2.current_locpot_vec[:, 0][-1])
# #     #
# #     # stg2.elongate_interface_potential(from_iteslf=False, side_from_itself=side, z_in=z_in, v_in=v_in,
# #     #                                   manual=True, multi_manual=manual_multi,
# #     #                                   pos_to_insert=74.584, To_update=True)
# #
# #     plt.plot(stg2.elongated_locpot_vec[:,0],stg2.elongated_locpot_vec[:,1])
# #     plt.show()
# # print("--------------------------------")
# # print("--------------------------------")
# # print('Final dt = {:.5e} sec'.format(cons.fs2sec(stg2.dt)))
# # print('Final k0 = {:.5e} 1/Ang'.format(stg2.psi0_dic['k0']))
# # print('Final sigma = {:.5g} Ang'.format(cons.m2A(stg2.psi0_dic['sigma'])))
# # print('E0  = {:.5g} eV'.format(cons.J2eV(stg2.psi0_dic['E0'])))
# # print('N = {:.5g} partitions'.format((stg2.psi0_dic['N'])))
# # print('Nt = {:.5g} time steps'.format(stg2.Nt))
# # print("--------------------------------")
# # print("--------------------------------")
# #
# # z = stg2.current_locpot_vec[:,0]
# # z = cons.A2m(z)
# # kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
# # kk = to_1D_vec(kk)
# # results_Trans = transmision_coeff(stg2.psi0, 2000, stg2.dt,
# #                                   stg2.current_locpot_vec[:, 1],
# #                                   stg2.current_locpot_vec[:, 0], kk,stg2.new_interface, path_to_save=overall_values['-sys_size_save_path-'],final_time = 4)
