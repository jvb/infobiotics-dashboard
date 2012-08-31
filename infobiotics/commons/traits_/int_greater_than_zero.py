from traits.api import BaseInt
from numpy import uint, uint0, uint8, uint16, uint32, uint64, uintc, uintp

class IntGreaterThanZero(BaseInt):
    
    info_text = 'an integer greater than zero'

    default_value = 1

    def validate(self, object, name, value):
        if type(value) in (uint, uint0, uint8, uint16, uint32, uint64, uintc, uintp):
            value = int(value)
        value = super(IntGreaterThanZero, self).validate(object, name, value)
        if value > 0:
            return value
        self.error(object, name, value)        
