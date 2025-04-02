#!/usr/bin/python3 

import numpy as np
import scipy as sp
import xarray as xr
import pandas as pd
import dask.array as da

from itertools import product


def velocity_field(x, y, z):
    return np.array([0, (x-100.)*(x+100.)-20., y-20.])

def structure(coordinates, spacing, point = None, axes_names = None):
    if point == None:
        point = spacing
    if axes_names == None:
        axes_names = ["x", "y", "z"]
    extremes = np.append(np.min(coordinates, 0), np.max(coordinates, 0))
    double_spacing = np.append(spacing, spacing)
    double_point = np.append(point, point)
    ndims = spacing.size
    BB = np.transpose((np.floor(np.divide(extremes-double_point+double_spacing/2, double_spacing))*double_spacing + double_point).reshape(2, ndims))
    axes = [np.arange(BB[i, 0], BB[i, 1], spacing[i]) for i in range(ndims)]
    shape = list(i.size for i in axes)
    cube = xr.DataArray(name='cube', data=da.empty(shape, dtype='bool'),
                        dims=axes_names, coords={axes_names[i]: axes[i] for i in range(ndims)})
    cube.assign_attrs({'spacing': spacing, 'BB': BB})
    return cube

def polynomial(coordinates, grade):
    l = list(set(product(set(range(grade + 1)),repeat = 3)))
    l.sort()
    matr = np.array(l)
    matr= matr[np.sum(matr, 1)<=grade, :]
    return np.multiply(np.multiply((np.array(coordinates[:, 0])[:, None]** np.array(matr[:, 0])[None, :]), (np.array(coordinates[:, 1])[:, None]** np.array(matr[:, 1])[None, :])), (np.array(coordinates[:, 2])[:, None]** np.array(matr[:, 2])[None, :])).reshape((coordinates.shape[0], matr.shape[0]))

#punti in (-1, 1)x(-1, 1), z= y/4
n_punti = 10000
n_sensori = 2

sens_1_punti = 1000*np.random.rand(n_punti, 3)
sens_2_punti = 1000*np.random.rand(n_punti, 3)
punti = np.zeros((sens_1_punti.shape[0]+sens_2_punti.shape[0], sens_1_punti.shape[1]))
for i in range(sens_1_punti.shape[1]):
    punti[:, i] = np.append(sens_1_punti[:, i], sens_2_punti[:, i])
cube = structure(punti, np.array([0.1, 0.2, 0.3]))


#print(reticolo(sens_1_punti, sens_2_punti, 0.1))
#da = xr.DataArray(
#    np.random.rand(4, 2),
#    [
#        ("x", punti[0, :]),
#        ("y", punti[])
#        ("gruppo", np.arange(n_sensori)),
#    ],
#)

coeff = 10*np.random.rand(n_sensori* 3) 

velocità = np.array([])
for i in range(n_punti):
    punti[i, 2] = punti[i, 1]/4
    velocità = np.append(velocità, velocity_field(punti[i, 0], punti[i, 1], punti[i, 2]))
print(polynomial(punti, 3))
dir_1 = np.array([1., 1., 0.])
dir_1 /= np.linalg.norm(dir_1)
dir_2 = np.array([1., 2., 2.])
dir_2 /= np.linalg.norm(dir_2)
dir_3 = np.array([0., 1., 1.])
dir_3 /= np.linalg.norm(dir_3)

direzioni = np.append(dir_1, dir_2)
direzioni = np.append(direzioni, dir_3)
coordinate  = np.transpose(np.copy(punti))
coordinate[2, ] = np.ones(n_punti)

row = np.array([], dtype=int)
column = np.array([], dtype=int) 

data = np.array([])
A = sp.sparse.coo_matrix((data, (row, column)), shape=(max(n_sensori*n_punti, 3*(n_sensori+n_punti)), max(n_sensori*n_punti, 3*(n_sensori+n_punti))))
incognite = np.append(velocità, coeff)

#misure = A@incognite


#ans = sp.sparse.linalg.spsolve(A, misure)