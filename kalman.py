from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np

def read_file(filename, node_id, coord = "x"):
    with open(filename) as f:
        if coord == "x":
            lines = [float(i.split()[5]) for i in f.readlines() if
                     "node_({})".format(node_id) in i
                    and "setdest" in i]
        elif coord == "y":
            lines = [float(i.split()[6]) for i in f.readlines() if
                     "node_({})".format(node_id) in i
                    and "setdest" in i]
        else:
            raise ValueError("invalid coordinate")
        return lines

def kalman():
    for i in range (1):
        observations_x = read_file("./SanFrancisco.tcl", i, "x")
        observations_y = read_file("./SanFrancisco.tcl", i, "y")

        kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                          transition_covariance=0.01 * np.eye(2))
        states_pred_x = kf.em(observations_x).smooth(observations_x)[0]
        states_pred_y = kf.em(observations_y).smooth(observations_y)[0]

        mse = sum((states_pred_x[:, 0] - observations_x)**2) / len(observations_x)
        print(mse)
        print(states_pred_x)
        
        plt.style.use("ggplot")
        plt.grid(True)
        plt.plot(states_pred_x[:, 0], label="predicted data")
        plt.plot(observations_x, label="observations")
        # plt.scatter(states_pred_x[:, 0][10:], states_pred_y[:, 0][10:], label="predicted data")
        # plt.scatter(observations_x[10:], observations_y[10:], label="raw data")
        plt.legend()
        plt.figure()
        plt.plot(observations_x - states_pred_x[:,0], label="X coordinate error")
        plt.plot(observations_y - states_pred_y[:,0], label="Y coordinate error")
        plt.legend()
        plt.show()
