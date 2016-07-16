import os
import sys

import pandas as pd
import numpy as np

if not os.path.exists('nyc_taxi.csv'):
    print("You need to download the NYC taxi data first (into a file called nyc_taxi.csv)")
    sys.exit(1)

cols = ['dropoff_x', 'dropoff_y', 'trip_distance']

df = pd.read_csv('nyc_taxi.csv', usecols=cols).dropna(axis=0)

np.savez('taxi', x=df['dropoff_x'], y=df['dropoff_y'])
