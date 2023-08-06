import os, sys
import timeit
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, cdist, squareform
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
#from geopy.distance import geodesic
#from geographiclib.geodesic import Geodesic

sys.path.append('../')
from sklearn_geokernels.geodesics import geodesic_vincenty
# import geodesic kernels from sklearn_geokernels (as drop in for sklearn.gaussian_process.kernels):
from sklearn_geokernels.kernels import RBF_geo, Matern_geo, RationalQuadratic_geo, WhiteKernel, RBF, Matern



def make_simdata1(n_samples, noise = 0., random_state = None):
    """Generate regression problem.
    Inputs `X` are independent features uniformly distributed on the interval
    [-pi/2, pi/2] for the first, [pi, -pi] for  second, and [0,1] for third dimension. 

    The output `y` is created according to the formula::
        y(X) = 10 * sin(pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + noise * N(0, 1).

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.
    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.
    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The input samples.
    y : ndarray of shape (n_samples,)
        The output values.

    """
    np.random.seed(random_state)
    X = np.random.rand(n_samples, 3)
    X[:,0] = (X[:,0] - 0.5) * 0.1 * np.pi  
    X[:,1] = (X[:,1] - 0.5) * 0.1 * np.pi
    #X[:, 2] = X[:, 2] * 1.0
    y = 10 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + noise * np.random.rand(n_samples)
    return X, y


def test_RBF_geo(kernel_name = 'RBF_geo', n_samples= 200, plot=False):
    """
    Test of Gaussian Process regression with geodesic kernels

    This test automatically generates a 3D dataset and fits a Gaussian Process.

    Parameters
    ----------
    kernel_name : str, accepted: 'RBF_geo' (default), 'Matern_geo', or 'RationalQuadratic_geo'
    n_samples : int, default=200
    plot : bool, default=False
    """
    # Generate test data
    X, y = make_simdata1(n_samples, noise = 0.2, random_state =0)
    # Convert X to Latitude and Longitude coordinates in degree
    X[:,0:2] *= 180/np.pi
    # split in train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    # test anisotropic length_scale
    if kernel_name == 'RBF_geo':
        print('Test: RBF_geo')
        kernel = 1.0 * RBF_geo(length_scale = [1e5,1], 
        length_scale_bounds = [(1e4, 1e7),(0.1, 1e4)]) + WhiteKernel(noise_level_bounds=(1e-3, 1e2))
    elif kernel_name == 'Matern_geo':
        print('Test: Matern_geo')
        kernel = 1.0 * Matern_geo(length_scale = [1e5,1], 
        length_scale_bounds = [(1e4, 1e7),(0.1, 1e4)]) + WhiteKernel(noise_level_bounds=(1e-3, 1e2))
    elif kernel_name == 'RationalQuadratic_geo':
        print('Test: RationalQuadratic_geo')
        kernel = 1.0 * RationalQuadratic_geo(length_scale = 1, 
        length_scale_bounds = (1e-1, 1e4)) + WhiteKernel(noise_level_bounds=(1e-3, 1e2))
    else:
        print(f'Kernel name {kernel_name} not accepted. \
            Please choose from: RBF_geo, Matern_geo, or RationalQuadratic_geo.')
    #kernel = 1.0 * RBF(length_scale = [1,1,1], length_scale_bounds = (0.1, 1e4)) + WhiteKernel(noise_level_bounds=(1e-3, 1e2))
    start = timeit.default_timer()
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3)
    gp.fit(X_train, y_train)
    fitstop = timeit.default_timer()
    print(f'Fitting time: {(fitstop - start):.2f} seconds')
    y_pred, y_std = gp.predict(X_test, return_std=True)
    stop = timeit.default_timer()
    print(f'Prediction time: {(stop - fitstop):.2f} seconds')
    print(f'RMSE: {np.sqrt(np.nanmean((y_pred - y_test)**2)):.4f}')
    print(f'R^2 : {gp.score(X_test, y_test):.4f}')
    if plot:
        plt.clf()
        plt.errorbar(y_test, y_pred, yerr = y_std, label='Test data', fmt="o")
        plt.xlabel('Y true')
        plt.xlabel('Y prediction')
        plt.legend()
        plt.show()


# Load sample data
inpath = '../samples'   
fname = os.path.join(inpath,'SyntheticData_quadratic_10nfeatures_2022-03-29_grid_100sample.csv')
data = pd.read_csv(fname)

X = data[['Easting', 'Northing', 'Feature_1']].values
X -= X.mean(axis=0)
y = data['Ytarget'].values

# Time it
start = timeit.default_timer()
kernel = RBF_geo(length_scale = [2,1], length_scale_bounds = (1e-1, 1e2)) + WhiteKernel(noise_level_bounds=(1e-4, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3)
gp.fit(X, y)
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.2f} seconds')
y_pred, MSE = gp.predict(X, return_std=True)


# Time it
start = timeit.default_timer()
kernel = RBF(length_scale = [2,2,1], length_scale_bounds = (1e-2, 1e3)) + WhiteKernel(noise_level_bounds=(1e-4, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3)
gp.fit(X, y)
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.2f} seconds')
y_pred2, MSE2 = gp.predict(X, return_std=True)


# Time it
start = timeit.default_timer()
kernel = Matern_geo(length_scale = [2,1], length_scale_bounds = (1e-1, 1e2)) + WhiteKernel(noise_level_bounds=(1e-4, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3)
gp.fit(X, y)
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.2f} seconds')
y_pred, MSE = gp.predict(X, return_std=True)


# Time it
start = timeit.default_timer()
kernel = RationalQuadratic_geo(length_scale = 1., length_scale_bounds = (1e-1, 1e2)) + WhiteKernel(noise_level_bounds=(1e-4, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3)
gp.fit(X, y)
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.2f} seconds')
y_pred, MSE = gp.predict(X, return_std=True)

def _check_length_scale(X, length_scale):
    length_scale = np.squeeze(length_scale).astype(float)
    if np.ndim(length_scale) > 1:
        raise ValueError("length_scale cannot be of dimension greater than 1")
    if np.ndim(length_scale) == 1 and X.shape[1] != length_scale.shape[0]:
        raise ValueError(
            "Anisotropic kernel must have the same number of "
            "dimensions as data (%d!=%d)" % (length_scale.shape[0], X.shape[1])
        )
    return length_scale

def _check_length_scale_geodesic(X, length_scale):
    length_scale = np.squeeze(length_scale).astype(float)
    if X.shape[1] < 2:
        raise ValueError("X must have at least 2 features: Latitude, Longitude")
    if np.ndim(length_scale) > 1:
        raise ValueError("length_scale cannot be of dimension greater than 1")
    if np.ndim(length_scale) == 1 and X.shape[1] != length_scale.shape[0]:
        raise ValueError(
            "Anisotropic kernel must have the same number of "
            "dimensions as data (%d!=%d)" % (length_scale.shape[0], X.shape[1])
        )
    return length_scale


def test_distance(X, length_scale = 1.0):
    length_scale = _check_length_scale(X, length_scale)
    Y = X
    if np.size(length_scale) == 1:
        length_scale = np.ones(X.shape[1]) * length_scale
    pdists = (
        pdist(X[:,:2] / length_scale[:2], metric = lambda u, v: geodesic(u, v).meters**2) + 
        pdist(X[:,2:] / length_scale[2:],  metric = 'seuclidean')
    )
    cdists = (
        cdist(X[:,:2] / length_scale[:2], Y[:,:2] / length_scale[:2],
            metric = lambda u, v: geodesic(u, v).meters**2) +
            cdist(X[:,2:] / length_scale[2:], Y[:,2:] / length_scale[2:],  metric = 'seuclidean')
    )
    assert np.size(squareform(pdists)) == np.size(cdists) == len(X)**2




start = timeit.default_timer()
pdist(X[:,:2], metric = lambda u, v: geodesic(u, v).meters)
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.3f} seconds')
# Fitting time: 0.552 seconds

start = timeit.default_timer()
dist1 = pdist(X[:,:2], metric = lambda u, v: geodesic_harvesine(u, v))
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.3f} seconds')
Fitting time: 0.041 seconds

start = timeit.default_timer()
dist2 = pdist(X[:,:2], metric = lambda u, v: _geodesic2(u, v))
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.3f} seconds')
#Fitting time: 0.380 seconds

start = timeit.default_timer()
dist3 = pdist(X[:,:2], metric = lambda u, v: geodesic_vincenty(u, v))
stop = timeit.default_timer()
print(f'Fitting time: {(stop - start):.3f} seconds')
#Fitting time: 0.04 seconds

# WINNER: _geodesic_vincenty (10 and 14 times faster than geographiclib and geopy, respectively)
# second: _geodesic_harvesine (9 and 13 times faster than geographiclib and geopy, respectively), but also less accurate