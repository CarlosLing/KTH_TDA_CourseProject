import stableRANK as sr
from distance import get_distance_matrix

import numpy as np
import matplotlib.pyplot as plt

inf=float("inf")


def tda_analysis(data, variable='Income', N=50, N_sig=20):

    # Do analysis of signatures regarding variable
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
                      'mean_H0': (1 / N_sig) * sum_H0,
                      'mean_H1': (1 / N_sig) * sum_H1,
                      'mean_norm': (1 / N_sig) * sum_norm}

        sum_diff_sq = 0

        for i in range(N_sig):
            diff_norm = results[t]['normalized_sign'][i] - results[t]['mean_norm']
            sum_diff_sq = sum_diff_sq + diff_norm*diff_norm

        results[t]['sd_norm'] = (1 / (N_sig-1)) * sum_diff_sq
        results[t]['sd_norm'].content[1] = np.sqrt(results[t]['sd_norm'].content[1])

    return results


COLORS = ['red', 'blue', 'green', 'magenta']
DCOLORS = ['darkred', 'darkblue', 'darkgreen', 'darkmagenta']


def plot_results(results, types, N_sig=20, xmax=1):

    n_t = len(types)
    plt.figure()
    for i in range(n_t):
        t = types[i]
        color = COLORS[i]
        dcolor = DCOLORS[i]
        upper = results[t]['mean_norm'] + 2*results[t]['sd_norm']
        lower = results[t]['mean_norm'] - 2*results[t]['sd_norm']
        upper.plot(color=color)
        results[t]['mean_norm'].plot(color=dcolor)
        lower.plot(color=color)

    plt.axis(xmax=xmax)
    plt.show()

    for i in range(n_t):
        plt.figure()
        t = types[i]
        color = COLORS[i]
        dcolor = DCOLORS[i]
        for j in range(N_sig):
            results[t]['normalized_sign'][j].plot(color='black', alpha = 0.2)
        upper = results[t]['mean_norm'] + 2*results[t]['sd_norm']
        lower = results[t]['mean_norm'] - 2*results[t]['sd_norm']
        upper.plot(color=color)
        results[t]['mean_norm'].plot(color=dcolor)
        lower.plot(color=color)
        plt.axis(xmax=xmax)
        plt.show()

