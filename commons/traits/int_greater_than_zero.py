from enthought.traits.api import BaseInt

class IntGreaterThanZero(BaseInt):
    
    info_text = 'an integer greater than zero'

    default_value = 1

    def validate(self, object, name, value):
        value = super(IntGreaterThanZero, self).validate(object, name, value)
        if value > 0:
            return value
        self.error(object, name, value)        
