import numpy as np
from persim import plot_diagrams
from ripser import ripser
import matplotlib.pyplot as plt
import NEWDistance as distance
from utils import read_data
from TDA_analysis import tda_analysis
from TDA_analysis import plot_results

plt.style.use('ggplot')

if __name__ == '__main__':
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

    # ----------Distance Matrix Test----------
    print("\nDistance Matrix Test:")

    class1 = data[data['Income'] == '<=50K']
    class2 = data[data['Income'] == '>50K']
    N = 50
    np.random.seed(0)
    sampled_class1 = class1.sample(N)
    sampled_class2 = class2.sample(N)

    d = distance.Distance()
    d.weights['Income'] = 0
    class1_matrix = d.distance_matrix(sampled_class1)
    class2_matrix = d.distance_matrix(sampled_class2)
    class1_diagrams = ripser(class1_matrix, maxdim=2, distance_matrix=True)['dgms']
    class2_diagrams = ripser(class2_matrix, maxdim=2, distance_matrix=True)['dgms']

    plot_diagrams(class1_diagrams, show=True)
    plot_diagrams(class2_diagrams, show=True)

    # ----------TDA Test----------
    print("\nTDA Test:")

    # ----------Wage geometry between genders----------
    print("Geometry of males and females with and without salary.")
    variable = 'Gender'
    N = 25
    N_sig = 25

    dist = distance.Distance()
    dist.weights['Income'] = 1
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results)
    dist.weights['Income'] = 0
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results)

    # ----------Geometries of the rich and poor----------
    print("Geometries of the rich and poor.")
    variable = 'Income'
    dist.weights['Income'] = 1
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results)

    # ----------Geometries of the different races----------
    print("Geometries of the different races.")
    variable = 'Race'
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results)