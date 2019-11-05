import pandas as pd
import os


def read_data(file, gdp_file):
    path = os.path.expanduser(file)
    path_gdp = os.path.expanduser(gdp_file)

    df = pd.read_csv(path, header=None, sep=', ')
    df.columns = [
        "Age", "WorkClass", "fnlwgt", "Education", "EducationNum",
        "MaritalStatus", "Occupation", "Relationship", "Race", "Gender",
        "CapitalGain", "CapitalLoss", "HoursPerWeek", "NativeCountry", "Income"
    ]

    df['NetCapital'] = df.CapitalGain - df.CapitalLoss
    df = df.drop(['Education', 'CapitalGain', 'CapitalLoss'], 1)

    gdp_data = pd.read_csv(path_gdp)
    df_gdp = pd.merge(df, gdp_data, on='NativeCountry', how='left')

    data = df_gdp

    return data

