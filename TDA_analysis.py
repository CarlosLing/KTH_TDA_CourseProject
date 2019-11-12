import stableRANK as sr

import numpy as np
inf=float("inf")

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import _pickle as pickle
from ripser import ripser

data = np.random.random((100,2))
diagrams = ripser(data)['dgms']
plot_diagrams(diagrams, show=True)

rips = Rips()
data = np.random.random((100,2))
diagrams = rips.fit_transform(data)
rips.plot(diagrams)
