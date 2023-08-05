import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from Locpot_class import *
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

__version__ = '0.0.6'

