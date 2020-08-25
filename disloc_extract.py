# -*- coding: utf-8 -*-

"""
Dislocation extraction from *.dislocations.vtk and post processing to make a table with type and length of dislocation
"""

import pandas as pd
import itertools
#import matplotlib.pyplot as plt
#from matplotlib import colors
#import pylab

df = []
df1 = []
df2 = []

with open('dump.imp1000mps.11500.dislocations.vtk', 'r') as f:
    
    for line in f:

        if 'burgers_vector_family' in line:
            #skip the nest two lines and read data until blank line
            for line in itertools.islice(f, 2, None):
                if line == "\n":
                    break
                else:
                    df1.append(line)
        
        if 'segment_length' in line:
            #skip the nest two lines and read data until blank line
            for line in itertools.islice(f, 2, None):
                if line == "\n":
                    break
                else:
                    df2.append(line)  

#Converting list of strings to actual values                    
for i in range(0, len(df1)): 
   df1[i] = int(df1[i]) 
   df2[i] = float(df2[i]) 

df = pd.DataFrame(
    {'Family': df1,
     'Length': df2,
    })

print("Total number of dislocations (including Other)=", len(df))    
    
df = df[df.Family != 0]    

print("Total number of dislocations (excluding Other)=", len(df))

df.to_csv('100nm_sc1000mps_L2_46ps.dat', sep='\t', index=False)  
 

