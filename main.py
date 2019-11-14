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
    d.weights[3] = 0.00001
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

    # ----------Distance Test----------
    print("Distance Test:")
    d1 = data.iloc[0]
    d2 = data.iloc[1]
    d3 = data.iloc[2]
    d1v = [d1.Age, d1.EducationNum, d1.HoursPerWeek, d1.NetCapital, d1.Gender, d1.Race,
           d1.WorkClass, d1.MaritalStatus, d1.Occupation, d2.Relationship, d1.NativeCountry]
    d2v = [d2.Age, d2.EducationNum, d2.HoursPerWeek, d2.NetCapital, d2.Gender, d2.Race,
           d2.WorkClass, d2.MaritalStatus, d2.Occupation, d2.Relationship, d2.NativeCountry]
    d3v = [d3.Age, d3.EducationNum, d3.HoursPerWeek, d3.NetCapital, d3.Gender, d3.Race,
           d3.WorkClass, d3.MaritalStatus, d3.Occupation, d3.Relationship, d3.NativeCountry]
    print(d.standard_dist(d1v, d2v))
    print(d.standard_dist(d1v, d3v))
    print(d.standard_dist(d2v, d3v))
    d.weights *= 2;
    print(d.standard_dist(d1v, d2v))
    print(d.standard_dist(d1v, d3v))
    print(d.standard_dist(d2v, d3v))

    # ----------TDA Test----------
    print("\nTDA Test:")
    np.random.seed(5)
    N = 75
    D = np.zeros((N, N))
    sampled_data = data.sample(N)
    dist = dist.Distance()
    dist.weights[3] = 0.00001
    for i in range(N):
        for j in range(i):
            d1 = data.iloc[i]
            d2 = data.iloc[j]
            d1v = [d1.Age, d1.EducationNum, d1.HoursPerWeek, d1.NetCapital, d1.Gender, d1.Race,
                   d1.WorkClass, d1.MaritalStatus, d1.Occupation, d2.Relationship, d1.NativeCountry]
            d2v = [d2.Age, d2.EducationNum, d2.HoursPerWeek, d2.NetCapital, d2.Gender, d2.Race,
                   d2.WorkClass, d2.MaritalStatus, d2.Occupation, d2.Relationship, d2.NativeCountry]
            d = dist.standard_dist(d1v, d2v)
            D[i, j] = d
            D[j, i] = d
    diagrams = ripser(D, maxdim=2, distance_matrix=True)['dgms']
    plot_diagrams(diagrams, show=True)