from enthought.traits.api import BaseLong

class LongGreaterThanZero(BaseLong):
    ''' Used by McssParams.runs and MC2Params.number_samples (which are 
    effectively the same thing). '''
    
    info_text = 'a Long greater than zero'

    default_value = 1L
    
    def validate(self, object, name, value):
        value = super(LongGreaterThanZero, self).validate(object, name, value)
        if value > 0:
            return value
        self.error(object, name, value)
