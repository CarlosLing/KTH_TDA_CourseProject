import pandas as pd
import numpy as np

from utils import read_data
from distance import get_distance_matrix
from ripser import ripser
import stableRANK as sr

inf=float("inf")
import matplotlib.pyplot as plt
plt.style.use('ggplot')

if __name__ == '__main__':

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

