import os, sys
import timeit
import numpy as np
import pandas as pd
#from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from scipy.spatial.distance import pdist, cdist, squareform
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.datasets import make_friedman2
#from geopy.distance import geodesic
#from geographiclib.geodesic import Geodesic

sys.path.append('../')
from geokernels.geodesics import geodesic_vincenty, geodesic_harvesine
# import geodesic kernels from sklearn_geokernels (as drop in for sklearn.gaussian_process.kernels)
from geokernels.sklearn_geokernels import RBF, RBF_geo, Matern_geo, RationalQuadratic_geo, WhiteKernel


def gen_testdata(n_samples = 100):
    """
    Generate test data.
    """
    X, y = make_friedman2(n_samples, noise=0., random_state=0)
    # Generate random data
    X = np.random.rand(nsample, 2) * 180 - 90
    # Add random noise
    X[:,0] += np.random.rand(nsample) * 0.1
    X[:,1] += np.random.rand(nsample) * 0.1
    # Latitude: -90 <= lat <= 90
    # Longitude:
    X[:,1] *= 2
    return X

def test_RBF_geo(X, length_scale = 1.0):


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