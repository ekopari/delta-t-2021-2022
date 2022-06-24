import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import csv
import time
import dateutil
import data_series
from matplotlib.widgets import Slider, Button


def degrees(s):
    parts = s.split()
    degrees = float(parts[0][:-3])
    minutes = float(parts[1][:-1])
    seconds = float(parts[2][:-1])
    return degrees + minutes/60 + seconds/3600



fig = plt.figure(1 , figsize=(10, 5))
ax = fig.add_subplot(2, 1, 1, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(2,1,2)
ax.stock_img()

plt.subplots_adjust(bottom=0.25)

csvdata = []

with open("data.csv","r") as csvf:
    reader = csv.reader (csvf)
    for row in reader:
        if reader.line_num == 1:
            continue
        csvdata += [row]

axtime = plt.axes([0.25, 0.1, 0.65, 0.03])
time_slider = Slider(
    ax=axtime,
    label='Time',
    valmin=0,
    valmax=len(csvdata)-1,
    valinit=0,
)

"""
x_points = []
y_points = []
for i in range(len(csvdata)):
    x_points += [i]
    y_points += [float(csvdata[i][3])]
ax2.plot(x_points,y_points,c="green",label="nr")
ax2.legend(loc="lower right")
ax2.set_title("Pressure")
ax2.set_ylabel("hPa")
"""

with open("data.csv", "r") as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            columns = row[1:len(row)]


"""
for col in columns:
    ax2 = fig.add_subplot(2,1,2)
    series1 = data_series.DataSeries(str(col), "", [str(col)])
    series1.fill_chart(ax2)
    time.sleep(10)"""


light_series = data_series.DataSeries("Light" ,"", ["color clear"])
gyro_series = data_series.DataSeries("Gyro" ,"", ["gyro x","gyro y","gyro z"])
pressure_series = data_series.DataSeries("Pressure" ,"hPa", ["Pressure"])
pressure_series.fill_chart(ax2)

map_initialised = False

def update_time(val):
    global map_initialised
    global ns
    global point
    global point_pressure
    row = csvdata[int(val)]
    date = row[0]
    date = dateutil.parser.parse(date)
    lat = row[19]
    lat = degrees(lat)
    lon = row[20]
    lon = degrees(lon)
    ax.set_title(f'ISS position at {date}')
    if map_initialised : 
        ns.remove()
        point.remove()
        point_pressure.remove()
    ns = ax.add_feature(Nightshade(date, alpha=0.2))
    point = ax.scatter(lon , lat , c="red")
    point_pressure = ax2.axvline(val)
    fig.canvas.draw_idle()
    map_initialised = True



time_slider.on_changed(update_time)



plt.show()
