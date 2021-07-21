import h5py
import matplotlib.pyplot as plt
from glob import glob
from obspy.geodetics import gps2dist_azimuth
from pandas import read_csv
import numpy as np

# ----------------------------------------------------------------------------
# input
# ----------------------------------------------------------------------------
ref_station = 87  # pandas uses numbers to represent numbers from csv file
bp = "1"
cl = "1"
files = glob("data/natasha_stacks1/*bp{}_cl{}.h5".format(bp, cl))
lagmax = 10
trace_scaling = 3
print(files)
# metadata:
station_info = read_csv("stationlist.csv")
# maybe if we want to restrict to some stations include a list here...then skip the other stations
# stations = []
lag = np.linspace(-100, 100, 4001)
# ----------------------------------------------------------------------------
# end input
# ----------------------------------------------------------------------------

location_ref = [station_info.loc[station_info.sta==ref_station, "lat"].values[0],
                station_info.loc[station_info.sta==ref_station, "lon"].values[0]]
print(location_ref)
traces = []
locations = []
distances = []

for file in files:
    print(file)
    d = h5py.File(file, "r")["corr_windows"]["data"][:]

    # we could resample here to higher sampling e.g. 50 Hz

    # then append
    station = int(file.split(".")[1])  # when reading from csv, numbers are automatically interpreted as numbers by pandas..
    print(station)
    lat = station_info.loc[station_info.sta==station, "lat"].values[0]
    lon = station_info.loc[station_info.sta==station, "lon"].values[0]
    print(lat, lon)
    locations.append([lat, lon])
    distances.append(gps2dist_azimuth(lat, lon, *location_ref)[0] / 1000)
    print(distances[-1])
    traces.append(d[0])

for i, t in enumerate(traces):
    # could color code by longitude..
    plt.plot(t * trace_scaling + distances[i], lag, color="k", linewidth=1, alpha=0.5) 
plt.ylim([-lagmax, 0])
plt.xlim([min(distances), max(distances)])
plt.show()