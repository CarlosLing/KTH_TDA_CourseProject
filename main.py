from persim import plot_diagrams
from ripser import ripser
from TDA_analysis import *
from utils import read_data

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
    N = 25
    N_sig = 50
    dist = distance.Distance()

    # ----------Wage geometry between genders----------
    print("Geometry of males and females with and without salary.")
    variable = 'Gender'
    results = tda_analysis(data, seed=0, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)
    dist.weights['Income'] = 0
    results = tda_analysis(data, seed=0, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)
    dist = distance.Distance()

    # ----------Geometries of the rich and poor----------
    print("Geometries of the rich and poor.")
    variable = 'Income'
    print("All sub-distances currently active.")
    results = tda_analysis(data, dist=dist, variable=variable, seed=0, N=N, N_sig=N_sig)
    plot_compiled_results(results, xmax=1)
    for key in dist.weights.keys():
        print("Current inactive distance: " + key)
        weight = dist.weights[key]
        dist.weights[key] = 0
        results = tda_analysis(data, dist=dist, variable=variable, seed=0, N=N, N_sig=N_sig)
        plot_compiled_results(results, xmax=1)
        dist.weights[key] = weight
    print("Marital status, occupation and gender seem important. Check this!")
    print("Without marital status, occupation and gender.")
    dist.weights['MaritalStatus'] = 0
    dist.weights['Occupation'] = 0
    dist.weights['Gender'] = 0
    results = tda_analysis(data, dist=dist, variable=variable, seed=0, N=N, N_sig=N_sig)
    plot_compiled_results(results, xmax=1)

    print("Only marital status, occupation and gender.")
    dist.zero_weights()
    dist.weights['MaritalStatus'] = 1
    dist.weights['Occupation'] = 1
    dist.weights['Gender'] = 1
    results = tda_analysis(data, dist=dist, variable=variable, seed=0, N=N, N_sig=N_sig)
    plot_compiled_results(results, xmax=1)
    print("Weird...")

    # ----------Geometries of the rich and poor----------
    print("Geometries of the rich and poor with different country distance.")
    variable = 'Income'
    dist.distances['NativeCountry'] = distance.indicator
    dist.weights['NativeCountry'] = 1
    results = tda_analysis(data, dist=dist, variable=variable, seed=0, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)
    dist = distance.Distance()

    # ----------Geometries of the different races----------
    print("Geometries of the different races.")
    variable = 'Race'
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)

    # ----------Geometries of the different Relationship----------
    print("Geometries of the different Relationship.")
    variable = 'Relationship'
    results = tda_analysis(data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)

    # ----------Geometries of the different Marital S----------
    print("Geometries of the different Marital Status.")
    marital_data = data[data['MaritalStatus'] != 'Married-AF-spouse']
    variable = 'MaritalStatus'
    results = tda_analysis(marital_data , dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)

    # ----------Geometries of the different WorkClass----------
    print("Geometries of the different WorkClass.")
    WorkClass_data = data[data['WorkClass'] != '?']
    WorkClass_data = WorkClass_data[WorkClass_data['WorkClass'] != 'Never-worked']
    WorkClass_data = WorkClass_data[WorkClass_data['WorkClass'] != 'Without-pay']
    variable = 'WorkClass'
    results = tda_analysis(WorkClass_data, dist=dist, variable=variable, N=N, N_sig=N_sig)
    plot_results(results, xmax=1)