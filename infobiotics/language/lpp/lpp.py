from enthought.traits.api import HasTraits, Str, List, Lattice, Dict, Int
from sps import SPsystem
from lat import Lattice

class LPPsystem(HasTraits):
	name = Str
	SPsystems = List(SPsystem)
	lattice = Lattice
	spatialDistribution = Dict(Str,Dict(Str, List(Int)))


from IFFL import IFFL
from onePointLattice import onePoint

l = LPPsystem(
	name='IFFLModel',
	SPsystems = [
		IFFL(name='IFFL'),	
	],
	lattice = onePoint,
	spatialDistribution = {
		'IFFL':dict(
			x=0,
			y=0,
		),
	},
)	