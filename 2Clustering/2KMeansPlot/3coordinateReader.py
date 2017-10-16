import csv
import sys
import matplotlib.pyplot as plt

point_xy = {}
filename = 'dbscan.csv'

def read_file():
    with open(filename, 'rt') as f:
        reader = csv.reader(f)
        featureName_list = next(reader)

        for row in reader:
            key = None
            for j, val in enumerate(row):
                if j == 1:
                    point_xy[val] = []
                    key = val
                if j == 2 or j == 3:
                    point_xy[key].append(val)
        print(point_xy)

def plot():
    cluster0 = [1, 4, 12, 28, 40, 56, 66, 75]
    cluster1 = [5, 6, 8, 10, 11, 14, 16, 17, 19, 20, 21, 22, 25, 26, 29, 30, 31, 32, 34, 37, 38, 39, 42, 45, 46, 47, 48, 49, 50, 52, 53, 54, 60, 63, 64, 68, 69, 70, 71, 72, 74]
    cluster2 = [9, 33, 78]

    for point in cluster0:
        x = point_xy[str(point)][0]
        y = point_xy[str(point)][1]
        plt.plot(x, y, 'ro')

    for point in cluster1:
        x = point_xy[str(point)][0]
        y = point_xy[str(point)][1]
        plt.plot(x, y, 'bo')

    for point in cluster2:
        x = point_xy[str(point)][0]
        y = point_xy[str(point)][1]
        plt.plot(x, y, 'go')
    plt.show()
    
read_file()
plot()