import sys

import numpy as np

import pandas
import matplotlib.pyplot as plt

# The following is needed to register the axes
import mpl_scatter_density  # noqa

from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

if len(sys.argv) != 2:
    print("Example usage: python example_taxi.py yellow_tripdata_2016-05.csv")
    print("You can get the data at: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml")
    sys.exit(1)

filename = sys.argv[1]

print("Reading file (this typically takes 10-20 seconds)...")
df = pandas.read_csv(filename, usecols=['dropoff_longitude', 'dropoff_latitude']).dropna(axis=0)
x = df['dropoff_longitude']
y = df['dropoff_latitude']

print("Done reading file, making plot")

norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

ax = plt.subplot(1, 1, 1, projection='scatter_density')

xmin = -74.15
xmax = -73.75
ymin = 40.62
ymax = 40.85

aspect = 1 / np.cos(np.radians(0.5 * (ymin + ymax)))

ax.scatter_density(x, y, cmap='plasma', norm=norm)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel
ax.set_aspect(aspect)

plt.show()
