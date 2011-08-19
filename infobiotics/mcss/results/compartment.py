class Compartment(object): # TODO rename McssCompartment

#    def __init__(self, index, id, name, x_position, y_position, template_index, creation_time, destruction_time, run, simulation):
    def __init__(self, index, id, name, x_position, y_position, template_index, run, simulation):
#        z_position, 
        self.run = run
        self._simulation = simulation
        self.index = index
        self.id = id
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
#        self.z_position = z_position
        self.template_index = template_index
#        self.creation_time = creation_time
#        self.destruction = destruction_time        

    def coordinates(self):
        return (self.x_position, self.y_position)

    def compartment_name_and_xy_coords(self):
        return "%s (%s,%s)" % (self.name, self.x_position, self.y_position)

    def __str__(self): # used by McssResults.export_timeseries
        xy_position = '{x_position},{y_position}'.format(**self.__dict__)
        if xy_position in self.name:
            return self.name
        else:
            return '{name} at ({x_position},{y_position})'.format(**self.__dict__)
    