from enthought.traits.api import BaseFloat 

# used by McssParams.max_time and McssParams.log_interval
class FloatGreaterThanZero(BaseFloat):
    info_text = 'a float greater than zero'

    default_value = 1.0

    def validate(self, object, name, value):
        value = super(FloatGreaterThanZero, self).validate(object, name, value)
        if value > 0:
            return value
        self.error(object, name, value)
