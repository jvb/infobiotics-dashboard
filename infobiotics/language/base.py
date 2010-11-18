from types import GeneratorType
import re

class base(object):
    ''' Base class for species, reaction and compartment that implements common functionality. 
    
    id should be automatically generated using self._id_generator.next(), too conform with SBML specification. 
    
    name should be a valid Python identifier that matches r"[_A-Za-z][_A-Za-z1-9]*" see http://homepage.mac.com/s_lott/books/python/html/p04/p04c04_re.html 
    
    '''

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith(('_', 'name'))) #TODO add to reserved prefixes?
    
    def __init__(self, **kwargs):
        if self.__class__.__name__ != 'base' and (not hasattr(self, '_id_generator') or not isinstance(self._id_generator, GeneratorType)):
            raise NotImplementedError("Subclasses of base must have a class attribute '_id_generator' that is a generator")

        # set id automatically
        self._id = self._id_generator.next() #FIXME use name_generator, abandon ids and make name readonly - use ids only for SBML, and name as id for IML. remove compartment base (add __getitem__ and reinstate properties in metacompartment and compartment that do different things)

        # set name if given and valid, falling back to id if not given and raising error if invalid
        name = kwargs.pop('name', None)
        if name is None:
            name = self.id
            self._named = False # used to distinguish model objects that are named explicitly as opposed to mirroring their generated id
        else:
            if not re.match('[_A-Za-z][_A-Za-z1-9]*', name):
                raise ValueError("name should be a valid Python identifier, i.e. a string that starts with a letter or _, and containing any number of letters, digits or _'s. Got '%s' " % name)
            self._named = True
        self.name = name
        
        # try and set all kwargs on instance
        for k, v in kwargs.items():
            setattr(self, k, v)
#            try:
#                setattr(self, k, v)
#            except AttributeError, e:
#                sys.stderr.write('base.__init__(%s=%s)\n' % (k, v if not isinstance(v, str) else "'%s'" % v))
#                raise e

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()
    
    def repr(self, indent=''):
        ''' Return indented string representation of object construction. '''
        raise NotImplementedError 

    def str(self, indent=''):
        ''' Return string representation of object. '''
        raise NotImplementedError
