# -*- coding: utf-8 -*-
"""
Dislocation binning and plotting

@author: Sumit
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as ticker
import numpy as np  
import pylab
import math 
import pandas as pd
from scipy import stats


########################### System and QCGD-LOC #############################

Acg = 64

dia = 20000.0         # Particle diameter in Angstroms
vol = (4/3)*math.pi*((dia/2)**3)

df = pd.read_csv("2um_sc1000mps_L%i_800ps.dat" %Acg, delimiter='\t')
          
#Specific BV family analysis 
#bvf=2   #(1-Perfect, 2- Shockley, 3- SR, 4 - Hirth, 5 - Frank, 6 - GB1, 7 - GB2)
#df = df[df['Family'] == bvf]


num_dis = len(df)       # num of dislocations
num_dis_qcgd = num_dis* ((Acg)**3)

disloc_type = df.iloc[:,0].values     
disloc_len = df.iloc[:,1].values 


#Discretizing x values
xt = plt.xticks()[0]  
xmin, xmax = 0, 100  
lnspc = np.linspace(xmin, xmax, len(disloc_len))

#########################  QCGD fitting ###############################

shape_qcgd = 0.7585430758017024
scale_qcgd = (770.9300030200636/Acg)
loc = 0.0

t = 0
xval = np.arange(1, 100, 1)
qcgd_fit = [None] * len(xval)
qcgd_fit[0] = 0            #explicitly setting first value to zero to avoid math domain error in the loop

tot_dis = 0
for i in range(1, 99, 1):
    qcgd_fit[t+1] = num_dis_qcgd / (shape_qcgd*((i)/scale_qcgd)*math.sqrt(2*math.pi)) * math.exp(-1/2*(math.log((i)/scale_qcgd)/shape_qcgd)**2) / scale_qcgd
    tot_dis = tot_dis + qcgd_fit[t+1]*(t+1)
    t = t+1
    
print(tot_dis)
plt.plot(xval, qcgd_fit, label="L%i_fit" %Acg, color="r", marker = ".") # Create line plot with lognormal equation
plt.legend()

dis_den = (10**20) * tot_dis/vol
print(dis_den)

#########################################################################


ax = plt.axes()
plt.ylabel('Numbers', fontsize=12, fontname='Times New Roman')
plt.xlabel('Dislocation Length (Å)', fontsize=12, fontname='Times New Roman')
pylab.xticks(fontsize=10, fontname='Times New Roman')
pylab.yticks(fontsize=10, fontname='Times New Roman')
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
plt.text(0.6, 0.6, "Number of super dislocations = %i" % num_dis + "\n\n L%i (t = 800 ps)" %Acg  + "\n\n α(fit) = %f" %scale_qcgd +
          ", σ(fit) = %f" %shape_qcgd + "\n\n DD(Predicted) = %e" %dis_den +"/m\u00b2", 
          horizontalalignment='center', verticalalignment='center', fontname='Times New Roman', 
          transform=ax.transAxes)
plt.savefig('2um_sc1000_800ps_MD_hist_L%ifit.png' %Acg, dpi=300, facecolor='w', edgecolor='w', bbox_inches = 'tight', format='png')
plt.show()



