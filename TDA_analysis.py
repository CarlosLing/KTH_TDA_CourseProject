import stableRANK as sr
from distance import get_distance_matrix
import numpy as np
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
