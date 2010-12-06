'''Work in progress method for converting infobiotics.language models into
mcss-compatible sbml.

TODO differentiate between mcss-compatible sbml and real sbml.

TODO degraded species in reactions with no products

TODO transport rules need products as well as reactants
TODO transport rules from inside compartments to outside ones use 'r1:c1' rather than 'r1:0,1'
TODO inside compartments (templates) have names like c2:::c1

'''

{
    'a -> b': '', # transformation reaction

    'a -> [a]_name': ':name', # send 'a' into compartment named 'name'

    '[a] -> a': ':*', # sends 'a' to any neighbour if outmost compartment or enclosing compartment if not
    'a -> a (0,1)': ':0,1', # send along vector (0,1) (if outmost compartment?)

    'a -> a (name)': ':name', # send 'a' (out?) to neighbouring compartment named 'name'

    # same
    'a -> a [ ]_vesicle': 'name:*', # send 'a' out of vesicle
    '[a]_vesicle -> a [ ]_vesicle': 'name:*' # send 'a' out of vesicle
}





#from infobiotics.language import *
#
#cell = compartment(
##    'a -> b 1',
##    'a -> [a]_vesicle 1',
##    '[a] -> a 1',
##    'a -> a (0,1) 1',
#    label='cytoplasm',
#    nucleus=compartment('[a]_nucleus -> a []_nucleus 1'),
#    vesicle=compartment(),
#)
#print cell.str()
##print cell.nucleus.repr()
#
#class cytoplasm(compartment):
#    nucleus = compartment('[a] -> a []_nucleus 1')
#    vesicle = compartment()
#print cytoplasm.nucleus.str()
#
#
#class nucleus(compartment):
##    label = 'nucleus' # if not set glean from class name 
#    r = '[a] -> a []_nucleus 1'
#
#nucleus = compartment(label='nucleus')
#nucleus = compartment() # not possible to know label without introspection module stack    
#
#print nucleus.str()
#
#exit()


from infobiotics.language import *

# Don't import ID generators ! Use different IDs for SBML, and simplified names for IML IDs.
def id_generator(prefix=''):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1
species_id_generator = id_generator('s')
constant_id_generator = id_generator('c')#k')
reaction_id_generator = id_generator('re')
compartment_id_generator = id_generator('c')
template_id_generator = id_generator()#'t')
z_position_generator = id_generator()

def recursively_create_compartments(compartment, outside_sbml_compartment, x, y):
    compartment._id = compartment_id_generator.next()
    template_id = template_id_generator.next()

    # templates
    sbml_compartment = model.createCompartment()
    sbml_compartment.setId(compartment._id)
    sbml_compartment.setName('%s:%s::' % (compartment.label, template_id))
    sbml_compartment.setSize(float(compartment.volume))
    sbml_compartment.setUnits('volume')
    sbml_compartment.setSpatialDimensions(3) # required for setOutside below
    sbml_compartment.setOutside(outside_sbml_compartment.getId())

    # users of templates
    sbml_compartment = model.createCompartment()
    sbml_compartment.setId(compartment._id)
#    sbml_compartment.setName(compartment.label)#name)
    if outside_sbml_compartment.getId() == 'default':
        sbml_compartment.setName('%s::%s:%s,%s' % (compartment.label, template_id, x, y))
    else:
        sbml_compartment.setName('%s::%s:%s,%s,%s' % (compartment.label, template_id, x, y, z_position_generator.next()))
#        sbml_compartment.setName('%s:%s:%s:' % (compartment.label, template_id, template_id))
    sbml_compartment.setSize(float(compartment.volume))
    sbml_compartment.setUnits('volume')
    sbml_compartment.setSpatialDimensions(3) # required for setOutside below
    sbml_compartment.setOutside(outside_sbml_compartment.getId())

    # recursion
    for compartment in compartment.compartments:
        recursively_create_compartments(compartment, sbml_compartment, x, y) #TODO 'outside' attribute not required?


def create_species(compartment, name, amount):
    sbml_species = model.createSpecies()
    sbml_species.setName(name)
    species_id = species_id_generator.next()
    compartment._species_ids[name] = species_id # set the id on the compartment #TODO how will this work for classes?
    sbml_species.setId(species_id)
    sbml_species.setCompartment(compartment._id)
    sbml_species.setInitialAmount(float(amount)) #TODO setInitialConcentration? mcss probably doesn't use this.
    sbml_species.setHasOnlySubstanceUnits(True) # we are dealing only in molecules
    return sbml_species

def recursively_create_species(compartment):
    compartment._species_ids = {} # create a dict on the compartment - used in recursively_create_reactions? #TODO
    for name, amount in compartment.amounts().items(): #TODO might need to 
#        sbml_species = model.createSpecies()
#        sbml_species.setName(name)
#        species_id = species_id_generator.next()
#        compartment._species_ids[name] = species_id # set the id on the compartment #TODO how will this work for classes?
#        sbml_species.setId(species_id)
#        sbml_species.setCompartment(compartment._id)
#        sbml_species.setInitialAmount(float(amount)) #TODO setInitialConcentration? mcss probably doesn't use this.
#        sbml_species.setHasOnlySubstanceUnits(True) # we are dealing only in molecules
        create_species(compartment, name, amount)
    for compartment in compartment.compartments:
        recursively_create_species(compartment)


def recursively_create_reactions(compartment):
    for reaction in compartment.reactions:

        sbml_reaction = model.createReaction()
        sbml_reaction.setId(reaction_id_generator.next())

#        sbml_reaction.setName(sbml_reaction.getId()) #TODO '%s:%s,%s' for transport reactions
        if reaction.is_transport_rule:
            # 'a -> a (0,1)': ':0,1', # send along vector (0,1) (if outmost compartment?)
            # 'a -> a (*)'
            # 'a -> a (nucleus)'
            name = ':' + reaction.vector
        elif reaction.products_label is not None:
            if reaction.products_label != compartment.label:
                # 'a -> [a]_name': ':name', # send 'a' into compartment named 'name'
                name = ':' + reaction.products_label
            elif len(reaction.products_outside) > 0:
                # 'a -> a []_self'
                name = ':*'
        else:
            # transformation rule
            name = ''
        sbml_reaction.setName(name)

        sbml_reaction.setReversible(False)
        sbml_reaction.setFast(False)

#        if isinstance(reaction.constant, Constant):
#            constant_value = reaction.constant.value
#        else:
#            constant_value = reaction.constant
#        if isinstance(reaction.constant, Constant) and reaction.constant.id != '':
#            constant_id = reaction.constant.id
#        else:
#            constant_id = constant_id_generator.next()
        constant_value = reaction.rate
        constant_id = constant_id_generator.next()

        kinetic_law = sbml_reaction.createKineticLaw()
        kinetic_law.setFormula(constant_id)

        parameter = kinetic_law.createParameter()
        parameter.setId(constant_id)
        parameter.setValue(constant_value)
        parameter.setName(constant_id)

        def initialise_sbml_species_reference(sbml_species_reference):
            try:
                sbml_species_reference.setSpecies(compartment._species_ids[name]) #TODO here is where we need the alphabet from the reactions
            except KeyError:
                create_species(compartment, name, 0)
#                sbml_species = model.createSpecies() #TODO or maybe not
#                sbml_species.setName(name)
#                species_id = species_id_generator.next()
#                compartment._species_ids[name] = species_id
#                sbml_species.setId(species_id)
#                sbml_species.setCompartment(compartment._id)
#                sbml_species.setInitialAmount(0)
#                sbml_species.setHasOnlySubstanceUnits(True)
                sbml_species_reference.setSpecies(compartment._species_ids[name])
            sbml_species_reference.initDefaults() # sets stoichiometry to 1

        for name in reaction.reactants_inside:
            initialise_sbml_species_reference(sbml_reaction.createReactant())

#        for species in reaction.reactants_outside: #TODO

        for name in reaction.products_inside:
            initialise_sbml_species_reference(sbml_reaction.createProduct())

#        for species in reaction.products_outside: #TODO

    for compartment in compartment.compartments:
        recursively_create_reactions(compartment)


#TODO _degraded for each reactant in reactions with no products
#TODO transport rules

if __name__ == '__main__':

    class C(compartment):
        volume = 2
        inner = compartment(volume=3)
        r1 = 'a -> b 0.1'
    #    r2 = 'b -> [ b ] 0.5'
        a = 10

    c = C()
#    print c.repr()
#    exit()

    system = model(c)

    import libsbml
    # see http://sbml.org/Software/libSBML/docs/python-api/

    document = libsbml.SBMLDocument()
#    document.setLevelAndVersion(2, 4)
    model = document.createModel()
    model.setId('test') # needed by mcss
    document.setLevelAndVersion(2, 4)

    default_compartment = model.createCompartment()
    default_compartment.setId('default')
    default_compartment.setSpatialDimensions(2) #TODO really?

    for unit_definition in (
        ('substance', libsbml.UNIT_KIND_ITEM, 1), # molecules
#        ('volume', libsbml.UNIT_KIND_LITRE, 1),
        ('volume', libsbml.UNIT_KIND_METRE, 3), #TODO get from model
        ('area', libsbml.UNIT_KIND_METRE, 2),
        ('length', libsbml.UNIT_KIND_METRE, 1),
        ('time', libsbml.UNIT_KIND_SECOND, 1), #TODO get from model
    ):
        sbml_unit_defintion = model.createUnitDefinition()
        sbml_unit_defintion.setId(unit_definition[0])
        sbml_unit_defintion.setName(unit_definition[0])
        sbml_unit = model.createUnit()
        sbml_unit.setKind(unit_definition[1])
        sbml_unit.initDefaults() # sets exponent to 1, scale to 0 and multiplier to 1.0
        if len(unit_definition) > 2:
            sbml_unit.setExponent(unit_definition[2])

    for c, x, y in system.compartments:
        recursively_create_compartments(c, default_compartment, x, y)
        recursively_create_species(c)
        recursively_create_reactions(c)

    document.checkL2v4Compatibility()
    document.printErrors()

    print libsbml.writeSBMLToString(document)
#    libsbml.writeSBMLToFile(document, 'test.sbml')
