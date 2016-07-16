import pandas as pd
import numpy as np

cols = ['dropoff_x', 'dropoff_y', 'trip_distance']

df = pd.read_csv('nyc_taxi.csv', usecols=cols).dropna(axis=0)

np.savez('taxi', x=df['dropoff_x'], y=df['dropoff_y'])