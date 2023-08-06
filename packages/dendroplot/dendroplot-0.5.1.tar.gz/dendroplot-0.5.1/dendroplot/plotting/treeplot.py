#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from astrodendro import Dendrogram
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

label = 'A439_12'

# Load the dendrogram
try:
	d = Dendrogram.load_from(label+'_dendrogram.hdf5')
	print('Loading pre-existing dendrogram')
except:
	print('Could not load',label+'_dendrogram.hdf5')

# Plot the tree
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)            
ax.set_yscale('log')
ax.set_xlim(-3, 156)
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
ax.set_xlabel('Structure Number', fontsize=12)
ax.set_ylabel('Brightness Temperature [K]', fontsize=12)
p = d.plotter()
branch = [s for s in d.all_structures if s not in d.leaves and s not in d.trunk]
tronly = [s for s in d.trunk if s not in d.leaves]
for st in tronly:
	p.plot_tree(ax, structure=[st], color='brown', subtree=False)
for st in branch:
	p.plot_tree(ax, structure=[st], color='black', subtree=False)
for st in d.leaves:
	p.plot_tree(ax, structure=[st], color='green')
plt.savefig(label+'_dendrogram.pdf', bbox_inches='tight')
