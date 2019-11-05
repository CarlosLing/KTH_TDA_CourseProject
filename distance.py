import pandas as pd
import numpy as np


def dist(a, b):

    """ Computes the distance between two different entries of a dataset a and b

    The methodology to compute the distances simply computes the distances regarding different variables, and computes
    the Mean Square Distance"""

    # Age
    Age = abs(a.Age - b.Age)
    Education = abs(a.EducationNum - b.EducationNum)
    Gender = 1 * (a.Gender != b.Gender)
    WorkClass = 1 * (a.WorkClass != b.WorkClass)
    MaritalStatus = 1 * (a.MaritalStatus != b.MaritalStatus)
    Occupation = 1 * (a.Occupation != b.Occupation)
    Relationship = 1 * (a.Relationship != b.Relationship)
    HoursPerWeek = abs(a.HoursPerWeek - b.HoursPerWeek)
    Country = abs(a.GDP_PC - b.GDP_PC)
    NetCapital = abs(a.NetCapital - b.NetCapital)

    distance = np.sqrt(Age**2 + Education**2 + Gender**2 + WorkClass**2 + MaritalStatus**2 +
                       Occupation**2 + Relationship**2 + HoursPerWeek**2 + Country**2 + NetCapital**2)

    return distance
