# -*- coding: utf-8 -*-
"""
Dislocation binning and plotting

@author: Sumit
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import colors
import pylab

import pandas as pd

dis_data = pd.read_csv('L2_46ps.txt', delimiter='\t')
n_bins = 50

disloc_type = dis_data.iloc[:,0].values 
disloc_len = dis_data.iloc[:,1].values 

# N is the count in each bin, bins is the lower-limit of the bin
N, bins, patches = plt.hist(disloc_len, bins=n_bins, range=[0, 200])

# We'll color code by height, but you could use any scalar
fracs = N / N.max()

# we need to normalize the data to 0 to 1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.coolwarm(norm(thisfrac))
    thispatch.set_facecolor(color)

# We can also normalize our inputs by the total number of counts
#plt.hist(disloc_len, bins=n_bins, density=True)

#.hist(disloc_len, bins = num_bins, normed=1, facecolor='blue', alpha=0.5 label='Data')
plt.ylabel('Numbers', fontsize=12, fontname='Times New Roman')
plt.xlabel('Dislocation Length (Å)', fontsize=12, fontname='Times New Roman')
pylab.xticks(fontsize=10, fontname='Times New Roman')
pylab.yticks(fontsize=10, fontname='Times New Roman')
#plt.savefig('100nm_sc1000_L2_46ps_histogram.png', dpi=300, facecolor='w', edgecolor='w', format='png')
plt.show()



