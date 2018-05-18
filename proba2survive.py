import pandas as pd
import numpy as np
from IPython import embed

from main import proba2survive



def main():
    df = pd.read_csv('barbare.csv')
    embed()
    proba2survive(df, 1, [], [], {'machado'}, {'potion', 'armor1', 'armor2', 'torche', 'martello', 'machado'})


if __name__ == '__main__':
    main()