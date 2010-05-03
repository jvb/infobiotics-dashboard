from enthought.traits.api import BaseFloat 

class FloatWithMinimum(BaseFloat):
    ''' usage: trait = FloatWithMinimum(minimum_value=0) '''
    
    info_text = 'a float with a minimum value'

    def init(self, minimum_value=None): #TODO want to be able to set minimum_value from with out keyword arg
        if minimum_value is None:
            minimum_value = 0
        self.minimum_value = minimum_value

    def get_default_value(self):
        # to explain the tuple with a 0 see http://code.enthought.com/projects/files/ETS31_API/enthought.traits.trait_handlers.TraitType.html#get_default_value
        return (0, self.minimum_value)

    def validate(self, object, name, value):
        value = super(FloatWithMinimum, self).validate(object, name, value)
        if value >= self.minimum_value:
            return value
        self.error(object, name, value)
