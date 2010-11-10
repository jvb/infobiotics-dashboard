from enthought.traits.api import HasTraits, This, Symbol, List, Str, Instance, Disallow, Callable, Either, Int, Float

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
		
def reaction(reactants, products, constant):
	return Reaction(reactants, products, constant)
#print reaction('a,b',['c'], 0.1)

# shorthand. Alternatively 'import reaction as r'
r = Reaction

#class Compartments(HasTraits):
#    compartments = List(Instance('Compartment'))    
Compartments = List(Instance('Compartment'))

#class Compartment(HasTraits):
#	compartments = Compartments

## using Python (?) import symbols
#class Compartment(HasTraits):
#	from_ = Symbol

def get_attributes_list(self, name):
	''' Returns the list of attribute values for attributes whose
	names start with 'name'. '''
	attributes = []
	for d in (self.__dict__, self.__class__.__dict__):
		for key, value in d.iteritems():
			if key.startswith(name):
				attributes.append(value)
	return attributes

def get_attributes_dict(self, name):
	''' Returns dictionary of attribute names and values whose 
	names start with 'name', with names stripped of 'name' 
	and a leading underscore. '''
	attributes = {}
	for d in (self.__dict__, self.__class__.__dict__):
		for key, value in d.iteritems():
			if key.startswith(name):
				key = key.split(name)[1]
#				key.strip('_') # doesn't work for some reason
				if key[0] == '_':
					key = key[1:]
				attributes[key]=value
	return attributes


# using trait attribute name wildcards http://code.enthought.com/projects/traits/docs/html/traits_user_manual/advanced.html#wildcard-rules
class Compartment(HasTraits):
	
	_ = Disallow # e.g HasStrictTraits http://code.enthought.com/projects/traits/docs/html/traits_user_manual/advanced.html#hasstricttraits

	compartment_ = Either(Instance(This), Callable)
	reaction_ = Either(Instance(Reaction))#, Callable)
	species_ = Int

	def _compartments_values(self):
		return get_attributes_list(self, 'compartment')

	def _compartments_names_and_values(self):
		return get_attributes_dict(self, 'compartment')
	
	def _reactions_values(self):
		return get_attributes_list(self, 'reaction')
	
	def _reactions_names_and_values(self):
		return get_attributes_dict(self, 'reaction')

	def _species_values(self):
		return get_attributes_list(self, 'species')
	
	def _species_names_and_values(self):
		return get_attributes_dict(self, 'species')
	
	def reactions(self):
		reactions = []
		for reaction in self._reactions_values():
			if callable(reaction):
				print reaction; continue #FIXME skips the remainder of this suite
				returned = reaction(self) #TODO how can I distinguish between methods, functions and lambdas?
				if returned is not None:
					if hasattr(returned, '__iter__'): 
						for r in returned:
							if isinstance(r, Reaction):
								reactions.append(r)
			else:
				reactions.append(reaction)
		return reactions
				
	volume = Float #TODO make into a litre/length**3 validated Trait


# inheritable

class Compartment1(Compartment):
	reaction1 = Reaction(reactants=['a'],products=['b'])
	reaction2 = Reaction(reactants=['c'],products=[''])

class Compartment2(Compartment1):
	reaction1 = Reaction(reactants=['c'],products=['d'])
	reaction2 = None # nullify reactions in superclasses with None
		
class Compartment3(Compartment1):
	def reaction1(self): 
		return Reaction('x,y','z')
	reaction2 = lambda: Reaction(['e'],['f'])
	constantX = 1.0
	reactionX = Reaction('x','y',constantX)
	

# Modules == Compartments?
# multiple inheritance uses first superclasses definition of initial amounts

# parameterising reactions and modules/compartments...


#def test(arg, **kwargs):
#	print arg, kwargs
#
#test(**{'t':0})



if __name__ == '__main__':
	
	print 'c1'
	c1 = Compartment1()
#	c1.print_traits()
	print c1.reaction1
	assert c1.reaction_ == None
	print c1.reaction2
	print
	
	print 'c2'
	c2 = Compartment2()
#	c2.print_traits()
	print c1.reaction1
	print c2.reaction2
	print
	
	print 'c3'
	c3 = Compartment3()
	c3.print_traits() # print_traits() doesn't print attributes that were assigned at class definition time but they are still type checked
	print c3.reaction1; print c3.reaction1()
	print c3.reaction2
	print
	
	print 'c4'
	def function():
		pass
	c4 = Compartment3(
		reactionTest=Reaction(reactants=['f'],products=['g','h']),
		reaction_function=function,
		species_A=2
	)
	c4.print_traits() # print_traits does print attributes that were assigned at class instantiation time
	print
	
	print c4._reactions_names_and_values()
	print c4._species_names_and_values()
	
	print c4.reactions()
	
