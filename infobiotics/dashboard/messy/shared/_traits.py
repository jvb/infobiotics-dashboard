def trait_type_class_name(self, trait_name): #TODO use in ParamsExperiment and ParamsFileXMLReader
    return eval('self.trait("%s").trait_type.__class__.__name__' % trait_name)
