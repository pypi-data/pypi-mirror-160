# Read LOCPOT

import numpy as np
import re

def ReadLOCPOT(FilePath):
    
    # Open file and read contents
    fid = open(FilePath,'r')
    fconts = fid.read()
    
    # Define regex to find dimensions
    findtext = ('\s* \d+ \s* \d+ \s* \d+')
    
    # Find all occurances of three integers in a line
    x = re.findall(findtext,fconts)
    
    # Take the last occurance and split into components
    xdim, ydim, zdim = x[-1].split()
    dimen = int(zdim), int(xdim), int(ydim)
    zpoints = dimen[0]

    # Now find the line where the potential begins
    newtext = '(.*)' + xdim + '(.*)' + ydim + '(.*)' + zdim + '(.*)'
    
    # Delete file contents (to save memory)
    fconts = None
    
    # Rewind to beginning of file
    fid.seek(0)
    
    # Read entire file into a list by line
    linelist = fid.readlines()
    fid.close()
    
    # Get length of z vector
    # IMPORTANT: assumes cubic, tegragonal,
    # or hexagonal lattice
    zlength = float(linelist[4].split()[-1])
    
    # Create k-vector
    # Divide into dz - entire length by number of points
    dz = zlength / zpoints
    zaxis = (np.arange(zpoints)-1)*zlength/zpoints
    kaxis = np.fft.fftfreq(zpoints,dz)*2*np.pi
    
    # Look for beginning of potential
    LineToStart = 0
    for i in linelist:
        LineToStart = LineToStart + 1
        if re.match(newtext,i):
            break
    
    # Initialize potential variable
    potential = np.zeros(np.prod(dimen))
    
    # How many lines to read (assuming 5 points
    # per line with overflow)
    LinesToRead = int(np.ceil(np.prod(dimen)/5))
    
    # Read potential into array
    k = 0
    for i in linelist[LineToStart:LineToStart+LinesToRead]:
        LineRead = i.split()
        for j in LineRead:
            potential[k] = float(j)
            k = k + 1

    # Reshape - z-axis FIRST (first index is sheets)
    potential = np.reshape(potential,dimen)
    
    # Average over xy axis
    avpot = np.sum(potential,axis=(1,2))/np.prod(dimen[1:])
    
    return avpot, zaxis, kaxis