class Species(object): #TODO rename mcss_species

    def __init__(self, index, name, simulation):
        self.index = index
        self.name = name
        self._simulation = simulation

    def __str__(self): # used by McssResults.export_timeseries
        return '{name}'.format(**self.__dict__)