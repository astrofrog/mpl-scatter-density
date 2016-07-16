from __future__ import division

import numpy as np
cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t

cimport cython


@cython.boundscheck(False)  # turn off bounds-checking for entire function
def histogram2d(np.ndarray[DTYPE_t, ndim=1] x,
                 np.ndarray[DTYPE_t, ndim=1] y,
                 float xmin, float xmax, float ymin, float ymax,
                 int nx, int ny):

    cdef int n = x.shape[0]

    cdef np.ndarray[DTYPE_t, ndim=2] count = np.zeros([ny, nx], dtype=DTYPE)
    
    cdef int ix, iy
    cdef unsigned int i, j
    cdef float normx, normy
    cdef float tx, ty
    cdef float fnx = float(nx)
    cdef float fny = float(ny)
    
    normx = 1. / (xmax - xmin)
    normy = 1. / (ymax - ymin)
    
    with nogil:
        for i in range(n):
            tx = x[i]
            ty = y[i]
            if tx > xmin and tx < xmax and ty > ymin and ty < ymax:
                ix = int((x[i] - xmin) * normx * fnx)
                iy = int((y[i] - ymin) * normy * fny)
                count[iy, ix] += 1.
    
    return count