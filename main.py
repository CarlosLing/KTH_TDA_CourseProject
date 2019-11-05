import pandas as pd
import numpy as np

from utils import read_data

if __name__ == '__main__':

    data = read_data('adult.data', gdp_file='GDP_percapita_complete.csv')

