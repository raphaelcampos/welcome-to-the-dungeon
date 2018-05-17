import pandas as pd
import numpy as np
from IPython import embed

from main import proba2survive



def main():
    df = pd.read_csv('barbare.csv')
    embed()
    proba2survive(df, 6, [], ['1', '1.1', '2', 'torche', 'armor1'])


if __name__ == '__main__':
    main()