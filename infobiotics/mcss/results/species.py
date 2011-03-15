class Species(object):
    """An mcss species dataset as a Python object."""

    def __init__(self, index, name, simulation):
        self.index = index
        self.name = name
        self._simulation = simulation
