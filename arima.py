from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from pandas.plotting import autocorrelation_plot
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

def arima():

    mse = []

    for i in range (200):
        observations_x = read_file("./SanFrancisco.tcl", i, "x")

        size = int(len(observations_x) * 0.26)
        train, test = observations_x[0:size], observations_x[size:len(observations_x)]
        history = [x for x in train]
        predictions_x = []

        for i, v in enumerate(test):
            model = ARIMA(history, order=(5,1,0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            # print(model_fit.summary())
            yhat = output[0]
            predictions_x.append(yhat)
            obs = v
            history.append(obs)

        error = mean_squared_error(test, predictions_x)
        # print('Test MSE: %.3f' % error)
        mse.append(error)

    return error

def kalman():
    error = []
    for i in range (200):
        observations_x = read_file("./SanFrancisco.tcl", i, "x")
        observations_y = read_file("./SanFrancisco.tcl", i, "y")

        kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                          transition_covariance=0.01 * np.eye(2))
        states_pred_x = kf.em(observations_x).smooth(observations_x)[0]
        states_pred_y = kf.em(observations_y).smooth(observations_y)[0]

        mse = sum((states_pred_x[:, 0] - observations_x)**2) / len(observations_x)
 
        # return (states_pred_x[:,0], states_pred_y[:,0])
        error.append(mse)
    return error

arima_preds = arima()
kalman_preds = kalman()

print(np.mean(arima_preds))
print(np.mean(kalman_preds))
