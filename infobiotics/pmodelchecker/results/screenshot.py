from enthought.mayavi import mlab
mlab.test_plot3d()
arr = mlab.screenshot()
import pylab as pl
pl.imshow(arr)
pl.axis('off')
pl.show()