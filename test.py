
import numpy as np
import matplotlib.pyplot as plt

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

fig, axes = plt.subplots(nrows=1)
axes.imshow(gradient, aspect='auto', cmap=plt.get_cmap('tab20'))
plt.show()