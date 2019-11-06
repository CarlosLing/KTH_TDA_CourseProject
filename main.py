import pandas as pd
import numpy as np
from ripser import ripser
from persim import plot_diagrams

from utils import read_data
from distance import get_distance_matrix

import NEWDistance as dist
from utils import read_data
if __name__ == '__main__':
    d = dist.Distance()
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')
    d1 = data.iloc[0]
    d2 = data.iloc[0]
    d1v = [d1.Age, d1.EducationNum, d1.HoursPerWeek, d1.NetCapital, d1.Gender, d1.Race,
           d1.WorkClass, d1.MaritalStatus, d1.Occupation, d1.NativeCountry]
    d2v = [d2.Age, d2.EducationNum, d2.HoursPerWeek, d2.NetCapital, d2.Gender, d2.Race,
           d2.WorkClass, d2.MaritalStatus, d2.Occupation, d2.NativeCountry]
    print(d.standard_dist(d1v, d2v))


    # np.random.seed(5)
    # data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')
    # N = 300
    #
    # distance_matrix, sampled_data = get_distance_matrix(data, N)
    # diagrams = ripser(distance_matrix, maxdim=2, distance_matrix=True)['dgms']
    # plot_diagrams(diagrams, show=True)
