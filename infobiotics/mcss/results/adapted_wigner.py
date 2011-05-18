from __future__ import division
#import sip; sip.setapi('QString', 2)
from enthought.etsconfig.api import ETSConfig; ETSConfig.toolkit = 'qt4'
 
import mcss_results
results = mcss_results.McssResults('tests/pulsePropagation-2_runs.h5')
#print results.species_information(); exit()
species = 'proteinGFP', 'proteinCI', 'proteinLuxI'
results.select_species(*species)
surfaces = results.surfaces()
#print surfaces.shape
time_index = 50
(xmin, xmax), (ymin, ymax) = results.xy_min_max()
def _min_max_generator(xmin, xmax, ymin, ymax):
    size = xmax - xmin if xmax - xmin < ymax - ymax else ymax - ymin
    min = 0
    max = min + size
    yield min, max
    while True:
        min = min + 2 * size
        max = min + size
        yield min, max
min_max_generator = _min_max_generator(xmin, xmax, ymin, ymax)

from enthought.mayavi import mlab
mlab.figure(
    1,
    size=(800, 640),
    fgcolor=(1, 1, 1),
    bgcolor=(0.5, 0.5, 0.5),
)
mlab.clf()

if xmax - xmin > ymax - ymin:
    longest = 'x'
    zmax = ymax + ymin
else:
    longest = 'y'
    zmax = xmax + xmin

zmin = 0

import numpy as np
for i, species in enumerate(species):
    surface = mcss_results.mean(surfaces, 0)[i]
#    zmax = np.max(surface)

    min, max = min_max_generator.next()
        
    n = len(species)
        
    if longest == 'x':
        ymin = min
        ymax = max
    else:
        xmin = min
        xmax = max
        
    extent = [
        xmin,
        xmax,
        ymin,
        ymax,
        zmin,
        zmax,
    ]
    
    surf = mlab.surf(surface[:, :, time_index], extent=extent)
#    mlab.outline(surf, extent=extent)
    mlab.axes(
        surf,
        color=(.7, .7, .7),
        extent=extent,
#        ranges=(0, 1, 0, 1, 0, 1),
        xlabel='',
        ylabel='',
        zlabel='',
        x_axis_visibility=False,
#        y_axis_visibility=False,
        z_axis_visibility=False,
    )
    mlab.text(xmax + xmax / 3, ymax - ((ymax - ymin) / 2), species, z=zmin, width=0.13)
#    mlab.text3d(xmax + xmax / 3, ymax - ((ymax - ymin) / 2), zmin, species)

quantities_display_units = 'molecules'
mlab.title(quantities_display_units)
mlab.orientation_axes()
mlab.view(45.0, 65, 115, np.array([ 15., 25., 5.]))
mlab.show()
