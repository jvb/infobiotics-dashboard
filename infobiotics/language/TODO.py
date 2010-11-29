# parse deterministic rate constants into stochastic rate constants
rate = '^'
print rate.replace('^', '**')
# see infobiotics.quantities.units.calculators

# default volumes
from volumes import bacterial_cell_volume, arabidopsis_cell_volume
print arabidopsis_cell_volume.rescale('metres ** 3')
print bacterial_cell_volume.rescale('metres ** 3')

