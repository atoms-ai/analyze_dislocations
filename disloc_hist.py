# -*- coding: utf-8 -*-
"""
Dislocation binning, histogram fitting and plotting for any QCGD systems (generic)

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

disloc_len_max = Acg*100
plot_tick_len = Acg*20

#################################################################################
          
#Specific BV family analysis 
#bvf=2   #(1-Perfect, 2- Shockley, 3- SR, 4 - Hirth, 5 - Frank, 6 - GB1, 7 - GB2)
#df = df[df['Family'] == bvf]

num_dis = len(df)       # num of dislocations

disloc_type = df.iloc[:,0].values     
disloc_len = df.iloc[:,1].values 

n_bins = 100     # num of bins
N, bins, patches = plt.hist(disloc_len, bins=n_bins, density=True, range=[0, disloc_len_max])

# color code by height, but you could use any scalar
fracs = N / N.max()

# we need to normalize the data to 0 to 1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Loop through objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.coolwarm(norm(thisfrac))
    thispatch.set_facecolor(color)

#Discretizing x values
xt = plt.xticks()[0]  
xmin, xmax = 0, disloc_len_max  
lnspc = np.linspace(xmin, xmax, len(disloc_len))

#########################  Log normal fitting  ###############################

shape, loc, scale = stats.lognorm.fit(disloc_len, floc=0) 
pdf_lognorm = stats.lognorm.pdf(lnspc, shape, loc, scale) 
plt.plot(lnspc, pdf_lognorm, color = "k", label="Lognormal")
plt.legend()

#########################################################################


ax = plt.axes()
plt.ylabel('Probability', fontsize=12, fontname='Times New Roman')
plt.xlabel('Dislocation Length (Å)', fontsize=12, fontname='Times New Roman')
pylab.xticks(fontsize=10, fontname='Times New Roman')
pylab.yticks(fontsize=10, fontname='Times New Roman')
ax.xaxis.set_major_locator(ticker.MultipleLocator(plot_tick_len))
plt.text(0.6, 0.6, "Number of dislocations = %i" %num_dis + "\n\n L%i (t = 800 ps)"  %Acg + "\n\n α(fit) = %f" %scale + ", σ(fit) = %f" %shape,       
         horizontalalignment='center', verticalalignment='center', fontname='Times New Roman', 
         transform=ax.transAxes)
plt.savefig("2um_sc1000_800ps_hist_L%i.png" %Acg, dpi=300, facecolor='w', edgecolor='w', bbox_inches = 'tight', format='png')
plt.show()



