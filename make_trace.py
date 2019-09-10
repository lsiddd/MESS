from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos
import random

def main():
    R = 6371

    number_of_users = 50
    number_of_samples = 100
    number_of_cells = 100

    filenames = glob("new*.txt")
    user = 0
    outfile = open("SanFrancisco.tcl", "w")

    x_plot = []
    y_plot = []

    for filename in filenames[:number_of_users]:
        print(f"opening file: {filename}")

        with open(filename) as f:
            lines = [i.split() for i in f.readlines()[:number_of_samples] ]

            x_pos = R * cos(float(lines[0][0])) * cos(float(lines[0][1]))
            y_pos = R * cos(float(lines[0][0])) * sin(float(lines[0][1])) * 10

            # x_plot.append(x_pos)
            # y_plot.append(y_pos * 10)

            second = 0

            outfile.write("$node_({}) set X_ {}\n".format(user, x_pos))
            outfile.write("$node_({}) set Y_ {}\n".format(user, y_pos))
            outfile.write("$node_({}) set Z_ 1\n".format(user))

            for line in lines:
                x_pos = R * cos(float(line[0])) * cos(float(line[1]))
                y_pos = R * cos(float(line[0])) * sin(float(line[1])) * 10

                if (x_pos < -6380 or x_pos > 6280):
                    continue
                if (y_pos > -1000 or y_pos < -9000 ):
                    continue

                x_plot.append(x_pos)
                y_plot.append(y_pos)

                outfile.write(f'$ns_ at {float(second)} "$node_({user}) setdest {x_pos} {y_pos} 1"\n')

                second += 1

            user += 1
    outfile.close()


    cellsFile = open("cellsDataset", "w")
    id = 1
    x = []
    y = []
    for i in random.sample(list(zip(x_plot, y_plot)), number_of_cells):
        x.append( i[0] + random.uniform(-50,50) )
        y.append( i[1] + random.uniform(-400,300) )
        cellsFile.write(f"{id} {x[-1]} {y[-1]}\n")
        id += 1
    cellsFile.close()

    print (np.mean(x_plot))
    print (np.mean(y_plot))
    plt.figure()
    plt.scatter(x_plot, y_plot)
    plt.scatter(x, y, color="green")
    plt.show()

if __name__ == "__main__":
    main()

