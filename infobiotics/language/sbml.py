from libsbml import *
reader = SBMLReader()
    
class SBMLModelReader(object):
    
    def __init__(self, file_name):
        document = reader.readSBMLFromFile(file_name)
        document.printErrors()
        model = document.getModel()
        #print model.getListOfSpecies().getElementName()
        for i in range(model.getNumSpecies()):
            species = model.getSpecies(i)
            print species.getInitialAmount(), species.getName(), 'in', model.getCompartment(species.getCompartment()).getName()

    
if __name__ == '__main__':
    SBMLModelReader('/home/jvb/Dropbox/Public/hg/bioluminescence/example.sbml')
    
