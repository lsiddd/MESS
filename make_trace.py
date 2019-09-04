from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

def main():
    R = 6371

    number_of_users = 200
    number_of_samples = 1000

    filenames = glob("new*.txt")
    user = 0
    outfile = open("SanFrancisco.tcl", "w")

    x_plot = []
    y_plot = []

    for filename in filenames[:number_of_users]:
        print(f"opening file: {filename}")

        with open(filename) as f:
            lines = [i.split() for i in f.readlines()[:number_of_samples] ]

            x_pos = R * cos(float(lines[0][0])) * cos(float(lines[0][1])) + 6300
            y_pos = R * cos(float(lines[0][0])) * sin(float(lines[0][1])) + 800

            second = 0

            outfile.write("$node_({}) set X_ {}\n".format(user, x_pos))
            outfile.write("$node_({}) set Y_ {}\n".format(user, y_pos))
            outfile.write("$node_({}) set Z_ 1\n".format(user))

            for line in lines:
                x_pos = R * cos(float(line[0])) * cos(float(line[1])) + 6300
                y_pos = R * cos(float(line[0])) * sin(float(line[1])) + 800
                x_plot.append(x_pos)
                y_plot.append(y_pos)

                outfile.write(f'$ns_ at {float(second)} "$node_({user}) setdest {x_pos} {y_pos} 1"\n')

                second += 1

            user += 1

    outfile.close()

    plt.figure()
    plt.scatter(x_plot, y_plot)
    plt.show()

if __name__ == "__main__":
    main()

