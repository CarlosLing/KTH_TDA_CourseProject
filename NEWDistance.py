import pandas as pd
import numpy as np
from utils import read_GDP


def p_norm(values1, values2, p=1):
    return np.linalg.norm(np.subtract(values1, values2), ord=p);

def p_norm_function(p):
    return lambda value1, value2: p_norm(value1, value2, p)

def indicator(value1, value2):
    return 1 * (value1 != value2)

gdp = read_GDP('GDP_percapita_complete.csv')
def GDP(country1, country2, sub_func=p_norm_function(1)):
    GDP1 = gdp.loc[country1, "GDP_PC"]
    GDP2 = gdp.loc[country2, "GDP_PC"]
    return sub_func(GDP1, GDP2)


# -------------------------DISTANCE CLASS-------------------------
# Create an instance and specify how you want this instance to behave,
# what distances, weights and aggregation to use.

class Distance:
    def __init__(self):
        self.p = 1
        self.age_dist = p_norm_function(self.p)
        self.education_dist = p_norm_function(self.p)
        self.hours_dist = p_norm_function(self.p)
        self.capital_dist = p_norm_function(self.p)
        self.gender_dist = indicator
        self.race_dist = indicator
        self.work_class_dist = indicator
        self.marital_status_dist = indicator
        self.occupation_dist = indicator
        self.relationship_dist = indicator
        self.country_dist = GDP
        self.aggregate_dists = np.linalg.norm

        self.weights = np.ones(11)

    def standard_dist(self, point1, point2):
        dists = [self.age_dist([point1[0]], [point2[0]]), self.education_dist([point1[1]], [point2[1]]),
                 self.hours_dist([point1[2]], [point2[2]]), self.capital_dist([point1[3]], [point2[3]]),
                 self.gender_dist([point1[4]], [point2[4]]), self.race_dist([point1[5]], [point2[5]]),
                 self.work_class_dist([point1[6]], [point2[6]]), self.marital_status_dist([point1[7]], [point2[7]]),
                 self.occupation_dist([point1[8]], [point2[8]]), self.relationship_dist([point1[9]], [point2[9]]),
                 self.country_dist([point1[10]], [point2[10]])];
        dists = np.multiply(np.asarray(dists), self.weights)

        return self.aggregate_dists(dists)

# -------------------------DISTANCE CLASS-------------------------
