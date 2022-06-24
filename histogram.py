import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import struct
import time

histograms_file = "histograms2.bin" 
h = []

fig = plt.figure()
ax = plt.axes(projection="3d")



with open(histograms_file, "rb") as f:
    histogram_bin = f.read()
    #h = memoryview(histogram_bin).cast("f")
    num_len = 4
    for i in range(len(histogram_bin)//num_len):
        start = i * num_len
        end = start + num_len
        h += [struct.unpack("f", histogram_bin[start:end])]


def draw_3d_histogram(time_step):
    b = h[256*time_step:256*(time_step+1)]
    g = h[256*(time_step+1):256*(time_step+2)]
    r = h[256*(time_step+2):256*(time_step + 3)]
    #ax.plot(range(256), b)
    ax.plot3D([time_step]*256, b, range(256), c="blue")
    ax.plot3D([time_step]*256, r, range(256), c="red")
    ax.plot3D([time_step]*256, g, range(256), c="green")



for i in range(2000):
    draw_3d_histogram(i)

plt.show()