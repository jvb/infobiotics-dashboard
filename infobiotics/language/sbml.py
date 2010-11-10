from enthought.traits.api import HasTraits, Either, Str, List, Dict, Int, Float, Constant, Instance, Tuple, Property, cached_property, DelegatesTo
from infobiotics.commons.sequences import flatten

Reactants = Either(
    Str,
    List(Str, max_len=2),
    Dict(Str, Int),
)

Products = Either(
    Str,
    List(Str),
    Tuple(Str),
    Dict(Str, Int),
)

class Constant(HasTraits):
    id = Str
    value = Float
#    def __init__(self, id, value, **traits):
#        super(Constant, self).__init__(**traits)
#        self.id = id
#        self.value = value

class Rule(HasTraits):
    reactants_outside = Reactants
    reactants_inside = Reactants
    reactants_label = Str
    products_outside = Products
    products_inside = Products
    products_label = Str
    constant = Either(Float, Instance(Constant), Tuple(Str, Float))
    target = Tuple(Int, Int)
    def _constant_changed(self, value):
        if not isinstance(value, Constant):
            if isinstance(value, tuple):
                self.constant = Constant(value[0], value[1])
            else:
                self.constant = Constant(value=value)


#    def __init__(self, **traits):
#        super(Rule, self).__init__(**traits)
#        if len(self.reactants_inside) == 0:
#            raise ValueError('Rules cannot have zero reactants')
#        if constant < 0:
#            raise ValueError('Rules cannot have negative constants')


#Rule('a', 'b', 0.1).print_traits(); exit()

class Compartment(HasTraits):

    name = Str

    def _name_default(self):
        return self.__class__.__name__

    compartments = List(Instance('Compartment'))

    def __str__(self):
        return '(%s%s)' % (self.name, ', '.join([str(c) for c in self.compartments]))

    rules = List(Rule)

    species_amounts = Dict(Str, Int)

    def update_species_amounts(self, **species_amounts):
        self.species_amounts.update(species_amounts)

class SPsystem(Compartment):
    ''' SPsytem inherits Compartment so it can be reused inside another P 
    system; x and y positions will be ignored. '''
    x = Int
    y = Int


class Bacteria(SPsystem):

    compartments = [
        Compartment(name='cytoplasm'),
    ]

    rules = [
        Rule(reactants_inside='a', products_inside='b', constant=123)#Constant('k_on', 0.1)),
    ]


class OtherBacteria(Bacteria):
    pass

class Medium(SPsystem):
    compartments = [
        Bacteria(),
        OtherBacteria(),
    ]

class LPPsystem(HasTraits):
#    compartments = 
    SPsystems = Either(
        Instance(SPsystem),
        List(Instance(SPsystem)),
        List(List(Instance(SPsystem))),
        List(Tuple(Instance(SPsystem))),
        Tuple(Instance(SPsystem)),
        Tuple(List(Instance(SPsystem))),
        Tuple(Tuple(Instance(SPsystem))),
    )

class Model(LPPsystem):
    SPsystems = [
        [Medium(x=x, y=y, species_amounts={'PQS':10}) for x in range(2) for y in range(1)],
        Bacteria(x=1, y=0,
            species_amounts=dict(
                PQS=5,
                PqsR=3,
            ),
        ),
    ]
#    SPsystems = Bacteria(x=1, y=0)

m = Model()
#print m.SPsystems[-1].rules
#m.print_traits()


def id_generator(prefix=''):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1

compartment_id_generator = id_generator('c')
species_id_generator = id_generator('s')
constant_id_generator = id_generator('k')
reaction_id_generator = id_generator('r')


def recursively_create_compartments(compartment, outside_sbml_compartment):
#    compartment.parent = 
    compartment.id = compartment_id_generator.next()
    sbml_compartment = model.createCompartment()
    sbml_compartment.setId(compartment.id)
    sbml_compartment.setName(compartment.name)
    sbml_compartment.setSize(1)
    sbml_compartment.setUnits('volume')
    sbml_compartment.setSpatialDimensions(3) # required for setOutside below
    sbml_compartment.setOutside(outside_sbml_compartment.getId())
    for compartment in compartment.compartments:
        recursively_create_compartments(compartment, sbml_compartment)


def recursively_create_species(compartment):
    compartment.species_ids = {}
    for species, amount in compartment.species_amounts.iteritems():
        sbml_species = model.createSpecies()
        sbml_species.setName(species)
        species_id = species_id_generator.next()
        compartment.species_ids[species] = species_id
        sbml_species.setId(species_id)
        sbml_species.setCompartment(compartment.id)
        sbml_species.setInitialAmount(amount)
    for compartment in compartment.compartments:
        recursively_create_species(compartment)


def recursively_create_reactions(compartment):
    for rule in flatten(compartment.rules):

        sbml_reaction = model.createReaction()
        sbml_reaction.setId(reaction_id_generator.next())
        sbml_reaction.setReversible(False)
        sbml_reaction.setFast(False)

        if isinstance(rule.constant, Constant):
            constant_value = rule.constant.value
        else:
            constant_value = rule.constant
        if isinstance(rule.constant, Constant) and rule.constant.id != '':
            constant_id = rule.constant.id
        else:
            constant_id = constant_id_generator.next()

        kinetic_law = sbml_reaction.createKineticLaw()
        kinetic_law.setFormula(constant_id)

        parameter = kinetic_law.createParameter()
        parameter.setId(constant_id)
        parameter.setValue(constant_value)
        parameter.setName(constant_id)


        for species in rule.reactants_inside:
            sbml_species_reference = sbml_reaction.createReactant()
            try:
                sbml_species_reference.setSpecies(compartment.species_ids[species])
            except KeyError:
                sbml_species = model.createSpecies()
                sbml_species.setName(species)
                species_id = species_id_generator.next()
                compartment.species_ids[species] = species_id
                sbml_species.setId(species_id)
                sbml_species.setCompartment(compartment.id)
                sbml_species.setInitialAmount(0)
                sbml_species_reference.setSpecies(compartment.species_ids[species])
                sbml_species_reference.initDefaults() # sets stoichiometry to 1

#        for species in rule.reactants_outside:

        for species in rule.products_inside:
            sbml_species_reference = sbml_reaction.createProduct()
            try:
                sbml_species_reference.setSpecies(compartment.species_ids[species])
            except KeyError:
                sbml_species = model.createSpecies()
                sbml_species.setName(species)
                species_id = species_id_generator.next()
                compartment.species_ids[species] = species_id
                sbml_species.setId(species_id)
                sbml_species.setCompartment(compartment.id)
                sbml_species.setInitialAmount(0)
                sbml_species_reference.setSpecies(compartment.species_ids[species])
                sbml_species_reference.initDefaults() # sets stoichiometry to 1

#        for species in rule.products_outside:

    for compartment in compartment.compartments:
        recursively_create_reactions(compartment)



if __name__ == '__main__':

    import libsbml
    # see http://sbml.org/Software/libSBML/docs/python-api/

    document = libsbml.SBMLDocument()

    model = document.createModel()
    document.setLevelAndVersion(2, 4)

    default_compartment = model.createCompartment()
    default_compartment.setId('default')
    default_compartment.setSpatialDimensions(2)

    for unit_definition in (
        ('substance', libsbml.UNIT_KIND_ITEM, 1),
        ('volume', libsbml.UNIT_KIND_LITRE, 1),
        ('area', libsbml.UNIT_KIND_METRE, 2),
        ('length', libsbml.UNIT_KIND_METRE, 1),
        ('time', libsbml.UNIT_KIND_SECOND, 1),
    ):
        sbml_unit_defintion = model.createUnitDefinition()
        sbml_unit_defintion.setId(unit_definition[0])
        sbml_unit_defintion.setName(unit_definition[0])
        sbml_unit = model.createUnit()
        sbml_unit.setKind(unit_definition[1])
        sbml_unit.initDefaults() # sets exponent to 1, scale to 0 and multiplier to 1.0
        if len(unit_definition) > 2:
            sbml_unit.setExponent(unit_definition[2])

    for p in flatten(m.SPsystems):
        recursively_create_compartments(p, default_compartment)
        recursively_create_species(p)
        recursively_create_reactions(p)

    document.checkL2v4Compatibility()
    document.printErrors()
    print libsbml.writeSBMLToString(document)
