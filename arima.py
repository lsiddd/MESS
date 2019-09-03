from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
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

for i in range (1):
    observations_x = read_file("./SanFrancisco.tcl", i, "x")
    observations_y = read_file("./SanFrancisco.tcl", i, "y")

    size = int(len(observations_x) * 0.26)
    train, test = observations_x[0:size], observations_x[size:len(observations_x)]
    history = [x for x in train]
    predictions = []

    for i, v in enumerate(test):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = v
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    
    plt.style.use("ggplot")
    plt.grid(True)
    plt.plot(test)
    plt.plot(predictions)
    plt.show()
    # plt.scatter(states_pred_x[:, 0][10:], states_pred_y[:, 0][10:], label="predicted data")
    # plt.scatter(observations_x[10:], observations_y[10:], label="raw data")
    # plt.legend()
    # plt.figure()
    # plt.plot(observations_x - states_pred_x[:,0], label="X coordinate error")
    # plt.plot(observations_y - states_pred_y[:,0], label="Y coordinate error")
    # plt.legend()
    # plt.show()
