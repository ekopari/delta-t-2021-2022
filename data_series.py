import csv
import random

csvdata = []
col_names = ["Temperature"]

with open("data.csv","r") as csvf:
    reader = csv.reader (csvf)
    for row in reader:
        if reader.line_num == 1:
            col_names = row
            continue
        csvdata += [row]

columns = []

for col_i in range(len(col_names)):
    col_name = col_names[col_i]
    col_data = []
    for row_i in range(len(csvdata)):
        data = csvdata[row_i][col_i]
        col_data += [data]
    columns += [(col_data ,col_name)]

class DataSeries:
    def __init__(self,title,unit,col_names):
        self.title = title
        self.unit = unit
        self.col_names = col_names
        self.data = []
        for col_name_ in col_names:
            for col in columns:
                if col[1] == col_name_:
                    self.data += [col[0]]
    def fill_chart(self, ax):
        for series_i in range(len(self.data)):
            x_points = []
            y_points = []
            #print(len(self.data[series_i]))
            for i in range(len(self.data[series_i])):
                x_points += [i]
                y_points += [float(self.data[series_i][i])]
            ax.plot(x_points,y_points,c=["green", "red", "blue", "yellow", "pink", "black"][series_i],label=self.col_names[series_i])
            ax.legend()
            ax.set_title(self.title)
            ax.set_ylabel(self.unit)
            print(len(x_points))

#return DataSeries("text", "text1", ["Temperature", "Humidity"])

