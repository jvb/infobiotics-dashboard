def scipy_interpolation_example():
    # http://www.scipy.org/Cookbook/Interpolation
    # The scipy.ndimage package also contains spline_filter and map_coordinates 
    # which can be used to perform N-dimensional interpolation for equally-spaced 
    # data. A two-dimensional example is given below:
    
    from scipy import ogrid, sin, mgrid, ndimage, array
    
    x, y = ogrid[-1:1:5j,-1:1:5j]
    #print x.shape, y.shape # (5, 1) (1, 5)
    fvals = sin(x) * sin(y)
    #print fvals.shape # (5, 5)
    newx, newy = mgrid[-1:1:100j,-1:1:100j]
    #print newx.shape, newy.shape # (100, 100) (100, 100)
    x0 = x[0,0]
    y0 = y[0,0]
    #print x0.shape, y0.shape
    dx = x[1,0] - x0
    dy = y[0,1] - y0
    #print dx.shape, dy.shape
    ivals = (newx - x0) / dx
    jvals = (newy - y0) / dy
    #print ivals.shape, jvals.shape # (100, 100) (100, 100)
    coords = array([ivals, jvals])
    print coords
    print coords.shape # (2, 100, 100)
    
    newf = ndimage.map_coordinates(fvals, coords)
    #print newf.shape # (100, 100)
    
    # To pre-compute the weights (for multiple interpolation results), you would use
    
    coeffs = ndimage.spline_filter(fvals)
    newf = ndimage.map_coordinates(coeffs, coords, prefilter=False)




def interpolatexy(surfacearray, multiplier):
    '''Interpolates an array of surfaces where surfacearray.shape = (x, y, t) 
    and surface at time t = surfacearray[:, :, t]
    
    multipler must be an integer
    
    '''
    xmax = surfacearray.shape[0]# - 1
    ymax = surfacearray.shape[1]# - 1
    interpolated = np.ndarray((xmax * multiplier, ymax * multiplier, surfacearray.shape[2]))
    numx = complex(interpolated.shape[0])
    numy = complex(interpolated.shape[1])
    coords = mgrid[0:xmax:numx, 0:ymax:numy]
    for t in range(interpolated.shape[2]):
        interpolated[:,:,t] = ndimage.map_coordinates(surfacearray[:,:,t], coords, order=1)        
    return interpolated


from scipy import mgrid, ndimage
import numpy as np

def interpolatet(surfacearray, multiplier):
    '''Interpolates an array of surfaces where surfacearray.shape = (x, y, t) 
    and surface at time t = surfacearray[:, :, t]
    
    multipler must be an integer
    
    '''
    xmax = surfacearray.shape[0]# - 1
    ymax = surfacearray.shape[1]# - 1
    interpolated = np.ndarray((xmax, ymax, surfacearray.shape[2] * multiplier))
    print interpolated.shape
#    exit()
    numx = complex(interpolated.shape[0])
    numy = complex(interpolated.shape[1])
    coords = mgrid[0:xmax:numx, 0:ymax:numy, 0:surfacearray.shape[2]:complex(interpolated.shape[2])]
    print coords.shape
#    for t in range(interpolated.shape[2]):
#        interpolated[:,:,t] = ndimage.map_coordinates(surfacearray[:,:,t], coords, order=1)        
    interpolated = ndimage.map_coordinates(surfacearray, coords, order=1)        
    return interpolated


def interpolate(surfacearray, xymultiplier, tmultiplier, order=1):
    '''Interpolates an array of surfaces where surfacearray.shape = (x, y, t) 
    and surface at time t = surfacearray[:, :, t]
    
    xymultipler and tmultiplier must be integers greater than 1
    
    order must be an integer in the range 0-5
    
    '''
    xmax, ymax, tmax = surfacearray.shape 
    interpolated = np.ndarray((xmax * xymultiplier, ymax* xymultiplier, tmax * tmultiplier))
    print interpolated.shape
    numx, numy, numt = (complex(i) for i in interpolated.shape) 
    coords = mgrid[0:xmax:numx, 0:ymax:numy, 0:tmax:numt]
    print coords.shape
    interpolated = ndimage.map_coordinates(surfacearray, coords, order=1)        
    return interpolated

if __name__ == '__main__':
#    npzfile = np.load('/home/jvb/Desktop/ThreeLayers.h5_surfaces.npz')
#    FP1 = npzfile['FP1']
#    #print FP1.shape # (132, 42, 135)
#    #print FP1[:,:,132]
#    FP1 = FP1[46:86,1:-1,-120:] # crop to Central cells only
#    print FP1.shape # (40, 40, 135)
#    interpolated = interpolatet(FP1, 5)
#    print interpolated
#    print interpolated.shape
#    print np.max(interpolated)
    execfile('combined_surfaces.py')
