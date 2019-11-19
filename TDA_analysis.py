import stableRANK as sr
from distance import get_distance_matrix
import numpy as np
import matplotlib.pyplot as plt
import NEWDistance as distance
import math

inf = float("inf")


def tda_analysis(data, variable='Income', dist=distance.Distance(), seed=float('nan'), N=50, N_sig=20):
    # Do analysis of signatures regarding variable
    if not math.isnan(seed): np.random.seed(seed)
    types = data[variable].unique()

    results = dict()
    contours = {"H0": [[[0], [1]], ("area", inf, inf)]}

    for t in types:
        data_type = data[data[variable] == t]

        barcodes = list()
        signatures = list()
        normalized_sig = list()
        sum_H0 = 0
        sum_H1 = 0
        sum_norm = 0
        for i in range(N_sig):
            sampled_data = data_type.sample(N)
            distance_matrix = dist.distance_matrix(sampled_data)

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
            sum_diff_sq = sum_diff_sq + diff_norm * diff_norm

        results[t]['sd_norm'] = (1 / (N_sig - 1)) * sum_diff_sq
        results[t]['sd_norm'].content[1] = np.sqrt(results[t]['sd_norm'].content[1])

    return results


COLORS = ['red', 'blue', 'green', 'magenta', 'cyan', 'yellow']
DCOLORS = ['darkred', 'darkblue', 'darkgreen', 'darkmagenta', 'darkcyan', 'orange']


def plot_results(results, xmax=float('nan')):
    types = list(results.keys())
    n_t = len(types)
    plt.figure()
    for i in range(n_t):
        t = types[i]
        color = COLORS[i]
        dcolor = DCOLORS[i]
        upper = results[t]['mean_norm'] + 2 * results[t]['sd_norm']
        lower = results[t]['mean_norm'] - 2 * results[t]['sd_norm']
        upper.plot(color=color)
        results[t]['mean_norm'].plot(color=dcolor)
        lower.plot(color=color)

    if not math.isnan(xmax) : plt.axis(xmax=xmax)
    plt.axis(xmin=0)
    plt.show()

    for i in range(n_t):
        plt.figure()
        t = types[i]
        color = COLORS[i]
        dcolor = DCOLORS[i]
        for j in range(len(results[types[0]]['barcodes'])):
            results[t]['normalized_sign'][j].plot(color='black', alpha=0.2)
        upper = results[t]['mean_norm'] + 2 * results[t]['sd_norm']
        lower = results[t]['mean_norm'] - 2 * results[t]['sd_norm']
        upper.plot(color=color)
        results[t]['mean_norm'].plot(color=dcolor)
        lower.plot(color=color)
        if not math.isnan(xmax) : plt.axis(xmax=xmax)
        plt.axis(xmin=0)
        plt.show()
