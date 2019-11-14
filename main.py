import pandas as pd
import numpy as np
from ripser import ripser
from persim import plot_diagrams

from utils import read_data
from distance import get_distance_matrix
from ripser import ripser
import stableRANK as sr

inf=float("inf")
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import NEWDistance as dist
from utils import read_data

if __name__ == '__main__':
    d = dist.Distance()
    d.weights[3] = 0.00001
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

    N = 50
    N_sig = 20
    # Do analysis of signatures regarding variable
    variable = 'Income'
    types = data[variable].unique()

    results = dict()
    contours = {"H0": [[[0], [1]], ("area", inf, inf)]}

    for t in types:

        data_subset = data[data[variable] == t]
        barcodes = list()
        signatures = list()
        normalized_sig = list()
        sum_H0 = 0
        sum_H1 = 0
        sum_norm = 0
        for i in range(N_sig):

            distance_matrix, sampled_data = get_distance_matrix(data_subset, N)
            ob = sr.euc_object(points=distance_matrix)

            bc = ob.barcode(distance_matrix=True)
            sign = bc.stable_rank_max(contours)
            n_sig = sign["H1"] * (sign["H0"].invert())

            barcodes.append(bc)
            signatures.append(sign)
            normalized_sig.append(n_sig)

            sum_H0 = sum_H0 + sign['H0']
            sum_H1 = sum_H1 + sign['H1']
            sum_norm = sum_norm + n_sig

        results[t] = {'barcodes': barcodes,
                      'signatures': signatures,
                      'normalized_sign': normalized_sig,
                      'mean_H0': (1/N_sig) * sum_H0,
                      'mean_H1': (1/N_sig) * sum_H1,
                      'mean_norm': (1/N_sig) * sum_norm}

    plt.figure()
    results[t]['barcodes'][0].plot()
    plt.show()
    plt.figure()
    results[types[0]]['mean_norm'].plot()
    plt.show()
    plt.figure()
    results[types[1]]['mean_norm'].plot()
    plt.show()
    plt.figure()
    results[t]['signatures'][0]['H1'].plot()
    plt.show()
    plt.figure()
    results[t]['normalized_sign'][0].plot()
    plt.show()

    ### Here comes the analysis:



    barcode = object.barcode(distance_matrix=True)
    barcode.plot("bar")



    plt.figure()
    signatures["H0"].plot()


    plt.figure()
    signatures["H1"].plot()
    plt.show()

    plt.figure()
    normelized_sig = signatures["H1"] * (signatures["H0"].invert())
    normelized_sig.plot()
    plt.show()
    
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