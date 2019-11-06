import pandas as pd
import numpy as np

from utils import read_data
from distance import get_distance_matrix

if __name__ == '__main__':

    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

    N = 2
    print("Ivar is the most handsome guy ever.")
    distance_matrix, sampled_data = get_distance_matrix(data, N)

