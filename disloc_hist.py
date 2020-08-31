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


df = pd.read_csv('100nm_sc1000mps_MD_150ps.dat', delimiter='\t')
            

#Specific BV family analysis 
#bvf=2   #(1-Perfect, 2- Shockley, 3- SR, 4 - Hirth, 5 - Frank, 6 - GB1, 7 - GB2)
#df = df[df['Family'] == bvf]

num_dis = len(df)       # num of dislocations

disloc_type = df.iloc[:,0].values     
disloc_len = df.iloc[:,1].values 

n_bins = 50     # num of bins
N, bins, patches = plt.hist(disloc_len, bins=n_bins, density=True, range=[0, 100])

# color code by height, but you could use any scalar
fracs = N / N.max()

# we need to normalize the data to 0 to 1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Loop through objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.coolwarm(norm(thisfrac))
    thispatch.set_facecolor(color)

# We can also normalize our inputs by the total number of counts
#plt.hist(disloc_len, bins=n_bins, density=True)

#Fitting
xt = plt.xticks()[0]  
#xmin, xmax = min(xt), max(xt)  
xmin, xmax = 0, 100  
lnspc = np.linspace(xmin, xmax, len(disloc_len))

#Beta fitting
#ab,bb,cb,db = stats.beta.fit(disloc_len)  
#pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
#plt.plot(lnspc, pdf_beta, label="Beta")

#########################  Log normal fitting  ###############################
shape, loc, scale = stats.lognorm.fit(disloc_len, floc=0) 
pdf_lognorm = stats.lognorm.pdf(lnspc, shape, loc, scale) 
plt.plot(lnspc, pdf_lognorm, color = "k", label="Lognormal")
plt.legend()

#########################  L2 fitting ###############################

shape_l2 = 0.694752
scale_l2 = 22.928668/2
loc_l2 = 0.0

t = 0
xval = np.arange(1, 100, 1)
L2fit = [None] * len(xval)
L2fit[0] = 0            #explicitly setting first value to zero to avoid math domain error in the loop

for i in range(1, 99, 1):
    L2fit[t+1] = 1 / (shape_l2*((i)/scale_l2)*math.sqrt(2*math.pi)) * math.exp(-1/2*(math.log((i)/scale_l2)/shape_l2)**2) / scale_l2
    t = t+1

plt.plot(xval, L2fit, label="L2_fit", color="r", marker = ".") # Create line plot with lognormal equation
plt.legend()

#########################################################################


ax = plt.axes()
plt.ylabel('Probability density', fontsize=12, fontname='Times New Roman')
plt.xlabel('Dislocation Length (Å)', fontsize=12, fontname='Times New Roman')
pylab.xticks(fontsize=10, fontname='Times New Roman')
pylab.yticks(fontsize=10, fontname='Times New Roman')
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
plt.text(0.6, 0.6, "Number of dislocations = %i \n\n MD (t = 150 ps)" % num_dis + "\n\n α(fit) = %f" %scale_l2 + 
         ", σ(fit) = %f" %shape_l2, 
         horizontalalignment='center', verticalalignment='center', fontname='Times New Roman', 
         transform=ax.transAxes)
plt.savefig('100nm_sc1000_150ps_L2FITMD_histogram.png', dpi=300, facecolor='w', edgecolor='w', bbox_inches = 'tight', format='png')
plt.show()



