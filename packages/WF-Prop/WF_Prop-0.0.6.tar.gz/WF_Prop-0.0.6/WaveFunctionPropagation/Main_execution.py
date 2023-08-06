from Locpot_class import *
from pymatgen.io.vasp.outputs import Locpot, Vasprun
from pymatgen.core.structure import Structure, Lattice
from Stage_1 import *
from Stage_2 import *
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import os
import PySimpleGUI as sg


def convert_to_type(values_dic):
    for k, it in values_dic.items():
        try:
            values_dic[k] = np.float64(it)
        except ValueError:
            pass
    return values_dic


def Gui():

#if __name__ == '__main__':

    sg.theme('DarkAmber')  # Keep things interesting for your users
    SYMBOL_UP = '▲'
    SYMBOL_DOWN = '▼'

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['Help', 'About...'], ]

    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Text('Wave Function propagation Gui', size=(50, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
              [sg.Text('Open the locpot file of your system. If you have the locpot of your bulk materials, you should supply them too')],
              [sg.Text('Main Locpot File', size=(18, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('Bulk material locpot 1', size=(18, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('Bulk material locpot 2', size=(18, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('If you want your E0 to be imported from your calculation, please Load here your', size=(60, 1))],
              [sg.Text('vapsrun file - for the bulk material you wish to initialize the electron at',size=(60, 1))],
              [sg.Text('vasprun file', size=(18, 1)), sg.Input(), sg.FileBrowse(key='-vasprun_file-')],
              [sg.Frame('select',layout=[[sg.Checkbox('Has an interface?', size=(20,1),default=False, key='-interface-')], [sg.Checkbox('Is 2D?', default=False,disabled=True,key='-2D-')],[sg.Checkbox('Define a certain range?', default=False,key='-Range-')],
                                         [sg.Checkbox('Flip sides of your interface', default=False,key='-flip-')]])] ,
              [sg.Text('What convergence test you wish to perform?')],
              [sg.Frame('Convergence Tests',layout=[[sg.Checkbox('spatial grid density', size=(40,1),key='-density-')], [sg.Checkbox('System size',  size=(40,1),key='-sys_size-')],[sg.Checkbox('Time steps', size=(40,1),key='-dt-')]])],
              [sg.Text('Please input here the initial energy. The energy of an electron at the bottom of the conduction band. In units of Joules')],
              [sg.In(default_text=5e-19, size=(10, 1),key='-E0-')],
              [sg.Text(
                  'Please input here the standard deviation of the guassian wave function. This should be given in units of Meter')],
              [sg.In(default_text=0.7e-10, size=(10, 1), key='-sigma-')],
              [sg.Text(
                  'Please input here the Initial number of time steps. The number of dt the overall simulation will undergo. This should be an integer')],
              [sg.In(default_text=500, size=(10, 1), key='-Nt-')],
              [sg.Text(
                  'Please input here the Initial value of your time step, dt. It will be used as an initial guess of the default value')],
              [sg.In(default_text=0.5e-17, size=(10, 1), key='-initial_dt-')],
              [sg.Text('Please choose the axis you wish to average the local potential')],
              [sg.Frame('axes',layout=[[sg.Checkbox('x', size=(20,1),key='-x_axis_grid-')],[sg.Checkbox('y', size=(20,1),key='-y_axis_grid-')],[sg.Checkbox('z', size=(20,1),key='-z_axis_grid-',default=True)]])],
              [sg.Text('Choose from the options what you would like to do')],
              [sg.Frame('Options',layout=[[sg.Checkbox('Print averaged local potential', size=(40,1),key='-Pr_avg_locpot-')], [sg.Checkbox('Extend Locpot',  size=(40,1),key='-ext_locpot-')],[sg.Checkbox('Full propagation', size=(40,1),key='-Full_prop-')],
                                          [sg.Checkbox('Transmission coefficient', size=(40,1),key='-Trans_coeff-')],[sg.Checkbox('Cumulative probability', size=(40,1),key='-cum_prob-')],
                                          [sg.Checkbox('Modeling the interface', size=(40,1),key='-modeling_interface-')]])],
              [sg.Submit(), sg.Cancel()],
              [sg.Text('')],[sg.Text('')]]
    column = [[sg.Column(layout,scrollable=True,key='Column',size=(900,3000))]]
    window = sg.Window('Propagate wave-function Menu ', column,resizable=False, size=(900,3000))

    event, values = window.read()
    window.close()

    overall_values = {}
    overall_values.update(values)
    if overall_values['Browse'] == "" and not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel'):
        overall_values['Browse'] = sg.popup_get_file('You must supply the locpot of your system.')
        if overall_values['Browse'] == "":
            sg.popup_error('You must supply The locpot file of your system')
            SystemError('You must supply The locpot file of your system')

    # ------------------------------------------------------------------------------------------

    #...........................................................................................

    # ------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------

    # ..........................................................................................

    # if not overall_values['-dt-'] and not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel'):
    #     layout_temp = [[sg.Menu(menu_def, tearoff=True)],
    #           [sg.Text('Please supply the size of dt you want to apply, in seconds, scale of fsec', size=(100, 1))],
    #           [sg.In(default_text=0.1e-16, size=(20, 1),key='-initial_dt-')],
    #           [sg.Submit(), sg.Cancel()]]
    #     window_temp = sg.Window('Initial Time step magnitue ', layout_temp)
    #     event_temp, values_temp = window_temp.read()
    #     window_temp.close()
    #     overall_values.update(values_temp)
    # elif not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel'):
    #     layout_temp = [[sg.Menu(menu_def, tearoff=True)],
    #           [sg.Text('Do you want to change the initial value of dt? You can edit it here', size=(100, 1))],
    #           [sg.In(default_text=0.1e-16, size=(20, 1),key='-initial_dt-')],
    #           [sg.Submit(), sg.Cancel()]]
    #     window_temp = sg.Window('Initial Time step magnitue ', layout_temp)
    #     event_temp, values_temp = window_temp.read()
    #     window_temp.close()
    #     overall_values.update(values_temp)



    # ------------------------------------------------------------------------------------------

    # ..........................................................................................

    # ------------------------------------------------------------------------------------------

    # Main menu handling,     # axis grid definition
    # Processing the very first information.
    # Loading the locpot, reading the gird axis - to be able to plot basic plots.
    try:
        event_temp
    except NameError:
        event_temp = 'Cancel'
    already_plotted_base_loc_vec=False

    # General operations before starting.
    # Defining grid axis, Loading Locpots from the browser.
    if not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel'):
        overall_values = convert_to_type(overall_values)
        if overall_values['-x_axis_grid-']:
            axis = 0
        elif overall_values['-y_axis_grid-']:
            axis = 1
        else:
            axis = 2
        # Locpot files loading
        if overall_values['Browse0'] =="" and not overall_values['Browse1'] =="":
            overall_values['Browse0'] = overall_values['Browse1']
            overall_values['Browse1'] = ""
        if not overall_values['Browse0'] =="":
            if not overall_values['Browse1'] =="":
                Locp = Locpot_yair(Locpot_Full_path= overall_values['Browse'],Locpot_bulk_materials_full_path=[overall_values['Browse0'],overall_values['Browse1']],axis_index=axis,Has_interface=overall_values['-interface-'],to_flip=overall_values['-flip-'])
            else:
                Locp = Locpot_yair(Locpot_Full_path=overall_values['Browse'],
                                   Locpot_bulk_materials_full_path=overall_values['Browse0'],
                                   axis_index=axis, Has_interface=overall_values['-interface-'],to_flip=overall_values['-flip-'])
        else:
            Locp = Locpot_yair(Locpot_Full_path=overall_values['Browse'],
                               axis_index=axis, Has_interface=overall_values['-interface-'],to_flip=overall_values['-flip-'])
    # ------------------------------------------------------------------------------------------

    # ..........................................................................................

    # ------------------------------------------------------------------------------------------
        # Handling the type of system you chose.
        # if does not have an interface and didnt provide a range.
        # in this case the user will be rquired to supply a reference point to be treated as an interface point.
        if not overall_values['-interface-'] and not overall_values['-Range-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Please supply the position where you want to treat as a reference point.',
                                    size=(80, 1)),
                            [sg.In(default_text='0', size=(10, 1), key='-ref_pos-')]],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Reference Position ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-ref_pos-'] = np.float64(overall_values['-ref_pos-'])
            overall_values['-ref_pos-'] = cons.A2m(overall_values['-ref_pos-'])

        # Handling the type of system you chose.
        # if does not have an interface but did provide a range.
        # in this case the user will be rquired to supply the range limits..
        if overall_values['-Range-'] and not overall_values['-interface-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text(
                               'Please supply the initial and final positions where you want to define your system.',
                               size=(80, 1))],
                           [[sg.Text('Start Position, in [M]', size=(10, 1))],
                            [sg.In(default_text=0, size=(10, 1), key='-Initi_pos-')]],
                           [[sg.Text('Final Position, in [M]', size=(10, 1))],
                            [sg.In(default_text=0, size=(10, 1), key='-Final_pos-')]],
                           [[sg.Text('Please supply the position where you want to treat as a reference point.',
                                     size=(80, 1))],
                            [sg.In(default_text=0, size=(10, 1), key='-ref_pos-')]],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Range Choice ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-Initi_pos-'] = np.float64(overall_values['-Initi_pos-'])
            overall_values['-Final_pos-'] = np.float64(overall_values['-Final_pos-'])
            overall_values['-ref_pos-'] = np.float64(overall_values['-ref_pos-'])
            overall_values['-Initi_pos-'] = cons.A2m(overall_values['-Initi_pos-'])
            overall_values['-Final_pos-'] = cons.A2m(overall_values['-Final_pos-'])
            overall_values['-ref_pos-'] = cons.A2m(overall_values['-ref_pos-'])
        # Handling the type of system you chose.
        # if does have an interface and provide a range.
        # in this case the user will be rquired to supply the range limits and a reference point.
        if overall_values['-Range-'] and overall_values['-interface-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text(
                               'Please supply the initial and final positions where you want to define your system.',
                               size=(80, 1))],
                           [[sg.Text('Start Position, in [M]', size=(10, 1))],
                            [sg.In(default_text='0', size=(10, 1), key='-Initi_pos-')]],
                           [[sg.Text('Final Position, in [M]', size=(10, 1))],
                            [sg.In(default_text='0', size=(10, 1), key='-Final_pos-')]],
                           [[sg.Text('Please supply the position where you want to treat as a reference point.',
                                     size=(80, 1))],
                            [sg.In(default_text=0, size=(10, 1), key='-ref_pos-')]],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Range and interface Choice ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-ref_pos-'] = np.float64(overall_values['-ref_pos-'])
            overall_values['-ref_pos-'] = cons.A2m(overall_values['-ref_pos-'])
            overall_values['-Initi_pos-'] = np.float64(overall_values['-Initi_pos-'])
            overall_values['-Final_pos-'] = np.float64(overall_values['-Final_pos-'])
            overall_values['-Initi_pos-'] = cons.A2m(overall_values['-Initi_pos-'])
            overall_values['-Final_pos-'] = cons.A2m(overall_values['-Final_pos-'])

     # ------------------------------------------------------------------------------------------

     # ...........................................................................................

     # ------------------------------------------------------------------------------------------


        # ------------------------------------------------------------------------------------------

        # ...........................................................................................

        # ------------------------------------------------------------------------------------------
        # Handling the convergence tests
        # Grid-density convergence test:
        # first step is to get information about the spatial partition - the Nt's number.
        # is independent of if the user chose to perform grid density convergence test or not.
        if not overall_values['-density-'] and overall_values['-Nt-'] == "" and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text(
                               'Please supply the number of spatial partition you wish your system to have. The # of dx`s ',
                               size=(50, 1))],
                           [[sg.Text('It should be an integer. Nt = ', size=(40, 1))],
                            [sg.In(default_text='100', size=(20, 1), key='-Nt-')]],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Nt Choice ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)

        # if the user chose to perform grid-density convergence test - it will asked him to provide the number of max
        # iterations the loop will be going through.
        if overall_values['-density-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text(
                               'Please supply the maximum number of iterations you wish to perform during the grid-density convegence',
                               size=(100, 1))],
                           [sg.In(default_text=20, size=(20, 1), key='-conv_dens_iter-')],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Grid density convergence Choice for maximum number of iterations ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)


        # ------------------------------------------------------------------------------------------

        # ...........................................................................................

        # ------------------------------------------------------------------------------------------

        # The only operation that might affect the convergence tests:
        # extending the local potential vector.
        if overall_values['-ext_locpot-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('How do you want to extend your Locpot?', size=(100, 1))],
                           [sg.Frame('Locpot Elongation',
                                     layout=[[sg.Checkbox('Insertaion into a position within the locpot', size=(60, 1),
                                                          key='-ex_loc_insert-')],
                                             [sg.Checkbox('Just multiplication', size=(40, 1), key='-ex_loc_mul-')]])],
                           [sg.Text(
                               'find a bulk-like Locpot region, or choose it manually? ',
                               size=(100, 1))],
                           [sg.Frame('What to insert',
                                     layout=[[sg.Checkbox('bulk-like locpot', size=(40, 1), key='-ex_loc_bulk_like-')],
                                             [sg.Checkbox('Choose manually', size=(40, 1), key='-ex_loc_choose_manu-')]])],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Locpot elongation', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)

            # if you dont have an interface - it asks the user to supply how many time to multiply it and where to insert it.
            if overall_values['-ext_locpot-'] and not overall_values['-interface-'] and not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel'):
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                [sg.Text('How many times you would like to multiply the locpot', size=(70, 1))],
                [sg.Text('It will also going to be used as the number of times the inserted part will be multiplied',size=(100, 1))],
                [sg.In(default_text=10, size=(20, 1), key='-ex_loc_multi-')],
                [sg.Text('If you chose to insert into a certain position, please supply it here, in units of Angstrum',size=(100, 1))],
                [sg.In(default_text=0, size=(20, 1), key='-ex_loc_insert_pos-')],
                [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Locpot elongation', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)


            # If the user defined his system to have an interface he can choose from what side to elongate his locpot.
            if overall_values['-ext_locpot-'] and overall_values['-interface-'] and not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel'):
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Do you want to elongate from both sizes of the interface, or just from one side',size=(100, 1))],
                               [sg.Text('Please choose only one category and fill only it in',size=(100, 1))],
                               [sg.Frame('Locpot Elongation', layout=[
                                   [sg.Checkbox('Both sizes', size=(40, 1), key='-ex_loc_both-')],
                                   [sg.Text('How many times', size=(40, 1))],
                                   [sg.In(default_text=10, size=(20, 1), key='-ex_loc_both_multi-')],
                                   [sg.Checkbox('Right size', size=(40, 1), key='-ex_loc_right-')],
                                   [sg.Text('How many times', size=(40, 1))],
                                   [sg.In(default_text=0, size=(20, 1), key='-ex_loc_right_multi-')],
                                   [sg.Checkbox('Left size', size=(40, 1), key='-ex_loc_left-')],
                                   [sg.Text('How many times', size=(40, 1))],
                                   [sg.In(default_text=0, size=(20, 1), key='-ex_loc_left_multi-')]
                               ]
                                         )],
                               [sg.Submit(), sg.Cancel()]]

                window_temp = sg.Window('Locpot elongation', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values = convert_to_type(overall_values)

        # Choosing manually the region to be multiplied
        # ========================================================================
        if overall_values['-ext_locpot-'] and overall_values['-interface-'] and overall_values['-ex_loc_choose_manu-'] and overall_values['-ex_loc_both-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                    Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                    already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Frame('Locpot Elongation', layout=[
                                   [sg.Text('choose range from the left side', size=(40, 1))],
                                   [sg.Text('Initial position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_left_init_pos-')],
                                   [sg.Text('Final position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_left_final_pos-')],
                                   [sg.Text('choose range from the Right side', size=(40, 1))],
                                   [sg.Text('Initial position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_right_init_pos-')],
                                   [sg.Text('Final position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_right_final_pos-')],
                                   ])],
                               [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Interface system elongation', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values = convert_to_type(overall_values)
            overall_values['-ex_loc_choose_manu_left_init_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_left_init_pos-'])
            overall_values['-ex_loc_choose_manu_left_init_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_left_init_pos-'])
            overall_values['-ex_loc_choose_manu_left_final_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_left_final_pos-'])
            overall_values['-ex_loc_choose_manu_left_final_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_left_final_pos-'])
            overall_values['-ex_loc_choose_manu_right_init_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_right_init_pos-'])
            overall_values['-ex_loc_choose_manu_right_init_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_right_init_pos-'])
            overall_values['-ex_loc_choose_manu_right_final_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_right_final_pos-'])
            overall_values['-ex_loc_choose_manu_right_final_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_right_final_pos-'])


        if overall_values['-ext_locpot-'] and overall_values['-interface-'] and overall_values['-ex_loc_choose_manu-'] and (overall_values['-ex_loc_right-'] or overall_values['-ex_loc_left-'])  and \
            (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                    Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                    already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Frame('Locpot Elongation', layout=[
                                   [sg.Text('choose range to be inserted', size=(40, 1))],
                                   [sg.Text('Initial position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_init_pos-')],
                                   [sg.Text('Final position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_final_pos-')]]
                                   )],
                               [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Interface system elongation', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values = convert_to_type(overall_values)
            overall_values['-ex_loc_choose_manu_init_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_init_pos-'])
            overall_values['-ex_loc_choose_manu_init_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_init_pos-'])
            overall_values['-ex_loc_choose_manu_final_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_final_pos-'])
            overall_values['-ex_loc_choose_manu_final_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_final_pos-'])

        if overall_values['-ext_locpot-'] and not overall_values['-interface-'] and overall_values['-ex_loc_choose_manu-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not already_plotted_base_loc_vec:
                    Locp.averaging_along_axis(to_plot=True,to_plot_cursor_choice=True)
                    already_plotted_base_loc_vec = True
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Frame('Locpot Elongation', layout=[
                                   [sg.Text('choose range to be inserted', size=(40, 1))],
                                   [sg.Text('Initial position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_init_pos-')],
                                   [sg.Text('Final position', size=(20, 1)),
                                   sg.In(default_text=0, size=(20, 1), key='-ex_loc_choose_manu_final_pos-')]
                                   ])],
                               [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Interface system elongation', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values = convert_to_type(overall_values)
            overall_values['-ex_loc_choose_manu_init_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_init_pos-'])
            overall_values['-ex_loc_choose_manu_init_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_init_pos-'])
            overall_values['-ex_loc_choose_manu_final_pos-'] = np.float64(overall_values['-ex_loc_choose_manu_final_pos-'])
            overall_values['-ex_loc_choose_manu_final_pos-'] = cons.A2m(overall_values['-ex_loc_choose_manu_final_pos-'])

        # ========================================================================
        # Before handling the convergence test we can check if we can import E0 from a vasprun file
        if not overall_values['-vasprun_file-'] == '':
            vasprun = Vasprun(overall_values['-vasprun_file-'])
            try:
                overall_values['-E0-'] = vasprun.get_band_structure().get_cbm()['energy']
                overall_values['-E0-'] = cons.eV2J(overall_values['-E0-'] )
            finally:
                pass

        # Now handling Convergence tests defined in the main form. Grid density convergence
        if overall_values['-density-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not Locp.locpot_bulk_materials ==[]:
                stg1 = Stage_1(Locpot_yair(input_locpot=Locp.locpot_bulk_materials[0]).locpot_vec, np.float64(overall_values['-E0-']), np.float64(overall_values['-sigma-']),
                               Noriginal=np.float64(overall_values['-Nt-']),
                               Max_z_iterations=np.int64(overall_values['-conv_dens_iter-']),
                               To_plot=True)
            else:
                stg1 = Stage_1(Locp.locpot_vec, np.float64(overall_values['-E0-']),np.float64(overall_values['-sigma-']), Noriginal=np.float64(overall_values['-Nt-']), Max_z_iterations=np.int64(overall_values['-conv_dens_iter-']),
                               To_plot=True)
            try:
                zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
            except AssertionError:
                if not Locp.locpot_bulk_materials == []:
                    zz, vv = Locpot_yair(input_locpot=Locp.locpot_bulk_materials[0]).locpot_vec.T
                    zz,vv = multiply_z_v_vecs(zz,vv,10)
                    zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
                else:
                    zz, vv = Locpot_yair(input_locpot=Locp).locpot_vec.T
                    zz,vv = multiply_z_v_vecs(zz,vv,10)
                    zz, vv, k0_initial, psi0, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
            zz_convg, vv_convg, psi0_convg, grid_density, psi0_dic = stg1.converge_main_axis_grid(tol=0.001)
        elif (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if not Locp.locpot_bulk_materials == []:
                stg1 = Stage_1(Locpot_yair(input_locpot=Locp.locpot_bulk_materials[0]).locpot_vec, np.float64(overall_values['-E0-']), np.float64(overall_values['-sigma-']),
                               Noriginal=np.float64(overall_values['-Nt-']),
                               To_plot=True)
            else:
                stg1 = Stage_1(Locp.locpot_vec, np.float64(overall_values['-E0-']),np.float64(overall_values['-sigma-']), Noriginal=np.float64(overall_values['-Nt-']), Max_z_iterations=10,
                               To_plot=True)
            try:
                zz_convg, vv_convg, k0_initial, psi0_convg, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
            except AssertionError:
                zz_convg, vv_convg = Locp.locpot_vec.T
                zz_convg, vv_convg = multiply_z_v_vecs(zz_convg, vv_convg, 10)
                zz_convg, vv_convg, k0_initial, psi0_convg, T0_run, v0_run, N_new = stg1.initial_wavefunc_energies()
            psi0_dic = stg1.get_psi_dic()
            grid_density = np.float64(len(zz_convg)/(zz_convg[-1]-zz_convg[0]))
            ###--------------------------------------------------------------------------------------------------------------
            ### At that point, whether the user chose or not to converge the grid density, we already have all the parameters
            ### required to initialize the system and move forward Stage2
            ###--------------------------------------------------------------------------------------------------------------

        #%% Handlng with the case when the user wants to extend his system. It also distinguish between cases where we have interface and do not have an interface

        if overall_values['-ext_locpot-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            # Extension locpot
            # Chose just multiplication.
            if overall_values['-ex_loc_mul-']:
                if overall_values['-interface-']:
                    print('You told me that you do have an interface. It is going to multiply the whole system just as it is.'
                          ' It makes no sense. I hope you know what you are doing..')
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],
                                   To_plot=True, Has_interface=False,multi_left = overall_values['-ex_loc_left-'], multi_right = overall_values['-ex_loc_right-'])
                    z_temp,v_temp = stg2.current_locpot_vec.T
                    z_temp, v_temp = multiply_z_v_vecs(z_temp,v_temp, multi=overall_values['-ex_loc_multi-'])
                    stg2.elongated_locpot_vec = to_2_column_mat(z_temp, v_temp)
                    stg2.elongated_locpot_vec = stg2.update_converged_spatial_grid(vecor_to_update=stg2.elongated_locpot_vec,
                                                                                   update_converged_vec=False,
                                                                                   update_interface=False)
                elif overall_values['-Range-']:
                    print('You gave me a range. It is going to multiply the whole system just as it is.'
                          ' If you intended to multiply just a certain range within your system,'
                          'it is preferable to choose it manually and then insert it into a position..')
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],
                                   To_plot=True, Has_interface=False,multi_left=overall_values['-ex_loc_multi-'])
                    z_temp,v_temp = stg2.current_locpot_vec.T
                    z_temp, v_temp = multiply_z_v_vecs(z_temp,v_temp, multi=overall_values['-ex_loc_multi-'])
                    stg2.elongated_locpot_vec = to_2_column_mat([z_temp, v_temp])
                    stg2.elongated_locpot_vec = stg2.update_converged_spatial_grid(vecor_to_update=stg2.elongated_locpot_vec,
                                                                                   update_converged_vec=False,
                                                                                   update_interface=False)
                else:
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],
                                   To_plot=True, Has_interface=False,multi_left=overall_values['-ex_loc_multi-'])
                    z_temp,v_temp = stg2.current_locpot_vec.T
                    z_temp, v_temp = multiply_z_v_vecs(z_temp,v_temp, multi=overall_values['-ex_loc_multi-'])
                    stg2.elongated_locpot_vec = to_2_column_mat([z_temp, v_temp])
                    stg2.elongated_locpot_vec = stg2.update_converged_spatial_grid(vecor_to_update=stg2.elongated_locpot_vec,
                                                                                   update_converged_vec=False,
                                                                                   update_interface=False)

            if overall_values['-ex_loc_insert-']:
                # Extension locpot
                # Extension locpot - insertion into position
                # Chose to insert into location. Now it will be divided into two branches -
                # choosing the range manually or let it automatically look for a bulk-like locpot.
                if overall_values['-ex_loc_choose_manu-']:
                    # Extension locpot
                    # Extension locpot - insertion into position
                    # Chose to select the range to be inserted later manually.
                    # we would like to distinguish between the case we have an interface and the
                    # case we do not have an interface.

                    ## if we have an interface - we also distinguish the case for extending from both sides or only one side.
                    if overall_values['-interface-'] and overall_values['-ex_loc_both-']:
                        minima = find_peaks_minima(Locp.locpot_vec[:,0], Locp.locpot_vec[:,1], ignore_local_minima=True)
                        minima_z = cons.A2m(minima[:, 0])
                        minima_v = minima[:, 1]
                        ind_start_left, pos_start_left = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_left_init_pos-'],minima_z)
                        ind_start_left, pos_start_left = find_closest_value_in_array(pos_start_left, cons.A2m(Locp.locpot_vec[:,0]))
                        ind_final_left, pos_final_left = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_left_final_pos-'],minima_z)
                        ind_final_left, pos_final_left = find_closest_value_in_array(pos_final_left, cons.A2m(Locp.locpot_vec[:,0]))
                        ind_start_right, pos_start_right = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_right_init_pos-'],minima_z)
                        ind_start_right, pos_start_right = find_closest_value_in_array(pos_start_right, cons.A2m(Locp.locpot_vec[:,0]))
                        ind_final_right, pos_final_right = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_right_final_pos-'],minima_z)
                        ind_final_right, pos_final_right = find_closest_value_in_array(pos_final_right, cons.A2m(Locp.locpot_vec[:,0]))
                        z_in_left = Locp.locpot_vec[:,0][ind_start_left:ind_final_left]
                        v_in_left = Locp.locpot_vec[:, 1][ind_start_left:ind_final_left]
                        z_in_right = Locp.locpot_vec[:,0][ind_start_right:ind_final_right]
                        v_in_right = Locp.locpot_vec[:, 1][ind_start_right:ind_final_right]
                        z_in_left,v_in_left = fix_potential_edges(z_in_left,v_in_left)
                        z_in_right, v_in_right = fix_potential_edges(z_in_right, v_in_right)
                    else:
                        try:
                            if overall_values['-Range']:
                                temp_locpot_z = np.array([overall_values['-Init_pos-']<=Locp.locpot_vec[:, 0] <= overall_values['-Final_pos-']])
                                temp_locpot_v = np.array([overall_values['-Init_pos-'] <= Locp.locpot_vec[:, 1] <=overall_values['-Final_pos-']])
                                minima = find_peaks_minima(temp_locpot_z, temp_locpot_v,ignore_local_minima=True)
                            else:
                                minima = find_peaks_minima(Locp.locpot_vec[:, 0], Locp.locpot_vec[:, 1],ignore_local_minima=True)
                        except KeyError:
                            minima = find_peaks_minima(Locp.locpot_vec[:, 0], Locp.locpot_vec[:, 1],ignore_local_minima=True)
                        minima_z = cons.A2m(minima[:, 0])
                        minima_v = minima[:, 1]

                        ind_start, pos_start = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_init_pos-'],minima_z)
                        ind_start, pos_start = find_closest_value_in_array(pos_start, cons.A2m(Locp.locpot_vec[:,0]))
                        ind_final, pos_final = find_closest_value_in_array(overall_values['-ex_loc_choose_manu_final_pos-'],minima_z)
                        ind_final, pos_final = find_closest_value_in_array(pos_final, cons.A2m(Locp.locpot_vec[:,0]))
                        z_in = Locp.locpot_vec[:,0][ind_start:ind_final]
                        v_in = Locp.locpot_vec[:, 1][ind_start:ind_final]
                        z_in, v_in = fix_potential_edges(z_in, v_in)



                if overall_values['-interface-']:
                    # Extension locpot
                    # Extension locpot - insertion into position
                    # Defining the sides where the elongation will take place and the factors of multiplications,
                    # for the definition of the stg2 object.
                    if overall_values['-ex_loc_both-']:
                        side = 'both'
                        both_multi = overall_values['-ex_loc_both_multi-']
                        left_multi = 1
                        right_multi = 1
                        manual_multi = both_multi
                    elif overall_values['-ex_loc_right-']:
                        side = 'right'
                        right_multi = overall_values['-ex_loc_right_multi-']
                        left_multi = 1
                        manual_multi = right_multi
                    else:
                        side = 'left'
                        left_multi = overall_values['-ex_loc_left_multi-']
                        right_multi = 1
                        manual_multi = left_multi

                    # Extension locpot
                    # Defining stg2 object. Here we have an interface but we distinguish between the case we also defined a range or not.
                    if overall_values['-Range-']:
                        stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],
                                       To_plot=True, Has_interface=True,multi_left = left_multi, multi_right = right_multi,
                                       limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
                    else:
                         stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=True, To_plot=True,multi_left = left_multi, multi_right = right_multi,
                                       Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])

                    # We have an interface. If the user chose to insert a bulk-like locpot. The insertion location is
                    # found automatically.
                    if overall_values['-ex_loc_bulk_like-']:
                        try:
                            stg2.elongate_interface_potential(from_iteslf = True,side_from_itself = side,
                                            manual = True, multi_manual = manual_multi, interface_position= overall_values['-ref_pos-'],
                                             To_update = True)
                        except KeyError:
                            stg2.elongate_interface_potential(from_iteslf = True,side_from_itself = side,
                                            manual = True, multi_manual = manual_multi,
                                             To_update = True)

                    # We have an interface. If the user chose to insert a manually chose region. The insertion location is
                    # taken from user definition of the regions.
                    elif overall_values['-ex_loc_choose_manu-']:
                        if side == 'both':
                            init_len = cons.m2A(stg2.current_locpot_vec[:, 0][-1])
                            stg2.elongate_interface_potential(from_iteslf=False, side_from_itself='left',
                                                          manual=True, multi_manual=manual_multi,z_in=z_in_left,v_in=v_in_left,
                                                          pos_to_insert=overall_values['-ex_loc_choose_manu_left_init_pos-'], To_update=True)
                            temp_elongated_locpot_vec = to_2_column_mat((stg2.elongated_locpot_vec[:,0],stg2.elongated_locpot_vec[:,1]))
                            differ = temp_elongated_locpot_vec[:, 0][-1] - cons.A2m(init_len)
                            stg2.elongate_interface_potential(from_iteslf=False, side_from_itself='right',z_in=z_in_right,v_in=v_in_right,
                                                          manual=True, multi_manual=manual_multi,
                                                          pos_to_insert=overall_values['-ex_loc_choose_manu_right_init_pos-']+differ,locpot_vector=temp_elongated_locpot_vec,
                                                          To_update=True,original_interface=stg2.new_interface)
                        else:
                            stg2.elongate_interface_potential(from_iteslf=False, side_from_itself=side,z_in=z_in,v_in=v_in,
                                                          manual=True, multi_manual=manual_multi,
                                                          pos_to_insert=overall_values['-ex_loc_choose_manu_init_pos-'], To_update=True)

                else:
                # Extension locpot
                # Extension locpot - insertion into position
                # We dont have an interface
                    side = 'Left'
                    # We dont have an interface. Defining the stg2 object in the cases when the user defined a desired region or not.
                    if overall_values['-Range-']:
                        stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],
                                       Has_interface=False,
                                       limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
                    else:
                        stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=False,
                                       Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])


                    # We dont have an interface. Elongating from bulk-like locpot or from choosing the region manually.
                    if overall_values['-ex_loc_bulk_like-']:
                        stg2.elongate_interface_potential(from_iteslf=True, side_from_itself=side,
                                                          manual=True, multi_manual=overall_values['-ex_loc_multi-'],
                                                          interface_position=overall_values['-ref_pos-'],
                                                          pos_to_insert=overall_values['-ex_loc_insert_pos-'],
                                                          To_update=True)

                    elif overall_values['-ex_loc_choose_manu-']:
                        stg2.elongate_interface_potential(from_iteslf=False, side_from_itself=side,
                                                              manual=True,multi_manual=overall_values['-ex_loc_multi-'], z_in=z_in,v_in=v_in,
                                                              pos_to_insert=overall_values[
                                                                  '-ex_loc_insert_pos-'], To_update=True)

        if overall_values['-ext_locpot-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')) and not overall_values['-interface-']:
            stg2.get_most_relevant_z_coordinate_vec()
            Locp.averaging_along_axis(locpot_vec=stg2.current_locpot_vec, to_plot=True, to_plot_cursor_choice=True)
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Relocate your reference point after extending the local potential vector', size=(100, 1))],
                           [sg.Text(
                               'If you supplied in a previous pop-up window a reference point, please relocate it',
                               size=(100, 1))],
                           [sg.In(default_text=0, size=(20, 1), key='-ref_pos-')],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Relocating Reference Point ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-ref_pos-'] = np.float64(overall_values['-ref_pos-'])
            overall_values['-ref_pos-'] = cons.A2m(overall_values['-ref_pos-'])
            stg2.update_ref_point(overall_values['-ref_pos-'])



        # System Size Convergence Test
        # First - initialize the the wave function to the updated locpot vector
        # initiation of position, automatically or manually?
        if overall_values['-dt-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                           [sg.Text('If you do not have an interface, please choose to locate the initial wave-function manually', size=(100, 1))],
                           [sg.Text(
                               'Do you want it to search for a position automatically or manually supply an initial position?',
                               size=(150, 1))],
                           [sg.Frame('Initial position',
                                     layout=[[sg.Checkbox('automatically', size=(50, 1), key='-z0_auto-')],
                                             [sg.Checkbox('manually', size=(40, 1), key='-z0_manual-')]])],
                           [sg.Text('Where do you want to save you plots?', size=(30, 1)), sg.Input(key='-dt_conv_save_path-'), sg.FileBrowse()],
                           [sg.Text(
                               'If you chose to calculate Transmission coefficient, do you wantt the detemine upper limit of simulation time for the integration?',
                               size=(100, 1))],
                           [sg.In(default_text=0, size=(20, 1), key='-final_time-')],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-dt_conv_save_path-'] = "/".join(list(overall_values['-dt_conv_save_path-'].split('/')[0:-1]))

            # If we have an Interface - Please Locate it
            if overall_values['-interface-']   and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec=stg2.current_locpot_vec, to_plot=True, to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Locate Your Interface ',
                                        size=(100, 1))],
                               [sg.Frame('Interface Position',
                                         layout=[[sg.In(default_text=0, size=(20, 1),
                                                              key='-Interface_pos-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Locating Your Interface Position ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-Interface_pos-'] = np.float64(overall_values['-Interface_pos-'])
                overall_values['-Interface_pos-'] = cons.A2m(overall_values['-Interface_pos-'])
                overall_values = convert_to_type(overall_values)
                ind_interface,pos_interface = find_closest_value_in_array(overall_values['-Interface_pos-'],stg2.current_locpot_vec[:,0])
                stg2.index_new_interface, stg2.new_interface = ind_interface, pos_interface

            # If we chose automatic search for z0 centering - from what side?
            if overall_values['-interface-'] and overall_values['-z0_auto-'] and not overall_values['-z0_manual-'] and \
                    (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('What side of the interface do you want it to be initialized at ', size=(100, 1))],
                               [sg.Frame('Initial position',
                                         layout=[[sg.Checkbox('Left size', size=(40, 1), key='-z0_auto_left_init-')],
                                                 [sg.Checkbox('Right size', size=(40, 1), key='-z0_auto_right_init-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)

            # if you chose to initialize the z0 manually - it would plot the locpot to enable the user to choose the initial
            # position of the z0.
            if overall_values['-z0_manual-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec =stg2.current_locpot_vec,to_plot=True,to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-manual_z0_val-')],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-manual_z0_val-'] = np.float64(overall_values['-manual_z0_val-'])
                overall_values['-manual_z0_val-'] = cons.A2m(overall_values['-manual_z0_val-'])
                overall_values = convert_to_type(overall_values)

            # Handling the manual z0 Value
            if overall_values['-z0_manual-']:
                z0_temp = overall_values['-manual_z0_val-']
            else:
                if overall_values['-z0_auto_left_init-']:
                    side_z0_init = 'Left'
                else:
                    side_z0_init = 'Right'
                z0_temp_ind, z0_temp_pos = stg2.find_initial_position_to_center_psi0(init_side = side_z0_init, manual = False,manual_pos = None, index = False)
                z0_temp = z0_temp_pos
                psi0_dic['z0'] = cons.m2A( z0_temp)


            # # If we would like to converge dt but we didnt converged system size before
            # # In this case we have to initialize z0
            # # How to initialize z0, auto or manually
            # if not overall_values['-sys_size-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            #     not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            #     layout_temp = [[sg.Menu(menu_def, tearoff=True)],
            #                [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
            #                [sg.Text(
            #                    'Do you want it to search for a position automatically or manually supply an initial position?',
            #                    size=(150, 1))],
            #                [sg.Frame('Initial position',
            #                          layout=[[sg.Checkbox('automatically', size=(50, 1), key='-z0_auto-')],
            #                                  [sg.Checkbox('manually', size=(40, 1), key='-z0_manual-')]])],
            #                    [sg.Text('Where do you want to save you plots?', size=(30, 1)),
            #                     sg.Input(key='-dt_conv_save_path-'), sg.FileBrowse()],
            #                [sg.Submit(), sg.Cancel()]]
            #     window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            #     event_temp, values_temp = window_temp.read()
            #     window_temp.close()
            #     overall_values.update(values_temp)
            #     overall_values['-dt_conv_save_path-'] = "/".join(list(overall_values['-dt_conv_save_path-'].split('/')[0:-1]))
            #
            #     # If we have an Interface - Please Locate it
            #     if overall_values['-interface-']   and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            #              not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            #         Locp.averaging_along_axis(locpot_vec=stg2.current_locpot_vec, to_plot=True, to_plot_cursor_choice=True)
            #         layout_temp = [[sg.Menu(menu_def, tearoff=True)],
            #                        [sg.Text('Locate Your Interface ',
            #                                 size=(100, 1))],
            #                        [sg.Frame('Interface Position',
            #                                  layout=[[sg.In(default_text=0, size=(20, 1),
            #                                                       key='-Interface_pos-')]])],
            #                        [sg.Submit(), sg.Cancel()]]
            #         window_temp = sg.Window('Locating Your Interface Position ', layout_temp)
            #         event_temp, values_temp = window_temp.read()
            #         window_temp.close()
            #         overall_values.update(values_temp)
            #         overall_values['-Interface_pos-'] = np.float64(overall_values['-Interface_pos-'])
            #         overall_values['-Interface_pos-'] = cons.A2m(overall_values['-Interface_pos-'])
            #         overall_values = convert_to_type(overall_values)
            #         ind_interface,pos_interface = find_closest_value_in_array(overall_values['-Interface_pos-'],stg2.current_locpot_vec[:,0])
            #         stg2.index_new_interface, stg2.new_interface = ind_interface, pos_interface
            #
            #     # If we chose automatic search for z0 centering - from what side?
            #     if overall_values['-interface-'] and overall_values['-z0_auto-'] and not overall_values['-z0_manual-'] and \
            #             (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            #              not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            #         layout_temp = [[sg.Menu(menu_def, tearoff=True)],
            #                        [sg.Text('What side of the interface do you want it to be initialized at ', size=(100, 1))],
            #                        [sg.Frame('Initial position',
            #                                  layout=[[sg.Checkbox('Left size', size=(40, 1), key='-z0_auto_left_init-')],
            #                                          [sg.Checkbox('Right size', size=(40, 1), key='-z0_auto_right_init-')]])],
            #                        [sg.Submit(), sg.Cancel()]]
            #         window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            #         event_temp, values_temp = window_temp.read()
            #         window_temp.close()
            #         overall_values.update(values_temp)
            #
            #     # if you chose to initialize the z0 manually - it would plot the locpot to enable the user to choose the initial
            #     # position of the z0.
            #     if overall_values['-z0_manual-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            #         not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            #         Locp.averaging_along_axis(locpot_vec =stg2.current_locpot_vec,to_plot=True,to_plot_cursor_choice=True)
            #         layout_temp = [[sg.Menu(menu_def, tearoff=True)],
            #                        [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
            #                        [sg.In(default_text=0, size=(20, 1), key='-manual_z0_val-')],
            #                        [sg.Submit(), sg.Cancel()]]
            #         window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            #         event_temp, values_temp = window_temp.read()
            #         window_temp.close()
            #         overall_values.update(values_temp)
            #         overall_values['-manual_z0_val-'] = np.float64(overall_values['-manual_z0_val-'])
            #         overall_values['-manual_z0_val-'] = cons.A2m(overall_values['-manual_z0_val-'])
            #         overall_values = convert_to_type(overall_values)
            #
            #     # Handling the manual z0 Value
            #     if overall_values['-z0_manual-']:
            #         z0_temp = overall_values['-manual_z0_val-']
            #     else:
            #         if overall_values['-z0_auto_left_init-']:
            #             side_z0_init = 'Left'
            #         else:
            #             side_z0_init = 'Right'
            #         z0_temp_ind, z0_temp_pos = stg2.find_initial_position_to_center_psi0(init_side = side_z0_init, manual = False,manual_pos = None, index = False)
            #         z0_temp = z0_temp_pos
            #         psi0_dic['z0'] = cons.m2A( z0_temp)

            if not overall_values['-ext_locpot-'] and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                    not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                if overall_values['-Range-']:
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'],
                                   dt=overall_values['-initial_dt-'],
                                   To_plot=True, Has_interface=overall_values['-interface-'],
                                   limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
                    stg2.psi0 = stg2.initialize_psi0(manual_center=True, manual_z0=z0_temp, To_update=True,
                                                     manual_psi_dic=psi0_dic)
                    if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                        print('Your initial Wave-function is Not normalized')
                        print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                        stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                                    stg2.psi0, units='Meter')
                else:
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=overall_values['-interface-'], To_plot=True,
                                   Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])
                    stg2.psi0 = stg2.initialize_psi0(manual_center=True, manual_z0=z0_temp, To_update=True,
                                                     manual_psi_dic=psi0_dic)
                    if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                        print('Your initial Wave-function is Not normalized')
                        print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                        stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                                    stg2.psi0, units='Meter')
                if overall_values['-z0_manual-']:
                    if overall_values['-dt_conv_save_path-'] is None or overall_values['-dt_conv_save_path-'] == '':
                        stg2.converge_time_step(manual_center = True,manual_z0 = overall_values['-manual_z0_val-'])
                    else:
                        stg2.converge_time_step(manual_center=True, manual_z0=overall_values['-manual_z0_val-'], path_to_save=overall_values['-dt_conv_save_path-'])
                else:
                    if overall_values['-dt_conv_save_path-'] is None or overall_values['-dt_conv_save_path-'] == '':
                        stg2.converge_time_step()
                    else:
                        stg2.converge_time_step(path_to_save=overall_values['-dt_conv_save_path-'])
            elif overall_values['-dt-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                stg2.psi0 = stg2.initialize_psi0(manual_center=True, manual_z0=z0_temp, To_update=True,
                                                 manual_psi_dic=psi0_dic)
                if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                    print('Your initial Wave-function is Not normalized')
                    print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                    stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                                stg2.psi0, units='Meter')
                if overall_values['-dt_conv_save_path-'] is None or overall_values['-dt_conv_save_path-'] == '':
                    stg2.converge_time_step()
                else:
                    stg2.converge_time_step(path_to_save=overall_values['-dt_conv_save_path-'])

        # Handling the dt convergence test:
        # -------------------------------------------------------------
        # -------------------------------------------------------------
            iteration = 1
            while True:
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Do you satisfy with the convergence results? Please answer [y/n]', size=(60, 1))],
                               [sg.Yes(), sg.No(), sg.Cancel()]]
                window_temp = sg.Window('Time step convergence check ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                if event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel':
                    break
                elif event_temp == 'Yes':
                    sg.popup_ok('Press Ok the continue')
                    break
                elif event_temp == 'No':
                    layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                   [sg.Text('How do you want to procceed?', size=(60, 1))],
                                   [sg.Frame('Options',
                                             layout=[[sg.Checkbox('Elongate the system', size=(15, 1),
                                                                  key='-sys_size_elongate_system-')],
                                                     [sg.Text(
                                                         'From what side, please write exactly [Right/Left]. Only when you have an interface',
                                                         size=(50, 1)),
                                                         sg.In(key='-sys_size_elongate_side-', size=(10, 1))],
                                                     [sg.Text(
                                                         'If you selected to elonagte your system, please supply the position you want to insert the additional locpot'),
                                                         sg.In(key='-sys_size_elongate_position-', size=(10, 1))],
                                                     [sg.Text('And how many times'),
                                                      sg.In(default_text=10, key='-sys_size_elongate_multi-',
                                                            size=(20, 1))],
                                                     [sg.Text('What would you like to insert')],
                                                     [sg.Checkbox('Bulk-Like Locpot',
                                                                  key='-sys_size_elongate_from_itself-')],
                                                     [sg.Text("")],
                                                     [sg.Text("Or you can choose other options:")],
                                                     [sg.Checkbox('Decreasing initial dt', size=(20, 1),
                                                                  key='-sys_size_decr_dt-')],
                                                     [sg.Text(
                                                         'If selected, give the value you wish in seconds. Scale of Fsec',
                                                         size=(50, 1)),
                                                         sg.In(key='-sys_size_dec_dt_value-', size=(10, 1))],
                                                     [sg.Checkbox(
                                                         'Increasing interations. The initial maximal number of iteration was 15',
                                                         size=(50, 1),
                                                         key='-sys_size_incr_iterations-')],
                                                     [sg.Text('If selected, give the value of iterations you want',
                                                              size=(50, 1)),
                                                      sg.In(key='-sys_size_incr_iterations_value-', size=(10, 1))]])],
                                   [sg.Submit(), sg.Cancel()]]
                    window_temp = sg.Window('Time Step convergence check ', layout_temp)
                    event_temp, values_temp = window_temp.read()
                    window_temp.close()
                    overall_values.update(values_temp)
                    if overall_values['-sys_size_elongate_system-']:
                        if overall_values['-interface-']:
                            stg2.elongate_interface_potential(from_iteslf=overall_values['-sys_size_elongate_from_itself-'],
                                                              side_from_itself=overall_values['-sys_size_elongate_side-'],
                                                              manual=not overall_values[
                                                                  '-sys_size_elongate_from_external-'],
                                                              multi_manual=overall_values['-sys_size_elongate_multi-'],
                                                              pos_to_insert=overall_values['-sys_size_elongate_position-'],
                                                              locpot_vector=None, To_update=True)
                            if overall_values['-dt_conv_save_path-'] is None or overall_values[
                                '-dt_conv_save_path-'] == '':
                                stg2.converge_time_step()
                            else:
                                stg2.converge_time_step(path_to_save = "/".join(list(os.path.join(overall_values['-dt_conv_save_path-'], str(iteration)).split("\\"))))

                        else:
                            stg2.elongate_interface_potential(from_iteslf=overall_values['-sys_size_elongate_from_itself-'],
                                                              manual=overall_values['-sys_size_elongate_from_itself-'],
                                                              multi_manual=overall_values['-sys_size_elongate_multi-'],
                                                              pos_to_insert=overall_values['-sys_size_elongate_position-'],
                                                              locpot_vector=None, To_update=True)
                            if overall_values['-dt_conv_save_path-'] is None or overall_values[
                                '-dt_conv_save_path-'] == '':
                                stg2.converge_time_step()
                            else:
                                stg2.converge_time_step(
                                    path_to_save="/".join(list(os.path.join(overall_values['-dt_conv_save_path-'], str(iteration)).split("\\"))))
                    if overall_values['-sys_size_decr_dt-']:
                        overall_values['-sys_size_dec_dt_value-'] = np.float64(overall_values['-sys_size_dec_dt_value-'])
                        stg2.dt = cons.fs2sec(overall_values['-sys_size_dec_dt_value-'])
                    if overall_values['-sys_size_incr_iterations-']:
                        overall_values['-sys_size_incr_iterations_value-'] = np.float64(
                            overall_values['-sys_size_incr_iterations_value-'])
                        if overall_values['-dt_conv_save_path-'] is None or overall_values[
                            '-dt_conv_save_path-'] == '':
                            stg2.converge_time_step(iterations=overall_values['-sys_size_incr_iterations_value-'])
                        else:
                            stg2.converge_time_step(iterations=overall_values['-sys_size_incr_iterations_value-'],path_to_save="/".join(list(os.path.join(overall_values['-dt_conv_save_path-'], str(iteration)).split("\\"))))
                    else:
                        if overall_values['-dt_conv_save_path-'] is None or overall_values[
                            '-dt_conv_save_path-'] == '':
                            stg2.converge_time_step()
                        else:
                            stg2.converge_time_step(
                                path_to_save="/".join(list(os.path.join(overall_values['-dt_conv_save_path-'], str(iteration)).split("\\"))))
                itertion =+1

        if (overall_values['-sys_size-']) and not (overall_values['-dt-']) and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                           [sg.Text(
                               'Do you want it to search for a position automatically or manually supply an initial position?',
                               size=(150, 1))],
                           [sg.Text(
                               'If you do not have an interface, please choose to locate the initial wave-function manually',
                               size=(100, 1))],
                           [sg.Frame('Initial position',
                                     layout=[[sg.Checkbox('automatically', size=(50, 1), key='-z0_auto-')],
                                             [sg.Checkbox('manually', size=(40, 1), key='-z0_manual-')]])],
                           [sg.Text('Where do you want to save you plots?', size=(30, 1)), sg.Input(key='-sys_size_save_path-'), sg.FileBrowse()],
                           [sg.Text(
                               'If you chose to calculate Transmission coefficient, do you wantt the detemine upper limit of simulation time for the integration?',
                               size=(100, 1))],
                           [sg.In(default_text=0, size=(20, 1), key='-final_time-')],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-sys_size_save_path-'] = "/".join(list(overall_values['-sys_size_save_path-'].split('/')[0:-1]))

            # If we have an Interface - Please Locate it
            if overall_values['-interface-']   and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec=stg2.current_locpot_vec, to_plot=True, to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Locate Your Interface ',
                                        size=(100, 1))],
                               [sg.Frame('Interface Position',
                                         layout=[[sg.In(default_text=0, size=(20, 1),
                                                              key='-Interface_pos-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Locating Your Interface Position ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-Interface_pos-'] = np.float64(overall_values['-Interface_pos-'])
                overall_values['-Interface_pos-'] = cons.A2m(overall_values['-Interface_pos-'])
                overall_values = convert_to_type(overall_values)
                ind_interface,pos_interface = find_closest_value_in_array(overall_values['-Interface_pos-'],stg2.current_locpot_vec[:,0])
                stg2.index_new_interface, stg2.new_interface = ind_interface, pos_interface

            # If we chose automatic search for z0 centering - from what side?
            if overall_values['-interface-'] and overall_values['-z0_auto-'] and not overall_values['-z0_manual-'] and \
                    (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('What side of the interface do you want it to be initialized at ', size=(100, 1))],
                               [sg.Frame('Initial position',
                                         layout=[[sg.Checkbox('Left size', size=(40, 1), key='-z0_auto_left_init-')],
                                                 [sg.Checkbox('Right size', size=(40, 1), key='-z0_auto_right_init-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)

            # if you chose to initialize the z0 manually - it would plot the locpot to enable the user to choose the initial
            # position of the z0.
            if overall_values['-z0_manual-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec =stg2.current_locpot_vec,to_plot=True,to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-manual_z0_val-')],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-manual_z0_val-'] = np.float64(overall_values['-manual_z0_val-'])
                overall_values['-manual_z0_val-'] = cons.A2m(overall_values['-manual_z0_val-'])
                overall_values = convert_to_type(overall_values)

            # Handling the manual z0 Value
            if overall_values['-z0_manual-']:
                z0_temp = overall_values['-manual_z0_val-']
            else:
                if overall_values['-z0_auto_left_init-']:
                    side_z0_init = 'Left'
                else:
                    side_z0_init = 'Right'
                z0_temp_ind, z0_temp_pos = stg2.find_initial_position_to_center_psi0(init_side = side_z0_init, manual = False,manual_pos = None, index = False)
                z0_temp = z0_temp_pos
                psi0_dic['z0'] = cons.m2A( z0_temp)

            # If we already did system time step test and the pop-up window of initializtion already apeared.
            # This is just to let the user choose where to save his figures.
        elif overall_values['-sys_size-'] and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                                             not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Where do you want to save your plots', size=(100, 1))],
                           [sg.Text(
                               'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                               size=(100, 1)),
                            sg.Input(key='-sys_size_save_path-'), sg.FileBrowse()],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Where do you want to save your plots', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)
            overall_values['-sys_size_save_path-'] = "/".join(
                list(overall_values['-sys_size_save_path-'].split('/')[0:-1]))

        if overall_values['-sys_size-'] and not (overall_values['-dt-'] or overall_values['-ext_locpot-']) and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if overall_values['-Range-']:
                stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'],
                               dt=overall_values['-initial_dt-'],
                               To_plot=True, Has_interface=overall_values['-interface-'],
                               limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
                stg2.psi0 = stg2.initialize_psi0(manual_center = True,manual_z0 =z0_temp,To_update = True, manual_psi_dic=psi0_dic)
                if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                    print('Your initial Wave-function is Not normalized')
                    print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                    stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                                stg2.psi0, units='Meter')
            else:
                stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=overall_values['-interface-'], To_plot=True,
                               Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])
                stg2.psi0 = stg2.initialize_psi0(manual_center = True,manual_z0 =z0_temp,To_update = True, manual_psi_dic=psi0_dic)
                if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                    print('Your initial Wave-function is Not normalized')
                    print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                    stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                                stg2.psi0, units='Meter')
            if overall_values['-z0_manual-']:
                if not overall_values['-sys_size_save_path-'] is None or not overall_values['-sys_size_save_path-'] == '':
                    stg2.converge_system_size(manual_center = True,manual_z0 = overall_values['-manual_z0_val-'],path_to_save=overall_values['-sys_size_save_path-'])
                else:
                    stg2.converge_system_size(manual_center=True, manual_z0=overall_values['-manual_z0_val-'])
            else:
                if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                                 '-sys_size_save_path-'] == '':
                    stg2.converge_system_size(path_to_save=overall_values['-sys_size_save_path-'])
                else:
                    stg2.converge_system_size()
        elif overall_values['-sys_size-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            stg2.psi0 = stg2.initialize_psi0(manual_center=True, manual_z0=z0_temp, To_update=True,
                                             manual_psi_dic=psi0_dic)
            if not is_normalized(cons.A2m(stg2.current_locpot_vec[:, 0]), stg2.psi0):
                print('Your initial Wave-function is Not normalized')
                print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:, 0])))
                stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:, 0],
                                                                            stg2.psi0, units='Meter')
            if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                             '-sys_size_save_path-'] == '':
                stg2.converge_system_size(path_to_save=overall_values['-sys_size_save_path-'])
            else:
                stg2.converge_system_size()
        # Handling system size convergence
        # ------------------------------------------------------
        # ------------------------------------------------------
            iteration = 1
            while True:
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                      [sg.Text('Do you satisfy with the convergence results? Please answer [y/n]', size=(60, 1))],
                      [sg.Yes(), sg.No(), sg.Cancel()]]
                window_temp = sg.Window('System size convergence check ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                if event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel':
                    break
                elif event_temp == 'Yes':
                    sg.popup_ok('Press Ok the continue')
                    break
                elif event_temp == 'No':
                    layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                   [sg.Text('How do you want to procceed?', size=(60, 1))],
                                   [sg.Frame('Options',
                                            layout=[[sg.Checkbox('Elongate the system', size=(15, 1),
                                                                 key='-sys_size_elongate_system-')],
                                                     [sg.Text(
                                                         'From what side, please write exactly [Right/Left]. Only when you have an interface',
                                                         size=(50, 1)), sg.In(key='-sys_size_elongate_side-',size=(10,1))],
                                                    [sg.Text(
                                                        'If you selected to elonagte your system, please supply the position you want to insert the additional locpot'),
                                                        sg.In(key='-sys_size_elongate_position-',size=(10,1))],
                                                    [sg.Text('And how many times'),
                                                     sg.In(default_text=10, key='-sys_size_elongate_multi-',size=(20,1))],
                                                    [sg.Text('What would you like to insert')],
                                                    [sg.Checkbox('Bulk-Like Locpot',
                                                                 key='-sys_size_elongate_from_itself-')],
                                                    [sg.Text("")],
                                                    [sg.Text("Or you can choose other options:")],
                                                    [sg.Checkbox('Decreasing initial dt', size=(20, 1),
                                                                 key='-sys_size_decr_dt-')],
                                                     [sg.Text(
                                                         'If selected, give the value you wish in seconds. Scale of Fsec',
                                                         size=(50, 1)),
                                                     sg.In(key='-sys_size_dec_dt_value-',size=(10,1))],
                                                    [sg.Checkbox(
                                                        'Increasing interations. The initial maximal number of iteration was 15',
                                                        size=(50, 1),
                                                        key='-sys_size_incr_iterations-')],
                                                     [sg.Text('If selected, give the value of iterations you want',
                                                             size=(50, 1)),
                                                     sg.In(key='-sys_size_incr_iterations_value-',size=(10,1))]])],
                                                     [sg.Submit(), sg.Cancel()]]
                    window_temp = sg.Window('System size convergence check ', layout_temp)
                    event_temp, values_temp = window_temp.read()
                    window_temp.close()
                    overall_values.update(values_temp)
                    if overall_values['-sys_size_elongate_system-']:
                        if overall_values['-interface-']:
                            stg2.elongate_interface_potential(from_iteslf=overall_values['-sys_size_elongate_from_itself-'],
                                                              side_from_itself=overall_values['-sys_size_elongate_side-'],
                                                              manual=True, multi_manual=overall_values['-sys_size_elongate_multi-'],
                                                              pos_to_insert=overall_values['-sys_size_elongate_position-'],
                                                              locpot_vector=None, To_update=True)
                            if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                                             '-sys_size_save_path-'] == '':
                                stg2.converge_system_size(path_to_save="/".join(list(os.path.join(overall_values['-sys_size_save_path-'], str(iteration)).split("\\"))))
                            else:
                                stg2.converge_system_size()
                        else:
                            stg2.elongate_interface_potential(from_iteslf=overall_values['-sys_size_elongate_from_itself-'],
                                                              manual=True, multi_manual=overall_values['-sys_size_elongate_multi-'],
                                                              pos_to_insert=overall_values['-sys_size_elongate_position-'],
                                                              locpot_vector=None, To_update=True)
                            if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                                             '-sys_size_save_path-'] == '':
                                stg2.converge_system_size(path_to_save="/".join(list(os.path.join(overall_values['-sys_size_save_path-'], str(iteration)).split("\\"))))
                            else:
                                stg2.converge_system_size()
                    if overall_values['-sys_size_decr_dt-']:
                        overall_values['-sys_size_dec_dt_value-'] = np.float64(overall_values['-sys_size_dec_dt_value-'])
                        stg2.dt = cons.fs2sec(overall_values['-sys_size_dec_dt_value-'])
                    if overall_values['-sys_size_incr_iterations-']:
                        overall_values['-sys_size_incr_iterations_value-'] = np.float64(overall_values['-sys_size_incr_iterations_value-'])
                        if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                                         '-sys_size_save_path-'] == '':
                            stg2.converge_system_size(iteration_num=overall_values['-sys_size_incr_iterations_value-'],path_to_save="/".join(list(os.path.join(overall_values['-sys_size_save_path-'], str(iteration)).split("\\"))))
                        else:
                            stg2.converge_system_size(iteration_num=overall_values['-sys_size_incr_iterations_value-'])

                    else:
                        if not overall_values['-sys_size_save_path-'] is None or not overall_values[
                                                                                         '-sys_size_save_path-'] == '':
                            stg2.converge_system_size(path_to_save="/".join(list(os.path.join(overall_values['-sys_size_save_path-'], str(iteration)).split("\\"))))
                        else:
                            stg2.converge_system_size()
                iteration +=1
        # ------------------------------------------------------
        # ------------------------------------------------------

        # Handling Case when dt convergence test is desired
        # dt convergence test


        # -------------------------------------------------------------
        # -------------------------------------------------------------



        if overall_values['-Pr_avg_locpot-'] and (overall_values['-ext_locpot-'] or overall_values['-sys_size-']) and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            fig, axs = plt.subplots(1, 1)
            fig.add_subplot(111, frameon=False)
            stg2.get_most_relevant_z_coordinate_vec()
            axs.plot(stg2.current_locpot_vec[:,0],stg2.current_locpot_vec[:,1], label='Local Potential')
            axs.grid()
            axis_dic = {0: 'X', 1: 'Y', 2: 'Z'}
            plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
            plt.xlabel('{} axis in Angstrum'.format(axis_dic[axis]))
            plt.ylabel('Electrostatic potential in eV, V({})'.format(axis_dic[axis]))
            fig.legend(labelspacing=3, fontsize='large', handletextpad=3, loc='lower right')

            fig.tight_layout()
            fig.show()
            fig.savefig('1D potential along axis {}'.format(axis_dic[axis]))

        elif overall_values['-Pr_avg_locpot-'] and not (overall_values['-ext_locpot-']  or overall_values['-sys_size-']) and overall_values['-density-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            fig, axs = plt.subplots(1, 1)
            fig.add_subplot(111, frameon=False)
            axs.plot(zz_convg, vv_convg, label='Local Potential')
            axs.grid()
            axis_dic = {0: 'X', 1: 'Y', 2: 'Z'}
            plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
            plt.xlabel('{} axis in Angstrum'.format(axis_dic[axis]))
            plt.ylabel('Electrostatic potential in eV, V({})'.format(axis_dic[axis]))
            fig.legend(labelspacing=3, fontsize='large', handletextpad=3, loc='lower right')

            fig.tight_layout()
            fig.show()
            fig.savefig('1D potential along axis {}'.format(axis_dic[axis]))

        elif overall_values['-Pr_avg_locpot-'] and not overall_values['-ext_locpot-'] and not overall_values['-density-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            Locp.averaging_along_axis(to_plot=True)

    # Handling the rest of the options:
    # Full propagation
    # Cumulative Probabilty
    # Transmission Coefficient
        # Initializing Stage_2 If it was not initialized till here.
        try:
            stg2
        except NameError:
            if overall_values['-Range-']:
                try:
                    if not (overall_values['-ref_pos-'] is None or overall_values['-ref_pos-'] == 0):
                         stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'],
                               dt=overall_values['-initial_dt-'],
                               To_plot=True, Has_interface=overall_values['-interface-'],
                               limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']],ref_point =  overall_values['-ref_pos-'])
                    else:
                        stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'],
                               dt=overall_values['-initial_dt-'],
                               To_plot=True, Has_interface=overall_values['-interface-'],
                               limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
                except KeyError:
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Nt=overall_values['-Nt-'],
                                   dt=overall_values['-initial_dt-'],
                                   To_plot=True, Has_interface=overall_values['-interface-'],
                                   limits_for_itself=[overall_values['-Initi_pos-'], overall_values['-Final_pos-']])
            else:
                try:
                    if not (overall_values['-ref_pos-'] is None or  overall_values['-ref_pos-'] == 0):
                         stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=overall_values['-interface-'], To_plot=True,
                                   Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'],ref_point =  overall_values['-ref_pos-'] )
                    else:
                        stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=overall_values['-interface-'], To_plot=True,
                               Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])
                except KeyError:
                    stg2 = Stage_2(Locp, grid_density, psi0_dic, Has_interface=overall_values['-interface-'],
                                   To_plot=True,
                                   Nt=overall_values['-Nt-'], dt=overall_values['-initial_dt-'])

        # initiation of position, automatically or manually?
        if (overall_values['-Full_prop-'] or overall_values['-Trans_coeff-'] or overall_values['-cum_prob-'] ) and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')) and not (overall_values['-dt-'] or overall_values['-sys_size-']):
            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                           [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                           [sg.Text(
                               'Do you want it to search for a position automatically or manually supply an initial position?',
                               size=(150, 1))],
                           [sg.Text(
                               'If you do not have an interface, please choose to initialize the wave-function manually',
                               size=(150, 1))],
                           [sg.Frame('Initial position',
                                     layout=[[sg.Checkbox('automatically', size=(50, 1), key='-z0_auto-')],
                                             [sg.Checkbox('manually', size=(40, 1), key='-z0_manual-')]])],
                           [sg.Text('If you chose to calculate Transmission coefficient, do you wantt the detemine upper limit of simulation time for the integration?', size=(100, 1))],
                           [sg.In(default_text=0, size=(20, 1),key='-final_time-')],
                           [sg.Submit(), sg.Cancel()]]
            window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
            event_temp, values_temp = window_temp.read()
            window_temp.close()
            overall_values.update(values_temp)

            # If we have an Interface - Please Locate it
            if overall_values['-interface-']   and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec=stg2.current_locpot_vec, to_plot=True, to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Locate Your Interface ',
                                        size=(100, 1))],
                               [sg.Frame('Interface Position',
                                         layout=[[sg.In(default_text=0, size=(20, 1),
                                                              key='-Interface_pos-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Locating Your Interface Position ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-Interface_pos-'] = np.float64(overall_values['-Interface_pos-'])
                overall_values['-Interface_pos-'] = cons.A2m(overall_values['-Interface_pos-'])
                overall_values = convert_to_type(overall_values)
                ind_interface,pos_interface = find_closest_value_in_array(overall_values['-Interface_pos-'],stg2.current_locpot_vec[:,0])
                stg2.index_new_interface, stg2.new_interface = ind_interface, pos_interface

            # If we chose automatic search for z0 centering - from what side?
            if overall_values['-interface-'] and overall_values['-z0_auto-'] and not overall_values['-z0_manual-'] and \
                    (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                     not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('What side of the interface do you want it to be initialized at ', size=(100, 1))],
                               [sg.Frame('Initial position',
                                         layout=[[sg.Checkbox('Left size', size=(40, 1), key='-z0_auto_left_init-')],
                                                 [sg.Checkbox('Right size', size=(40, 1), key='-z0_auto_right_init-')]])],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)

            # if you chose to initialize the z0 manually - it would plot the locpot to enable the user to choose the initial
            # position of the z0.
            if overall_values['-z0_manual-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                Locp.averaging_along_axis(locpot_vec =stg2.current_locpot_vec,to_plot=True,to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Where do you want to initialize you wave function', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-manual_z0_val-')],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Initiation position of the wave-function ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-manual_z0_val-'] = np.float64(overall_values['-manual_z0_val-'])
                overall_values['-manual_z0_val-'] = cons.A2m(overall_values['-manual_z0_val-'])
                overall_values = convert_to_type(overall_values)

            if overall_values['-z0_manual-']:
                z0_temp = overall_values['-manual_z0_val-']
            else:
                if overall_values['-z0_auto_left_init-']:
                    side_z0_init = 'Left'
                else:
                    side_z0_init = 'Right'
                z0_temp_ind, z0_temp_pos = stg2.find_initial_position_to_center_psi0(init_side = side_z0_init, manual = False,manual_pos = None, index = False)
                z0_temp = z0_temp_pos
            stg2.psi0 = stg2.initialize_psi0(manual_center = True,manual_z0 = z0_temp, To_update = True, manual_psi_dic=psi0_dic)
            if not is_normalized(cons.A2m(stg2.current_locpot_vec[:,0]),stg2.psi0):
                print('Your initial Wave-function is Not normalized')
                print(np.real(np.trapz(stg2.psi0 * np.conj(stg2.psi0), stg2.current_locpot_vec[:,0])))
                stg2.psi0 = stg2.psi0 * normalize_wave_function_numerically(stg2.current_locpot_vec[:,0], stg2.psi0, units='Meter')
        path_to_save = ''
        if overall_values['-Full_prop-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            try:
                results_full_prop = stg2.propagate_psi(path_to_save=overall_values['-sys_size_save_path-'])
                path_to_save = overall_values['-sys_size_save_path-']
            except KeyError:
                try:
                    results_full_prop = stg2.propagate_psi(path_to_save=overall_values['-dt_conv_save_path-'])
                    path_to_save = overall_values['-dt_conv_save_path-']
                except KeyError:
                    layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                   [sg.Text('Where do you want to save your Animation?', size=(100, 1))],
                                   [sg.Text(
                                       'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                       size=(100, 1)),
                                    sg.Input(key='-ani_save_path-'), sg.FileBrowse()],
                                   [sg.Submit(), sg.Cancel()]]
                    window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                    event_temp, values_temp = window_temp.read()
                    window_temp.close()
                    overall_values.update(values_temp)
                    overall_values['-ani_save_path-'] = "/".join(list(overall_values['-ani_save_path-'].split('/')[0:-1]))
                    results_full_prop = stg2.propagate_psi(path_to_save=overall_values['-ani_save_path-'])
                    path_to_save = overall_values['-ani_save_path-']
        if overall_values['-Trans_coeff-'] and (not(event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
            not(event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            z = stg2.current_locpot_vec[:, 0]
            z = cons.A2m(z)
            kk = to_1D_vec(create_k_grid(len(z), z[-1] - z[0]))
            kk = to_1D_vec(kk)
            try:
                if not (overall_values['-final_time-'] == 0 or  overall_values['-final_time-'] == '0'  or overall_values['-final_time-'] is None):
                    final_time = np.float64(overall_values['-final_time-'])
                else:
                    final_time = 0
            except KeyError:
                final_time = 0
            if overall_values['-Range-'] or not overall_values['-interface-']:
                try:
                    results_Trans = transmision_coeff(stg2.psi0,stg2.Nt,stg2.dt,stg2.current_locpot_vec[:,1],stg2.current_locpot_vec[:,0],kk,overall_values['-ref_pos-'],path_to_save=overall_values['-sys_size_save_path-'],final_time=final_time)
                    path_to_save = overall_values['-sys_size_save_path-']
                except KeyError:
                    try:
                        results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt, stg2.current_locpot_vec[:, 1],
                                                          stg2.current_locpot_vec[:, 0], kk, overall_values['-ref_pos-'],
                                                          path_to_save=overall_values['-dt_conv_save_path-'],final_time=final_time)
                        path_to_save = overall_values['-dt_conv_save_path-']
                    except KeyError:
                        try:
                            results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt,
                                                              stg2.current_locpot_vec[:, 1],
                                                              stg2.current_locpot_vec[:, 0], kk,
                                                              overall_values['-ref_pos-'],
                                                              path_to_save=overall_values['-ani_save_path-'],final_time=final_time)
                            path_to_save = overall_values['-ani_save_path-']
                        except KeyError:
                            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                           [sg.Text('Where do you want to save your plot?', size=(100, 1))],
                                           [sg.Text(
                                               'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                               size=(100, 1)),
                                               sg.Input(key='-trans_coe_save_path-'), sg.FileBrowse()],
                                           [sg.Submit(), sg.Cancel()]]
                            window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                            event_temp, values_temp = window_temp.read()
                            window_temp.close()
                            overall_values.update(values_temp)
                            overall_values['-trans_coe_save_path-'] = "/".join(
                                list(overall_values['-trans_coe_save_path-'].split('/')[0:-1]))
                            results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt, stg2.current_locpot_vec[:, 1],
                                                              stg2.current_locpot_vec[:, 0], kk, overall_values['-ref_pos-'],
                                                              path_to_save=overall_values['-trans_coe_save_path-'],final_time=final_time)
                            path_to_save = overall_values['-trans_coe_save_path-']

            else:
                try:
                    results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt, stg2.current_locpot_vec[:, 1],
                                                      stg2.current_locpot_vec[:, 0], kk, stg2.new_interface,path_to_save=overall_values['-sys_size_save_path-'],final_time = final_time)
                    path_to_save = overall_values['-sys_size_save_path-']
                except KeyError:
                    try:
                        results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt, stg2.current_locpot_vec[:, 1],
                                                          stg2.current_locpot_vec[:, 0], kk, stg2.new_interface,
                                                          path_to_save=overall_values['-dt_conv_save_path-'],final_time = final_time)
                        path_to_save = overall_values['-dt_conv_save_path-']
                    except KeyError:
                        try:
                            results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt,
                                                              stg2.current_locpot_vec[:, 1],
                                                              stg2.current_locpot_vec[:, 0], kk, stg2.new_interface,
                                                              path_to_save=overall_values['-ani_save_path-'],final_time = final_time)
                            path_to_save = overall_values['-ani_save_path-']
                        except KeyError:
                            layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                           [sg.Text('Where do you want to save your plot?', size=(100, 1))],
                                           [sg.Text(
                                               'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                               size=(100, 1)),
                                               sg.Input(key='-trans_coe_save_path-'), sg.FileBrowse()],
                                           [sg.Submit(), sg.Cancel()]]
                            window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                            event_temp, values_temp = window_temp.read()
                            window_temp.close()
                            overall_values.update(values_temp)
                            overall_values['-trans_coe_save_path-'] = "/".join(
                                list(overall_values['-trans_coe_save_path-'].split('/')[0:-1]))
                            results_Trans = transmision_coeff(stg2.psi0, stg2.Nt, stg2.dt, stg2.current_locpot_vec[:, 1],
                                                              stg2.current_locpot_vec[:, 0], kk, stg2.new_interface,
                                                              path_to_save=overall_values['-trans_coe_save_path-'],final_time = final_time)
                            path_to_save = overall_values['-trans_coe_save_path-']


        if overall_values['-cum_prob-'] and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
            if overall_values['-Range-']:
                try:
                    results_cum_prob = stg2.cumulative_probabilty_through_interface(
                        check_pos=overall_values['-ref_pos-'],path_to_save=overall_values['-sys_size_save_path-'])
                    path_to_save = overall_values['-sys_size_save_path-']
                except KeyError:
                    try:
                        results_cum_prob = stg2.cumulative_probabilty_through_interface(
                            check_pos=overall_values['-ref_pos-'], path_to_save=overall_values['-dt_conv_save_path-'])
                        path_to_save = overall_values['-dt_conv_save_path-']
                    except KeyError:
                        try:
                            results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                check_pos=overall_values['-ref_pos-'],
                                path_to_save=overall_values['-ani_save_path-'])
                            path_to_save = overall_values['-ani_save_path-']
                        except KeyError:
                            try:
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                    check_pos=overall_values['-ref_pos-'],
                                    path_to_save=overall_values['-trans_coe_save_path-'])
                                path_to_save = overall_values['-trans_coe_save_path-']
                            except KeyError:
                                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                               [sg.Text('Where do you want to save your plot?', size=(100, 1))],
                                               [sg.Text(
                                                   'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                                   size=(100, 1)),
                                                   sg.Input(key='-cum_prob_save_path-'), sg.FileBrowse()],
                                               [sg.Submit(), sg.Cancel()]]
                                window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                                event_temp, values_temp = window_temp.read()
                                window_temp.close()
                                overall_values.update(values_temp)
                                overall_values['-cum_prob_save_path-'] = "/".join(
                                    list(overall_values['-cum_prob_save_path-'].split('/')[0:-1]))
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                    check_pos=overall_values['-ref_pos-'], path_to_save=overall_values['-cum_prob_save_path-'])
                                path_to_save = overall_values['-cum_prob_save_path-']
            elif overall_values['-interface-']:
                try:
                    results_cum_prob = stg2.cumulative_probabilty_through_interface(path_to_save=overall_values['-sys_size_save_path-'])
                    path_to_save = overall_values['-sys_size_save_path-']
                except KeyError:
                    try:
                        results_cum_prob = stg2.cumulative_probabilty_through_interface(path_to_save=overall_values['-dt_conv_save_path-'])
                        path_to_save = overall_values['-dt_conv_save_path-']
                    except KeyError:
                        try:
                            results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                path_to_save=overall_values['-ani_save_path-'])
                            path_to_save = overall_values['-ani_save_path-']
                        except KeyError:
                            try:
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                    path_to_save=overall_values['-trans_coe_save_path-'])
                                path_to_save = overall_values['-trans_coe_save_path-']
                            except KeyError:
                                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                               [sg.Text('Where do you want to save your plot?', size=(100, 1))],
                                               [sg.Text(
                                                   'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                                   size=(100, 1)),
                                                   sg.Input(key='-cum_prob_save_path-'), sg.FileBrowse()],
                                               [sg.Submit(), sg.Cancel()]]
                                window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                                event_temp, values_temp = window_temp.read()
                                window_temp.close()
                                overall_values.update(values_temp)
                                overall_values['-cum_prob_save_path-'] = "/".join(
                                    list(overall_values['-cum_prob_save_path-'].split('/')[0:-1]))
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(path_to_save=overall_values['-cum_prob_save_path-'])
                                path_to_save = overall_values['-cum_prob_save_path-']
            else:
                try:
                    results_cum_prob = stg2.cumulative_probabilty_through_interface(
                        check_pos=overall_values['-ref_pos-'],path_to_save=overall_values['-sys_size_save_path-'])
                    path_to_save = overall_values['-sys_size_save_path-']
                except KeyError:
                    try:
                        results_cum_prob = stg2.cumulative_probabilty_through_interface(
                            check_pos=overall_values['-ref_pos-'], path_to_save=overall_values['-dt_conv_save_path-'])
                        path_to_save = overall_values['-dt_conv_save_path-']
                    except KeyError:
                        try:
                            results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                check_pos=overall_values['-ref_pos-'],
                                path_to_save=overall_values['-ani_save_path-'])
                            path_to_save = overall_values['-ani_save_path-']
                        except KeyError:
                            try:
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                    check_pos=overall_values['-ref_pos-'],
                                    path_to_save=overall_values['-trans_coe_save_path-'])
                                path_to_save = overall_values['-trans_coe_save_path-']
                            except KeyError:
                                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                               [sg.Text('Where do you want to save your plot?', size=(100, 1))],
                                               [sg.Text(
                                                   'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                                   size=(100, 1)),
                                                   sg.Input(key='-cum_prob_save_path-'), sg.FileBrowse()],
                                               [sg.Submit(), sg.Cancel()]]
                                window_temp = sg.Window('Where do you want to save your plots', layout_temp)
                                event_temp, values_temp = window_temp.read()
                                window_temp.close()
                                overall_values.update(values_temp)
                                overall_values['-cum_prob_save_path-'] = "/".join(
                                    list(overall_values['-cum_prob_save_path-'].split('/')[0:-1]))
                                results_cum_prob = stg2.cumulative_probabilty_through_interface(
                                    check_pos=overall_values['-ref_pos-'], path_to_save=overall_values['-cum_prob_save_path-'])
                                path_to_save = overall_values['-cum_prob_save_path-']
        try:
            if overall_values['-modeling_interface-'] and (not (event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel') or \
                    not (event_temp == sg.WIN_CLOSED or event_temp == 'Exit' or event_temp == 'Cancel')):
                if path_to_save == '' :
                    layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                                   [sg.Text('Where do you want to save interface modeling?', size=(100, 1))],
                                   [sg.Text(
                                       'Please browse the desired location. Enter the directory and choose any random file just to get the path',
                                       size=(100, 1)),
                                       sg.Input(key='-interface_model_save_path-'), sg.FileBrowse()],
                                   [sg.Submit(), sg.Cancel()]]
                    window_temp = sg.Window('Where do you want to save your interface model plots', layout_temp)
                    event_temp, values_temp = window_temp.read()
                    window_temp.close()
                    overall_values.update(values_temp)

                    overall_values['-interface_model_save_path-'] = "/".join(
                        list(overall_values['-interface_model_save_path-'].split('/')[0:-1]))
                    path_to_save = overall_values['-interface_model_save_path-']
                Locp.averaging_along_axis(to_plot=True, to_plot_atoms=True)
                Locp.averaging_along_axis(locpot_vec =stg2.current_locpot_vec,to_plot=True, to_plot_cursor_choice=True)
                layout_temp = [[sg.Menu(menu_def, tearoff=True)],
                               [sg.Text('Please indicate where your interface starts and ends', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-interface_start_position-')],
                               [sg.In(default_text=0, size=(20, 1), key='-interface_end_position-')],
                               [sg.Text('Please indicate where the region to be plotted', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-region_start_position-')],
                               [sg.In(default_text=0, size=(20, 1), key='-region_end_position-')],
                               [sg.Text('Please indicate what minima you want to treat as Delta', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-Delta_pos-')],
                               [sg.Text('Please indicate Where is the interface position', size=(100, 1))],
                               [sg.In(default_text=0, size=(20, 1), key='-Interface_position_model-')],
                               # [sg.Text('Please indicate what is the next minima you want to refer as the width - sigma', size=(100, 1))],
                               # [sg.In(default_text=0, size=(20, 1), key='-sigma_pos-')],
                               [sg.Submit(), sg.Cancel()]]
                window_temp = sg.Window('Modelling the interface - positions selection ', layout_temp)
                event_temp, values_temp = window_temp.read()
                window_temp.close()
                overall_values.update(values_temp)
                overall_values['-interface_start_position-'] = np.float64(overall_values['-interface_start_position-'])
                overall_values['-interface_start_position-'] = cons.A2m(overall_values['-interface_start_position-'])
                overall_values['-interface_end_position-'] = np.float64(overall_values['-interface_end_position-'])
                overall_values['-interface_end_position-'] = cons.A2m(overall_values['-interface_end_position-'])
                overall_values['-region_start_position-'] = np.float64(overall_values['-region_start_position-'])
                overall_values['-region_start_position-'] = cons.A2m(overall_values['-region_start_position-'])
                overall_values['-region_end_position-'] = np.float64(overall_values['-region_end_position-'])
                overall_values['-region_end_position-'] = cons.A2m(overall_values['-region_end_position-'])
                overall_values['-Delta_pos-'] = np.float64(overall_values['-Delta_pos-'])
                overall_values['-Delta_pos-'] = cons.A2m(overall_values['-Delta_pos-'])
                overall_values['-Interface_position_model-'] = np.float64(overall_values['-Interface_position_model-'])
                overall_values['-Interface_position_model-'] = cons.A2m(overall_values['-Interface_position_model-'])
                # overall_values['-sigma_pos-'] = np.float64(overall_values['-sigma_pos-'])
                # overall_values['-sigma_pos-'] = cons.A2m(overall_values['-sigma_pos-'])
                overall_values = convert_to_type(overall_values)
                results_interface_model = stg2.model_interface(overall_values['-interface_start_position-'], overall_values['-interface_end_position-'],overall_values['-region_start_position-'],overall_values['-region_end_position-']
                                                    ,overall_values['-Delta_pos-'], z_in = stg2.locp.locpot_vec[:,0], v_in = stg2.locp.locpot_vec[:,1],interface_pos = overall_values['-Interface_position_model-'],path_to_save = overall_values['-interface_model_save_path-'])
        except KeyError:
            pass
