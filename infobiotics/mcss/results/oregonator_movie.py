species = 'Y2', 'Y3'
#species = 'Y1', 'Y2'
frame_rate = 25
#colourmap = 'RdBu'
#colourmap = 'autumn'
colourmap = 'cool'
#colourmap = 'copper'
tmultiplier = 1
xymultiplier = 1
#xymultiplier = 6
#xymultiplier = 4
tmultiplier = 2
movie_filename = '/home/jvb/simulations/oregonator/oregonator.mov'
filename = '/home/jvb/simulations/oregonator/oregonator.h5'

import numpy as np

from movie import movie

from mcss_results import McssResults, mean

from mcss_results_widget import interpolate


def save_array_as_image(filename, array, colourmap=None, format=None, dpi=1, vmin=None, vmax=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib import cm

    figure = Figure(figsize=array.shape[::-1], dpi=1, frameon=False)
#    canvas = FigureCanvas(figure) # essential even though it isn't used
    FigureCanvas(figure) # essential even though it isn't used
    figure.figimage(array, cmap=cm.get_cmap(colourmap), vmin=vmin, vmax=vmax, origin=origin)
    figure.savefig(filename, dpi=dpi, format=format)


results = McssResults(filename)

results.step = 1

results.start = 240
results.stop = 840

results.select_species(*species)

print 'surfaces'
surfaces = results.surfaces()
print surfaces.shape

numruns, numsurfaces, lenx, leny, numtimepoints = surfaces.shape
numcompartments = lenx * leny

print 'mean over runs'
surfaces = mean(surfaces, 0)
print surfaces.shape        

#print 'Y1'
#surfaces = np.array((surfaces[0], ))
#print 'Y2'
#surfaces = np.array((surfaces[1], ))

print 'subtraction'
surfaces = np.array((surfaces[0] - surfaces[1], ))
print surfaces.shape

print 'interpolation'        
surfaces = np.array([interpolate(surfaces[i], xymultiplier, tmultiplier) for i in range(len(surfaces))])
print surfaces.shape

# setup movie
m = movie(movie_filename, frame_rate=frame_rate)
print m.template

vmin = np.min(surfaces[0])
vmax = np.max(surfaces[0])
    
print 'saving frames', m.tempdir
for ti in range(surfaces.shape[-1]):
    save_array_as_image(m.next_frame(), surfaces[0,:,:,ti], colourmap=colourmap, format='png', vmin=vmin, vmax=vmax)
    
print 'encoding movie', m.filename
encoded = m.encode()

# remove tempdir
del m
        
if not encoded:
    # report error
    exit(m.output)

print 'done'

print 'opening', movie_filename
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QUrl 
QDesktopServices.openUrl(QUrl('file://%s' % movie_filename, QUrl.TolerantMode))
    