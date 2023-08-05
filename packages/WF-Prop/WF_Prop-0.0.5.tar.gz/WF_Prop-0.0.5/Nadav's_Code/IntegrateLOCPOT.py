import numpy as np

def IntegrateLOCPOT(potential):
    zpot = np.zeros(potential.shape[-1])
    k = 0
    for sheet in potential:
        zpot[k] = np.sum(sheet)