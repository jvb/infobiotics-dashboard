from enthought.traits.api import BaseLong 

# used by McssParams.runs
class LongGreaterThanZero(BaseLong):
    info_text = 'a Long greater than zero'

    default_value = 1

    def validate(self, object, name, value):
        value = super(LongGreaterThanZero, self).validate(object, name, value)
        if value > 0:
            return value
        self.error(object, name, value)
