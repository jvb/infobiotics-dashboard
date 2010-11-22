from types import GeneratorType
import re


class base(object):
    ''' Base class for species, reaction and compartment that implements common functionality. 
    
    id should be a valid Python identifier that matches r"[_A-Za-z][_A-Za-z1-9]*" see http://homepage.mac.com/s_lott/books/python/html/p04/p04c04_re.html 
    
    '''

#    @property
#    def id(self): # change to identifier
#        return self._id

    def __init__(self, **kwargs):
        if self.__class__.__name__ != 'base' and (not hasattr(self, '_id_generator') or not isinstance(self._id_generator, GeneratorType)):
            raise NotImplementedError("Subclasses of base must have a class attribute '_id_generator' that is a generator")

#        # set id automatically
#        self._id = self._id_generator.next() #FIXME use name_generator  
#
#        # set name if given and valid, falling back to id if not given and raising error if invalid
#        name = kwargs.pop('name', None)
#        if name is None:
#            name = self.id
#            self._named = False # used to distinguish model objects that are named explicitly as opposed to mirroring their generated id
#        else:
#            if not re.match('[_A-Za-z][_A-Za-z1-9]*', name):
#                raise ValueError("name should be a valid Python identifier, i.e. a string that starts with a letter or _, and containing any number of letters, digits or _'s. Got '%s' " % name)
#            self._named = True
#        self.name = name

        # try and set all remaining kwargs on instance
        for k, v in kwargs.items():
            setattr(self, k, v)

#    def __repr__(self):
#        return self.repr()
#
#    def __str__(self):
#        return self.str()
    
    def repr(self, indent=''):
        ''' Return indented string representation of object construction. '''
        raise NotImplementedError 

    def str(self, indent=''):
        ''' Return string representation of object. '''
        raise NotImplementedError
