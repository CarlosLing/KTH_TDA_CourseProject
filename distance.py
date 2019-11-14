import pandas as pd
import numpy as np

AGE_RANGE = 73
EDUCATION_RANGE = 15
HPW_RANGE = 98
CAPITAL_RANGE = 104355
RELATIONSHIP_RANGE = 4
GDP_RANGE = 29126.373789999998


def dist(a, b):

    """ Computes the distance between two different entries of a dataset a and b

    The methodology to compute the distances simply computes the distances regarding different variables, and computes
    the Mean Square Distance"""

    # Individual distances

    # Continuous variables
    Age = abs(a.Age - b.Age) / AGE_RANGE
    Education = abs(a.EducationNum - b.EducationNum) / EDUCATION_RANGE
    HoursPerWeek = abs(a.HoursPerWeek - b.HoursPerWeek) / HPW_RANGE
    NetCapital = abs(a.NetCapital - b.NetCapital) / CAPITAL_RANGE

    # Discrete distances
    Gender = 1 * (a.Gender != b.Gender)
    Race = 1 * (a.Race != b.Race)

    # The following distances might admit a map
    WorkClass = 1 * (a.WorkClass != b.WorkClass)
    MaritalStatus = 1 * (a.MaritalStatus != b.MaritalStatus)
    Occupation = 1 * (a.Occupation != b.Occupation)

    # Check this distances
    # Categorical distances with mapping
    Relationship = abs(a.RelationshipMap != b.RelationshipMap) / RELATIONSHIP_RANGE
    Country = abs(a.GDP_PC - b.GDP_PC) / GDP_RANGE

    distance = np.sqrt(Age**2 + Education**2 + Gender**2 + WorkClass**2 + MaritalStatus**2 +
                       Occupation**2 + Relationship**2 + HoursPerWeek**2 + Country**2 + NetCapital**2 + Race**2)

    return distance



def get_distance_matrix(data:pd.DataFrame, N):

    if N > len(data):
        raise ValueError("The Sampling size Exceeds the size of the input data")

    D = np.zeros((N,N))

    sampled_data = data.sample(N)

    for i in range(N):
        for j in range(i):
            d = dist(sampled_data.iloc[i], sampled_data.iloc[j])
            D[i, j] = d
            D[j, i] = d

    return D, sampled_data
