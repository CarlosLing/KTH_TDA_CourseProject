import numpy as np
from persim import plot_diagrams
from ripser import ripser
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import NEWDistance as distance
from utils import read_data
from TDA_analysis import tda_analysis
inf=float("inf")

if __name__ == '__main__':

    d = distance.Distance()
    d.weights[3] = 0.00001
    d.weights[10] = 0.00001
    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

    # ----------TDA Test----------
    print("\nTDA Test:")
    np.random.seed(3)
    N = 20
    sampled_data = data.sample(N)
    D = d.distance_matrix(sampled_data)
    diagrams = ripser(D, maxdim=1, distance_matrix=True)['dgms']
    plot_diagrams(diagrams, show=True)


    results = tda_analysis(data, variable='Gender')

    variable = 'Gender'
    types = data[variable].unique()

    plt.figure()
    results[t]['barcodes'][0].plot()
    plt.show()
    plt.figure()
    results[types[0]]['mean_norm'].plot()
    plt.show()
    plt.figure()
    results[types[1]]['mean_norm'].plot()
    plt.show()

    t = types[0]
    N_sig = 20
    plt. figure()
    for i in range(N_sig):
        results[types[0]]['normalized_sign'][i].plot(color='red')
        results[types[1]]['normalized_sign'][i].plot(color='blue')
    plt.show()

    t = types[0]
    plt.figure()
    upper = results[t]['mean_norm'] + results[t]['sd_norm']
    lower = results[t]['mean_norm'] - results[t]['sd_norm']
    upper.plot(color='red')
    results[t]['mean_norm'].plot(color='red')
    lower.plot(color='red')
    t = types[1]
    upper = results[t]['mean_norm'] + results[t]['sd_norm']
    lower = results[t]['mean_norm'] - results[t]['sd_norm']
    upper.plot(color='blue')
    results[t]['mean_norm'].plot(color='blue')
    lower.plot(color='blue')
    plt.show()
    plt.figure()
    results[t]['sd_norm'].plot()
    plt.show()
    plt.figure()
    results[types[0]]['normalized_sign'][0].plot()
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
