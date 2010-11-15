from enthought.traits.api import *

class Reaction(HasTraits):
	reactants = List(Str)
	products = List(Str)
	constant = Float
	def __str__(self):
		return '%s -> %s' % (self.reactants, self.products)
	def __init__(self, reactants, products, constant=0.0):
		''' Allows instantiation of reactions with only a pair of strings (or lists of strings). '''
		if isinstance(reactants, str):
			reactants = [reactant.strip() for reactant in reactants.split(',')]
		self.reactants = reactants
		if isinstance(products, str):
			products = [product.strip() for product in products.split(',')]
		self.products = products
		self.constant = constant
