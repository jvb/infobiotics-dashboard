from enthought.traits.api import HasTraits, Code

class Test(HasTraits): 
    code = Code

Test().configure_traits()

