import pandas as pd
import numpy as np
from ripser import ripser
from persim import plot_diagrams

from utils import read_data
from distance import get_distance_matrix

if __name__ == '__main__':
    np.random.seed(5)
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')
    N = 300

    distance_matrix, sampled_data = get_distance_matrix(data, N)
    diagrams = ripser(distance_matrix, maxdim=2, distance_matrix=True)['dgms']
    plot_diagrams(diagrams, show=True)
