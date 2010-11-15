from enthought.traits.api import HasTraits, Str, Property
from infobiotics.commons.counter import Counter as multiset
from quantities.quantity import Quantity

class idd(HasTraits):
    id = Str

class named(idd):

    name = Property(Str)

    def _get_name(self):
        return self._name if self._name != '' else self.id

    def _set_name(self, name):
        self._name = name

    _name = Str
