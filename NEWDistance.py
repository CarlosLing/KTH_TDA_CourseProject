import pandas as pd
import numpy as np
from utils import read_GDP

AGE_RANGE = 73
EDUCATION_RANGE = 15
HPW_RANGE = 98
CAPITAL_RANGE = 104355
RELATIONSHIP_RANGE = 4
GDP_RANGE = 29126.373789999998


def p_norm_dist(values1, values2, p=1):
    if isinstance(values1, list):
        return np.linalg.norm(np.subtract(values1, values2), ord=p)
    else:
        return abs(values1 - values2)


def p_norm_dist_function(p):
    return lambda value1, value2: p_norm_dist(value1, value2, p)


def indicator(value1, value2):
    return 1 * (value1 != value2)


gdp = read_GDP('GDP_percapita_complete.csv')


def GDP_dist(country1, country2, sub_func=p_norm_dist_function(1)):
    GDP1 = gdp.loc[country1]["GDP_PC"]
    GDP2 = gdp.loc[country2]["GDP_PC"]
    return sub_func(GDP1, GDP2)


class Distance:
    """
    Distance class providing flexible distances.

    Attributes:
        distances (dict): The distances for each variable and the aggregation distance.
        weights (dict): The weighting for each of the sub-distances.
                        !!!IMPORTANT!!! If predictive analysis is the goal set at least
                        one of these to 0 to exclude it from the aggregated distance.
    """
    def __init__(self):
        p = 1
        self.distances = {
            'Age': p_norm_dist_function(p),
            'WorkClass': indicator,
            'EducationNum': p_norm_dist_function(p),
            'MaritalStatus': indicator,
            'Occupation': indicator,
            'Relationship': indicator,
            'Race': indicator,
            'Gender': indicator,
            'HoursPerWeek': p_norm_dist_function(p),
            'NativeCountry': GDP_dist,
            'Income': indicator,
            'NetCapital': p_norm_dist_function(p),
            'Aggregate': np.linalg.norm
        }

        self.weights = {
            'Age': 1/AGE_RANGE,
            'WorkClass': 1,
            'EducationNum': 1/EDUCATION_RANGE,
            'MaritalStatus': 1,
            'Occupation': 1,
            'Relationship': 1,
            'Race': 1,
            'Gender': 1,
            'HoursPerWeek': 1/HPW_RANGE,
            'NativeCountry': 1/GDP_RANGE,
            'Income': 1,
            'NetCapital': 1/CAPITAL_RANGE
        }

    def standard_dist(self, point1, point2):
        d = self.distances
        dists = [d['Age'](point1[0], point2[0]), d['WorkClass'](point1[1], point2[1]),
                 d['EducationNum'](point1[2], point2[2]), d['MaritalStatus'](point1[3], point2[3]),
                 d['Occupation'](point1[4], point2[4]), d['Relationship'](point1[5], point2[5]),
                 d['Race'](point1[6], point2[6]), d['Gender'](point1[7], point2[7]),
                 d['HoursPerWeek'](point1[8], point2[8]), d['NativeCountry'](point1[9], point2[9]),
                 d['Income'](point1[10], point2[10]), d['NetCapital'](point1[11], point2[11])]
        dists = np.multiply(dists, list(self.weights.values()))

        return d['Aggregate'](dists)

    def distance_matrix(self, data):
        n = len(data.index)
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i):
                d1 = data.iloc[i]
                d2 = data.iloc[j]
                d1v = [d1.Age, d1.WorkClass, d1.EducationNum, d1.MaritalStatus, d1.Occupation,
                       d1.Relationship, d1.Race, d1.Gender, d1.HoursPerWeek, d1.NativeCountry, d1.Income, d1.NetCapital]
                d2v = [d2.Age, d2.WorkClass, d2.EducationNum, d2.MaritalStatus, d2.Occupation,
                       d2.Relationship, d2.Race, d2.Gender, d2.HoursPerWeek, d2.NativeCountry, d2.Income, d2.NetCapital]
                d = self.standard_dist(d1v, d2v)
                matrix[i, j] = d
                matrix[j, i] = d
        return matrix
