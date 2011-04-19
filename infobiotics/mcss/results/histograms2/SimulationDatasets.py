#TODO see SurfaceHistories

# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


import tables
from md5sum import md5sum
from numpy import zeros, arange, array, float64, uint64, string_ 
#from decimal import Decimal
from bisect import bisect, bisect_right, bisect_left 
from math import floor, ceil
from infobiotics.commons.sequences import unique, copy


from numpy import arange, empty
import tables

def attributesOfRange(rangeSequence):
    start = rangeSequence[0]
    stop = rangeSequence[-1]
    if len(rangeSequence) == 1:
        step = 1
    else:
        step = rangeSequence[1] - rangeSequence[0]
    return (int(start), int(stop), int(step))

def amountsFromIndices(fileName,
                       listOfSpeciesIndices,
                       listOfCompartmentIndices,
                       listOfTimepointIndices,
                       listOfRunIndices):
    ''' Returns a tuple(4D array [species, compartment, timepoint, run],
                        listOfSpeciesIndices,
                        listOfCompartmentIndices,
                        listOfTimepointIndices, # possibly changed
                        listOfRunIndices)
     
    '''
    shape = (len(listOfSpeciesIndices),
             len(listOfCompartmentIndices),
             len(listOfTimepointIndices),
             len(listOfRunIndices))
    
    try:
        amountsFromIndices = empty(shape, int)
        
    except MemoryError:
        # try again with half the number of timepoints, recursively
        listOfTimepointIndices = listOfTimepointIndices[::2]
        return amountsFromIndices(fileName,
                                  listOfSpeciesIndices,
                                  listOfCompartmentIndices,
                                  listOfTimepointIndices,
                                  listOfRunIndices)
    
    with tables.openFile(fileName) as file:
        simulationNode = file.root

        start, stop, step = attributesOfRange(listOfTimepointIndices)
        timepointIndicesSlice = slice(start, stop + 1, step)
        
        for runIndex in listOfRunIndices:
            runNumber = runIndex + 1
            runNode = simulationNode._f_getChild("run%s" % runNumber)
            
            numberOfSpecies, numberOfCompartments, numberOfTimepoints = runNode.amounts.shape
            if len(listOfSpeciesIndices) < numberOfSpecies / 25:
                # rate-limiting step O(N * N)?
                for si, s in enumerate(listOfSpeciesIndices):
                    for ci, c in enumerate(listOfCompartmentIndices):
                        amountsFromIndices[si, ci, :, runIndex] = runNode.amounts[s, c, timepointIndicesSlice]

            else:
                # rate-limiting step ~ O(N * logN)
                amounts = runNode.amounts[..., timepointIndicesSlice]
                # can't use listOfTimepointIndices index-array on runNode.amounts 
                # because is currently PyTables array 
            
                # now it is amountsFromIndices NumPy array so we can use listOfCompartmentIndices as
                # an index-array to reduce amounts
                amounts = amounts[:, listOfCompartmentIndices]
    
                # use listOfSpeciesIndices as an index-array to reduce amounts
                amounts = amounts[listOfSpeciesIndices]
                        
                # copy amounts into amountsFromIndices[:,:,:,runIndex]
                amountsFromIndices[..., runIndex] = amounts
            
    return (amountsFromIndices,
            listOfSpeciesIndices,
            listOfCompartmentIndices,
            listOfTimepointIndices,
            listOfRunIndices)
    
    
    
    
    
    


def nearestTimepointIndex(listOfTimepoints, time):
    next = bisect(listOfTimepoints, time)
    previous = next - 1
    if next == len(listOfTimepoints):
        # time is after last timepoint
        return previous
    b = listOfTimepoints[next]
    a = listOfTimepoints[previous]
    if abs(time - a) < abs(time - b):
        # time is nearer to previous
        return previous
    else:
        # time is nearer to next
        return next


def nearestTimepoint(listOfTimepoints, time):
    return listOfTimepoints[nearestTimepointIndex(listOfTimepoints, time)]


def listOfTimepoints(startTime, stopTime, stepTime=1):
#    ''' stopTimeInclusive '''
#    listOfTimepoints = arange(startTime, stopTime+stepTime, stepTime, float64)
    listOfTimepoints = arange(startTime, stopTime, stepTime, float64)
    return listOfTimepoints


def listOfTimepointIndices(startTime, stopTime, stepTime):
#    startIndex = 0
#    stopIndex = (stopTime / stepTime) - (startTime / stepTime)
##    numberOfTimepoints = (stopTime - startTime) / stepTime
##    return linspace(startIndex, stopIndex, numberOfTimepoints)
#    return arange(startIndex, stopIndex, 1)
#    return [index for index, timepoint in enumerate(listOfTimepoints(startTime, stopTime, stepTime))]
    return [index for index in range(len(listOfTimepoints(startTime, stopTime, stepTime)))]


def attributesOfListOfTimepoints(listOfTimepoints):
    startTime = listOfTimepoints[0]
    stopTime = listOfTimepoints[-1]
    try:
        stepTime = listOfTimepoints[1] - listOfTimepoints[0]
    except IndexError:
        # only one timepoint
        stepTime = 1
    return (startTime, stopTime, stepTime) 


def attributesOfListOfTimepointsIndices(listOfTimepointIndices):
    return attributesOfListOfTimepoints(listOfTimepointIndices)


def listOfTimepointIndicesFromAnotherListOfTimepoints(listOfTimepoints, otherListOfTimepoints):
    '''
    Returns the list of timepoint indices for one list of timepoints in another.
    '''
    listOfTimepointIndicesInOtherListOfTimepoints = []
    for timepoint in listOfTimepoints:
        listOfTimepointIndicesInOtherListOfTimepoints.append(nearestTimepointIndex(otherListOfTimepoints, timepoint))
    return unique(listOfTimepointIndicesInOtherListOfTimepoints)


def listOfTimepointIndicesFromListOfTimepoints(listOfTimepoints, startTime=None, stopTime=None, stepTime=None):
    ''' 
    Returns the list of timepoint indices, in a listOfTimepoints, 
    from startTime to stopTime inclusive for every stepSize timepoint.
    The timepoints in listOfTimepoints must be evenly spaced. 
    Warning: the indices will be meaningless if you pass this method an  
    incomplete listOfTimepoints, i.e. a subset, with a corresponding array
    of values at those timepoints.
    '''

    originalStartTime, originalStopTime, originalStepTime = attributesOfListOfTimepoints(listOfTimepoints)

    # validate input parameters
    if startTime is None:
        startTime = originalStartTime
    
    if 0 < stopTime < startTime:
        stopTime = None
        
    if stopTime is None:
        stopTime = originalStopTime
        
    if stepTime is None:
        stepTime = originalStepTime
    
    # get startTimeIndex from run._listOfTimepoints
    if originalStartTime < startTime < originalStopTime:
        # make startTimeIndex the index of the timepoint closest to, and including, startTime
#        startTimeIndex = bisect.bisect_left(listOfTimepoints, floor(startTime))
        startTimeIndex = floor(bisect_left(listOfTimepoints, startTime))
    else:
        # make start the index of the first timepoint
        startTimeIndex = 0

    # get stopTimeIndex from listOfTimepoints
    if originalStartTime < stopTime < originalStopTime:
        # make stopTimeIndex the index of the timepoint closest to, and including, stopTime
#        stopTimeIndex = bisect_right(listOfTimepoints, ceil(stopTime))
        stopTimeIndex = ceil(bisect_right(listOfTimepoints, stopTime))
    else:
        # make stopTimeIndex the index of the final timepoint and add 1 since range stop indexes are exclusive
        stopTimeIndex = len(listOfTimepoints) + 1

    # determine stepSize from run.stepTime (actually run.simulation.log_interval)
    stepSize = stepTime / originalStepTime
#    print stepSize, stepTime, originalStepTime
    if stepSize is not int:
        # correct stepSize if not a whole number
        stepSize = int(stepSize)
    if stepSize < 1:
        # correct stepSize to 1 if less than 1
        stepSize = 1
    if stepTime > stopTimeIndex:
        # correct stepSize to distance between start and stop if greater than stopTimeIndex
        stepSize = stopTimeIndex - startTimeIndex
    return arange(startTimeIndex, stopTimeIndex, stepSize, int)


def listOfTimepointsFromListOfTimepoints(listOfTimepoints, startTime=None, stopTime=None, stepTime=None):
    ''' Returns the list of timepoints in run (from startTime to stopTime inclusive, every stepSize timepoint). '''
    # slice numpy array run.listTimepoints_ with an index array (see http://docs.scipy.org/doc/numpy/user/basics.indexing.html)
    return listOfTimepoints[listOfTimepointIndicesFromListOfTimepoints(listOfTimepoints, startTime, stopTime, stepTime)]


def listOfAttributeOfObjectFromListOfOtherAttributeOfObject(listOfObjects, attributeName, listOfOtherAttributeOfObjects=None, otherAttributeName=None):
    '''
    Factored out from listOfSpeciesNames, listOfSpeciesIndices, listOfRunIndices, listOfCompartmentNames, listOfCompartmentIndices
    '''
    if listOfOtherAttributeOfObjects is None:
        return [getattr(object, attributeName) for object in listOfObjects]
    else:
        listOfOtherAttributeOfObjects = copy(listOfOtherAttributeOfObjects)
        if len(listOfOtherAttributeOfObjects) > len(unique(copy(listOfOtherAttributeOfObjects))):
            raise ValueError('Input list contains duplicates: %s, therefore output list would contain duplicates making it unreliable.' % listOfOtherAttributeOfObjects)
        listOfAttributeOfObjects = []
        # check each object against listOfOtherAttributeOfObjects
        for object in listOfObjects:
            otherAttributeOfObject = getattr(object, otherAttributeName)
            if otherAttributeOfObject in listOfOtherAttributeOfObjects:
                # add attributeOfObject to list
                listOfAttributeOfObjects.append(getattr(object, attributeName))
                # now remove otherAttributeOfObject from listOfOtherAttributeOfObjects (we know it is the only instance because we would have raised an error above otherwise).
                listOfOtherAttributeOfObjects.remove(otherAttributeOfObject)
                # and go to next object
                continue
        return listOfAttributeOfObjects

        
class Simulation(object):
    '''
    Contains attributes of an mcss simulation's root node.
    '''

    @classmethod
#    @profile
    def fromH5File(cls, fileName):
        '''
        Create sets of linked objects for all data/metadata in simulation file.
        '''
        try:
            file = tables.openFile(fileName, 'r')
        except IOError, e:
            print e
            return
        if not file.root._v_attrs.__contains__('mcss_version'):
            raise Exception('%s is not an mcss simulation file' % fileName)
        
        simulationNode = file.root

        # simulation
        simulation = Simulation(
                         simulationNode._v_attrs,
#                         file.root._v_attrs.startTime,
                         fileName)
        
        # extracting entries from H5 tables:
        #http://www.pytables.org/docs/manual/ch03.html#readingAndSelectingUsage

        # create list of species objects for this simulation
        simulation.listOfSpecies = [
            Species(
#                uint64(row['species_index']), 
                # used uint64 because that was what ViTables said it was saved
                # as in the HDF5, however having uint64's as indices breaks 
                # PyTables in a strange way involving is_idx() which adds 1 
                # to the key of the stop index and it becomes a float and then 
                # returns a TypeError, so I have reverted back int for indices.
                int(row['species_index']),
                str(row['species_name']),
                simulation) 
            for row in simulationNode.species_information]

        # create a dictionary of index -> Species
        simulation.dictionaryOfSpecies = dict([(species.species_index, species) for species in simulation.listOfSpecies])
                    
        # rules
        simulation.listOfRules = [
            Rule(
                uint64(row['rule_template_index']),
                uint64(row['rule_index']),
                str(row['rule_id']),
                str(row['rule_name']),
                uint64(row['rule_x_target']),
                uint64(row['rule_y_target']),
                simulation) 
            for row in simulationNode.rule_information]

        # rulesets
        simulation.listOfRuleSets = [
            RuleSet(
                uint64(row['ruleset_index']),
                str(row['ruleset_name']),
                str(row['ruleset_compartment_id']),
                uint64(row['number_of_rules_in_ruleset']),
                simulation) 
            for row in simulationNode.ruleset_information]
        
        # runs
        runIndex = 0
        numberOfRuns = simulation.number_of_runs
        for runNumber in range(1, int(numberOfRuns) + 1):
            try:
                runNode = simulationNode._f_getChild("run%s" % runNumber)                
                # expect exceptions here
                run = Run(runNode._v_attrs, runNumber, runIndex, simulation)
                simulation.listOfRuns.append(run)
                runIndex += 1
                
                # compartments
                run.listOfCompartments = [
                    Compartment(
#                        uint64(row['compartment_index']), # see note for species_index 
                        int(row['compartment_index']),
                        str(row['compartment_id']),
                        string_(row['compartment_name']),
                        uint64(row['compartment_x_position']),
                        uint64(row['compartment_y_position']),
#                        uint64(row['compartment_z_position']), 
                        uint64(row['compartment_template_index']),
                        float64(row['compartment_creation_time']),
                        float64(row['compartment_destruction_time']),
                        run,
                        simulation) 
                    for row in runNode.compartment_information]
                simulation.listOfListOfCompartmentsInAllRuns.append(run.listOfCompartments)
                simulation.listOfNumberOfCompartmentsInAllRuns.append(len(run.listOfCompartments))
                
                # levels/amounts
                if simulation.log_type == 'levels':
                    run.hasAmounts = True
            
                # reactions
                if simulation.log_type == 'reactions':
                    run.hasReactions = True
                    run.run.listOfReactions = [
                        Reaction(
                            float64(row['time']),
                            uint64(row['species_index']),
                            uint64(row['species_amount']),
                            uint64(row['compartment_index']),
                            uint64(row['rule_index']),
                            run,
                            simulation) 
                        for row in runNode.reactions]
                    simulation.listOfListOfReactionsInAllRuns.append(run.listOfReactions)
                    simulation.listOfNumberOfReactionsInAllRuns.append(len(run.listOfReactions))
    
#                # propensities
#                if simulation.log_propensities == 1:
#                    run.hasPropensities = True
#                    raise NotImplementedError
                    
                # volumes/positions
                if simulation.log_volumes == 1:
                    run.hasVolumes = True
                    run.listOfPositions = [
                        Position(
                            float64(row['compartment_creation_time']),
                            uint64(row['compartment_index']),
                            uint64(row['compartment_x_position']),
                            uint64(row['compartment_y_position']),
                            run,
                            simulation)
                        for row in runNode.positions]
                    simulation.listOfListOfPositionsInAllRuns.append(run.listOfPositions)
                    
            except tables.exceptions.NoSuchNodeError, e:
#                print e
                # could not find node run%s % runNumber
                # so reopen file in r+ mode 
                file.close()
                file = tables.openFile(simulation.fileName, 'r+')
                # decrement number_of_runs
                file.root._v_attrs.number_of_runs = simulation.number_of_runs - 1
                # update simulation's attributes
                simulation.numberOfRuns = simulation.number_of_runs = file.root._v_attrs.number_of_runs
                # and try again
                continue
    
        simulation.postInitialisation()
    
        file.close()

        return simulation

    
    def __init__(self, attributes, fileName, startTime=0):
        # expose attributes as fields 
        self.data_file = attributes.data_file
        self.duplicate_initial_amounts = attributes.duplicate_initial_amounts
        self.lattice_x_dimension = attributes.lattice_x_dimension
        self.lattice_y_dimension = attributes.lattice_y_dimension
        self.lattice_z_dimension = attributes.lattice_z_dimension
        self.log_degraded = attributes.log_degraded
        self.log_interval = attributes.log_interval
        self.log_propensities = attributes.log_propensities
        self.log_type = attributes.log_type
        self.log_volumes = attributes.log_volumes
        self.max_time = attributes.max_time
        self.mcss_version = attributes.mcss_version
        self.model_format = attributes.model_format
        self.model_input_file = attributes.model_input_file
        self.number_of_rule_templates = attributes.number_of_rule_templates
        self.number_of_rules_in_templates = attributes.number_of_rules_in_templates
        self.number_of_runs = attributes.number_of_runs
        self.number_of_species = attributes.number_of_species
        self.periodic_x = attributes.periodic_x
        self.periodic_y = attributes.periodic_y
        self.periodic_z = attributes.periodic_z
        self.seed = attributes.seed
        self.simulation_algorithm = attributes.simulation_algorithm
        self.simulation_algorithm_name = attributes.simulation_algorithm_name
        self.simulation_end_time = attributes.simulation_end_time
        self.simulation_start_time = attributes.simulation_start_time
        self.total_number_of_rules = attributes.total_number_of_rules
     
        # attribute derived fields
        self.maxTime = self.max_time
        self.numberOfRuns = self.number_of_runs
        self.numberOfSpecies = self.number_of_species
        self.originalFileName = self.data_file
        self.originalModelFileName = self.model_input_file
        self.stepTime = self.log_interval
        
        # parameter derived fields
        self.fileName = fileName
        self.md5sum = md5sum(fileName)
        self.startTime = startTime

        # externally appended
        self.listOfSpecies = []
        self.dictionaryOfSpecies = {}
        self.listOfRules = []
        self.listOfRuleSets = []
        self.listOfRuns = []
        self.listOfListOfCompartmentsInAllRuns = []
        self.listOfNumberOfCompartmentsInAllRuns = []
        self.listOfListOfReactionsInAllRuns = []
        self.listOfNumberOfReactionsInAllRuns = []
        self.listOfListOfPositionsInAllRuns = []

        self.hasSingleRun = False#True if self.numberOfRuns == 1 else False # only knowable after all runs are added
        self.hasTruncatedRun = False
        self.truncatedRun = None
        
        
    def postInitialisation(self):
        firstRun = self.firstRun()
        lastRun = self.lastRun()
        if firstRun == lastRun:
            self.hasSingleRun = True
        if firstRun.lastTimepoint() != lastRun.lastTimepoint():
            self.hasTruncatedRun = True
            self.truncatedRun = lastRun

        
    def changeFileName(self, fileName):
        '''
        Changes self.fileName if the new file pointed to by fileName has the 
        same md5sum as self.fileName.
        '''
        
        if md5sum(fileName) == self.md5sum:
            self.fileName = fileName
        else:
            raise Exception('%s is not the same file as %s (md5sum\'s do not match).' % (fileName, self.fileName))

        
    def firstRun(self):
        return self.listOfRuns[0]


    def lastRun(self):
        return self.listOfRuns[-1]


    def listOfTimepointsOfNonTruncatedRuns(self):
        if self.hasSingleRun:
            return self.lastRun().listOfTimepoints
        elif self.hasTruncatedRun:
            # many runs but last one is truncated
            return self.listOfRuns[-2].listOfTimepoints
        else:
            return self.listOfRuns[0].listOfTimepoints
            
            
    def listOfTimepointIndicesOfNonTruncatedRuns(self):
        if not hasattr(self, '_listOfTimepointIndicesOfNonTruncatedRuns'):
            self._listOfTimepointIndicesOfNonTruncatedRuns = listOfTimepointIndicesFromListOfTimepoints(self.listOfTimepointsOfNonTruncatedRuns())
        return self._listOfTimepointIndicesOfNonTruncatedRuns


    def listOfTimepointsFromListOfTimepointsOfNonTruncatedRuns(self, startTime=None, stopTime=None, stepTime=None):
        if not hasattr(self, 'self._listOfTimepointsFromListOfTimepointsOfNonTruncatedRuns'):
            self._listOfTimepointsFromListOfTimepointsOfNonTruncatedRuns = listOfTimepointsFromListOfTimepoints(self.listOfTimepointsOfNonTruncatedRuns(), startTime, stopTime, stepTime)
        return self._listOfTimepointsFromListOfTimepointsOfNonTruncatedRuns
    

    def listOfTimepointIndicesFromListOfTimepointIndicesOfNonTruncatedRuns(self, startTime=None, stopTime=None, stepTime=None):
        return listOfTimepointIndicesFromListOfTimepoints(self.listOfTimepointsOfNonTruncatedRuns(), startTime, stopTime, stepTime)
                 

    
    def stopTimeCommonToAllRuns(self):
        ''' in case the last run was truncated '''
        if not hasattr(self, '_stopTimeIndexCommonToAllRuns'):
            lastRun = self.listOfRuns[-1]
            self._stopTimeCommonToAllRuns = lastRun.stopTime
        return self._stopTimeCommonToAllRuns


    def stopTimeIndexCommonToAllRuns(self):
        ''' in case the last run was truncated '''
        if not hasattr(self, '_stopTimeIndexCommonToAllRuns'):
            self._stopTimeIndexCommonToAllRuns = self.lastRun().timepointIndex(self.stopTimeCommonToAllRuns())
        return self._stopTimeIndexCommonToAllRuns


    def listOfTimepointsCommonToAllRuns(self):
        ''' Returns the list of timepoints common to all runs, in case the last run was truncated. '''
        if not hasattr(self, '_listOfTimepointsCommonToAllRuns'):
            self._listOfTimepointsCommonToAllRuns = self.lastRun().listOfTimepointsFromListOfTimepoints()#stopTime=self.stopTimeCommonToAllRuns())
        return self._listOfTimepointsCommonToAllRuns
    
        
    def listOfTimepointsIndicesCommonToAllRuns(self):
        ''' Returns the list of timepoint indices common to all runs, in case the last run was truncated. '''
        return listOfTimepointIndicesFromListOfTimepoints(self.listOfTimepointsCommonToAllRuns())
        

    def listOfTimepointsFromListOfTimepointsCommonToAllRuns(self, startTime=None, stopTime=None, stepTime=None):
        return listOfTimepointsFromListOfTimepoints(self.listOfTimepointsCommonToAllRuns(), startTime, stopTime, stepTime)    
    

    def listOfTimepointIndicesFromListOfTimepointsCommonToAllRuns(self, startTime=None, stopTime=None, stepTime=None):
        ''' Returns the list of timepoint indices common to all runs (from startTime to stopTime inclusive, every stepSize timepoint). '''
        return listOfTimepointIndicesFromListOfTimepoints(self.listOfTimepointsCommonToAllRuns(), startTime, stopTime, stepTime)

    
    def speciesIndex(self, speciesName):
        listOfSpeciesIndices = self.listOfSpeciesIndices([speciesName]) 
        if len(listOfSpeciesIndices) != 1:
            raise ValueError('%s not in list of species' % speciesName)
        else:
            return listOfSpeciesIndices[0]


#    def listOfSpeciesIndices(self, listOfSpeciesNames=None):
#        if listOfSpeciesNames is None:
#            return [species.species_index for species in self.listOfSpecies]
#        else:
#            listOfSpeciesNames = copy(listOfSpeciesNames) # since we will modify listOfSpeciesName we take a copy just to be safe.
#            if len(listOfSpeciesNames) > len(unique(copy(listOfSpeciesNames))):
#                raise ValueError('listOfSpeciesNames contains duplicates, therefore returned listOfSpeciesIndices would contain duplicates.')  
#            listOfSpeciesIndices = []
#            # check each species against listOfSpeciesNames
#            for species in self.listOfSpecies:
#                speciesName = species.species_name
#                if speciesName in listOfSpeciesNames:
#                    # add speciesIndex to list
#                    speciesIndex = species.species_index
#                    listOfSpeciesIndices.append(speciesIndex)
#                    # now remove speciesName from listOfSpeciesNames (we know it is the only instance because we would have raised an error above otherwise).
#                    listOfSpeciesNames.remove(speciesName)
#                    # and go to next species
#                    continue
#            return listOfSpeciesIndices
#        
#                    
#    def listOfSpeciesNames(self, listOfSpeciesIndices=None):
#        if listOfSpeciesIndices is None:
#            return [species.species_name for species in self.listOfSpecies]
#        else:
#            listOfSpeciesIndices = copy(listOfSpeciesIndices) # since we will modify listOfSpeciesIndices we take a copy just to be safe.
#            if len(listOfSpeciesIndices) > len(unique(copy(listOfSpeciesIndices))):
#                raise ValueError('listOfSpeciesIndices contains duplicates, therefore returned listOfSpeciesNames would contain duplicates.')  
#            listOfSpeciesNames = []
#            # check each species against listOfSpeciesIndices
#            for species in self.listOfSpecies:
#                speciesIndex = species.species_index
#                if speciesIndex in listOfSpeciesIndices:
#                    # add speciesName to list
#                    speciesName = species.species_name
#                    listOfSpeciesNames.append(speciesName)
#                    # now remove speciesIndex from listOfSpeciesIndices (we know it is the only instance because we would have raised an error above otherwise).
#                    listOfSpeciesIndices.remove(speciesIndex)
#                    # and go to next species
#                    continue
#            return listOfSpeciesNames
#
#
#    def listOfRunIndices(self, listOfRunNumbers=None):
#        if listOfRunNumbers is None:
#            return [run.runIndex for run in self.listOfRuns]
#        else:
#            listOfRunNumbers = copy(listOfRunNumbers) # since we will modify listOfRunName we take a copy just to be safe.
#            if len(listOfRunNumbers) > len(unique(copy(listOfRunNumbers))):
#                raise ValueError('listOfRunNumbers contains duplicates, therefore returned listOfRunIndices would contain duplicates.')  
#            listOfRunIndices = []
#            # check each run against listOfRunNumbers
#            for run in self.listOfRuns:
#                runNumber = run.runNumber
#                if runNumber in listOfRunNumbers:
#                    # add runIndex to list
#                    runIndex = run.runIndex
#                    listOfRunIndices.append(runIndex)
#                    # now remove runNumber from listOfRunNumbers (we know it is the only instance because we would have raised an error above otherwise).
#                    listOfRunNumbers.remove(runNumber)
#                    # and go to next run
#                    continue
#            return listOfRunIndices
#    def listOfInitialCompartmentIndices(self, listOfCompartmentNames=None):
#        listOfInitialCompartments = self.listOfInitialCompartments()
#        if listOfCompartmentNames is None:
#            return [compartment.compartment_index for compartment in listOfInitialCompartments]
#        else:
#            listOfCompartmentNames = copy(listOfCompartmentNames) # since we will modify listOfCompartmentNames we take a copy just to be safe.
#            if len(listOfCompartmentNames) > len(unique(copy(listOfCompartmentNames))):
#                raise ValueError('listOfCompartmentNames contains duplicates, therefore returned listOfInitialCompartmentIndices would contain duplicates.')  
#            listOfInitialCompartmentIndices = []
#            # check each compartment against listOfCompartmentNames
#            for compartment in listOfInitialCompartments:
#                compartmentName = compartment.compartment_name
#                if compartmentName in listOfCompartmentNames:
#                    # add compartmentIndex to list
#                    compartmentIndex = compartment.compartment_index
#                    listOfInitialCompartmentIndices.append(compartmentIndex)
#                    # now remove compartmentName from listOfCompartmentNames (we know it is the only instance because we would have raised an error above otherwise).
#                    listOfCompartmentNames.remove(compartmentName)
#                    # and go to next compartment
#                    continue
#            return listOfInitialCompartmentIndices
    
    
    def listOfSpeciesIndices(self, listOfSpeciesNames=None):
#        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfSpecies, 'species_index', listOfSpeciesNames, 'species_name')
        return [species.species_index for species in self.listOfSpecies if species.species_name in listOfSpeciesNames] if listOfSpeciesNames is not None else [species.species_index for species in self.listOfSpecies] 
    
    
    def listOfSpeciesNames(self, listOfSpeciesIndices=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfSpecies, 'species_name', listOfSpeciesIndices, 'species_index')

    
    def listOfRunIndices(self, listOfRunNumbers=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfRuns, 'runIndex', listOfRunNumbers, 'runNumber')

    
    def listOfRunNumbers(self, listOfRunIndices=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfRuns, 'runNumber', listOfRunIndices, 'runIndex')


    def listOfInitialCompartmentIndices(self, listOfCompartmentNames=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfInitialCompartments(), 'compartment_index', listOfCompartmentNames, 'compartment_name')


    def listOfInitialCompartmentNames(self, listOfCompartmentIndices=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfInitialCompartments(), 'compartment_name', listOfCompartmentIndices, 'compartment_index')
    
        
    def listOfInitialCompartments(self):
        if not hasattr(self, '_listOfInitialCompartments'):
            self._listOfInitialCompartments = []
            for compartment in self.listOfRuns[0].listOfCompartments:
                if not compartment.compartment_creation_time > self.startTime:
                    self._listOfInitialCompartments.append(Compartment.fromCompartment(compartment))
        return self._listOfInitialCompartments


    def initialAmounts(self,
                listOfSpeciesIndices=None, listOfSpeciesNames=None,
                listOfCompartmentIndices=None, listOfCompartmentNames=None,
                listOfTimepointIndices=None, listOfTimepoints=None,
                listOfRunIndices=None, listOfRunNumbers=None,
                ):
        return amounts(True,
                listOfSpeciesIndices, listOfSpeciesNames,
                listOfCompartmentIndices, listOfCompartmentNames,
                [0], None,
                listOfRunIndices, listOfRunNumbers) 


    def amountsInOneRun(self, runIndex=None, runNumber=None,
                         ignoreTruncatedRunIfSimulationHasManyRuns=False,
                         listOfSpeciesIndicies=None, listOfSpeciesNames=None,
                         listOfCompartmentIndices=None, listOfCompartmentNames=None,
                         listOfTimepointIndices=None, listOfTimepoints=None
                         ):
        assert runIndex is not None and runNumber is not None
        if runIndex is None:
            listOfRunIndices = self.listOfRunIndices([runNumber])
        elif runNumber is None:
            listOfRunNumbers = self.listOfRunNumbers([runIndex])
        return self.amounts(ignoreTruncatedRunIfSimulationHasManyRuns=ignoreTruncatedRunIfSimulationHasManyRuns,
                         listOfSpeciesIndicies=listOfSpeciesIndicies, listOfSpeciesNames=listOfSpeciesNames,
                         listOfCompartmentIndices=listOfCompartmentIndices, listOfCompartmentNames=listOfCompartmentNames,
                         listOfTimepointIndices=listOfTimepointIndices, listOfTimepoints=listOfTimepoints,
                         listOfRunIndices=listOfRunIndices, listOfRunNumbers=listOfRunNumbers)
        
        
    def amountsInAllRuns(self, ignoreTruncatedRunIfSimulationHasManyRuns=True,
                         listOfSpeciesIndicies=None, listOfSpeciesNames=None,
                         listOfCompartmentIndices=None, listOfCompartmentNames=None,
                         listOfTimepointIndices=None, listOfTimepoints=None
                         ):
        return self.amounts(ignoreTruncatedRunIfSimulationHasManyRuns=ignoreTruncatedRunIfSimulationHasManyRuns,
                         listOfSpeciesIndicies=listOfSpeciesIndicies, listOfSpeciesNames=listOfSpeciesNames,
                         listOfCompartmentIndices=listOfCompartmentIndices, listOfCompartmentNames=listOfCompartmentNames,
                         listOfTimepointIndices=listOfTimepointIndices, listOfTimepoints=listOfTimepoints,
                         listOfRunIndices=None, listOfRunNumbers=None)                    

    
    def amounts(self, ignoreTruncatedRunIfSimulationHasManyRuns=True,
                listOfSpeciesIndices=None, listOfSpeciesNames=None,
                listOfCompartmentIndices=None, listOfCompartmentNames=None,
                listOfTimepointIndices=None, listOfTimepoints=None,
                listOfRunIndices=None, listOfRunNumbers=None,
                chunkSize=2 ** 20):

        if listOfSpeciesIndices is None:
            if listOfSpeciesNames is not None:
                listOfSpeciesIndices = self.listOfSpeciesIndices(listOfSpeciesNames)
            else:
                listOfSpeciesIndices = self.listOfSpeciesIndices()
        # ensure that have the correct listOfSpeciesNames for the indices provided.
                listOfSpeciesNames = self.listOfSpeciesNames(listOfSpeciesIndices)
        elif listOfSpeciesNames is not None:
            listOfSpeciesNames = self.listOfSpeciesNames(listOfSpeciesIndices)
            print 'Overriding species names as indices are already specified.'
        
        if listOfCompartmentIndices is None: # will only use initial compartment indexes
            # use run.listOfCompartmentIndices if you want compartments that are created during the simulation.
            if listOfCompartmentNames is not None:
                listOfCompartmentIndices = self.listOfInitialCompartmentIndices(listOfCompartmentNames)
            else:
                listOfCompartmentIndices = self.listOfInitialCompartmentIndices()
                listOfCompartmentNames = self.listOfInitialCompartmentNames(listOfCompartmentIndices)
        elif listOfCompartmentNames is not None:
            listOfCompartmentNames = self.listOfInitialCompartmentNames(listOfCompartmentIndices)
            print 'Overriding compartment names as indices are already specified.'
            
        if listOfTimepointIndices is None:
            if listOfTimepoints is not None:
                print 'a'
                listOfTimepointIndices = listOfTimepointIndicesFromAnotherListOfTimepoints(listOfTimepoints, self.listOfTimepointsCommonToAllRuns())
            else:
                if ignoreTruncatedRunIfSimulationHasManyRuns:
                    print 'b'
                    listOfTimepoints = self.listOfTimepointsOfNonTruncatedRuns()
                    listOfTimepointIndices = self.listOfTimepointIndicesOfNonTruncatedRuns()
                else:
                    print 'c'
                    listOfTimepoints = self.listOfTimepointsCommonToAllRuns()
                    listOfTimepointIndices = self.listOfTimepointsIndicesCommonToAllRuns()
        elif listOfTimepoints is not None:
            if ignoreTruncatedRunIfSimulationHasManyRuns:
                print 'c'
                listOfTimepoints = self.listOfTimepointsFromListOfTimepointsOfNonTruncatedRuns(attributesOfListOfTimepoints(listOfTimepoints))
                listOfTimepointIndices = listOfTimepointIndicesFromListOfTimepoints(listOfTimepoints)
            else:
                print 'd'
                listOfTimepoints = self.listOfTimepointsCommonToAllRuns()
                listOfTimepointIndices = self.listOfTimepointsIndicesCommonToAllRuns()
            print 'Overriding timepoints as indices are already specified.'
            
            
        if listOfRunIndices is None:
            if listOfRunNumbers is not None:
                listOfRunIndices = self.listOfRunIndices(listOfRunNumbers)
            else:
                listOfRunIndices = self.listOfRunIndices()
                listOfRunNumbers = self.listOfRunNumbers(listOfRunIndices)
        elif listOfRunNumbers is not None:
            listOfRunNumbers = self.listOfRunNumbers(listOfRunIndices)
            print 'Overriding run numbers as indices are already specified.'

#        print listOfTimepoints
#        print listOfTimepointIndices

        startIndex, stopIndex, stepSize = attributesOfListOfTimepointsIndices(listOfTimepointIndices)
        
        maximumChunkSize = stopIndex - startIndex
        if chunkSize is not int:
            chunkSize = int(chunkSize)
        if chunkSize < 1:
            chunkSize = 1
        if chunkSize > maximumChunkSize:
            chunkSize = maximumChunkSize

        try:
            listOfAmountsInEachRun = []
            i = 0
            while i < len(listOfRunIndices):
                listOfAmountsInEachRun.append(zeros((len(listOfSpeciesIndices), len(listOfCompartmentIndices), len(listOfTimepointIndices))))
                i += 1
        except MemoryError, e:
            print e
            raise Exception('Out of memory due to too many runs. Try selecting fewer runs, a shorter time window or a larger step size.')
        
        try:
            file = tables.openFile(self.fileName)
        except IOError, e:
            print e
            return

        simulationNode = file.root
        for ri, runNumber in enumerate(listOfRunNumbers):
            runNode = simulationNode._f_getChild("run%s" % runNumber)

            startTimeIndex, stopTimeIndex, stepSize = attributesOfListOfTimepointsIndices(listOfTimepointIndices)
#            print startTimeIndex, stopTimeIndex, stepSize 

            amountsSlicedByTimepoints = runNode.amounts[:, :, startTimeIndex:stopTimeIndex:stepSize]
#            print amountsSlicedByTimepoints.shape
            
            for si, s in enumerate(listOfSpeciesIndices):
                for ci, c in enumerate(listOfCompartmentIndices):
#                    print ri, si, ci, s, c
#                    print listOfAmountsInEachRun[ri][si, ci, :].shape
#                    print amountsSlicedByTimepoints[s, c, :].shape
                    listOfAmountsInEachRun[ri][si, ci, :] = amountsSlicedByTimepoints[s, c, :]
        
        file.close()
        return Amounts(self, listOfAmountsInEachRun,
                       listOfSpeciesIndices, listOfSpeciesNames,
                       listOfCompartmentIndices, listOfCompartmentNames,
                       listOfTimepoints, listOfTimepointIndices,
                       listOfRunIndices, listOfRunNumbers)

        
        
        
        
#    mean = lambda array:d numpy.mean(array, axis=3)
#    std = lambda array: numpy.std(array, ddof=1, axis=3)
#    functions = (mean,)#std)
#
#    def get_averages(self):
#        try:
#            results = [] # list of 3D arrays to return in tuple
#            for fi, f in enumerate(SimulatorResults.functions):
#                stat = numpy.zeros((len(self.species_indices), len(self.compartment_indices), len(self.timepoints)), self.type)
#                results.append(stat)
#        except Exception, e:
##            raise Exception("Simulation is too large to hold in memory.\n"+
##                            "Try selecting fewer listOfSpecies, subcompartments, "+
##                            "a shorter time window or a larger step size.")
#            print e
#            return
#
#        # create large arrays handling failure
#        buffer = None
#        while buffer == None:
#            # allocate buffer (4-dimensional array)
#            try:
#                buffer = numpy.zeros((len(self.species_indices),
#                                      len(self.compartment_indices),
#                                      self.chunk_size,
#                                      len(self.run_indices)),
#                                      type)
#            except MemoryError:
#                # progressively halve chunk_size until buffer fits into memory
#                self.chunk_size = self.chunk_size // 2
#                buffer = None
#                continue
#
##            # try to get statistics from data in buffer
##            try:
##                for fi, f in enumerate(SimulatorResults.functions):
##                    f(buffer)
##            except MemoryError, e:
##                # progressively halve chunk_size until statistics can be done
##                self.chunk_size = self.chunk_size // 2
##                buffer = None
##                continue
#
#        def iteration(chunk_size):
#            """One iteration reads amounts into buffer and applies statistical functions to those amounts."""
#            self.amounts_chunk_end = amounts_chunk_start + (chunk_size * self.every)
#            for ri, r in enumerate(self.run_indices):
#                where = "%srun%s" % ('/', r)
#                amounts = h5.getNode(where, "amounts")[:, :, amounts_chunk_start:self.amounts_chunk_end:self.every]
#                for si, s in enumerate(self.species_indices):
#                    for ci, c in enumerate(self.compartment_indices):
#                        buffer[si, ci, :, ri] = amounts[s, c, :]
#            self.stat_chunk_end = stat_chunk_start + chunk_size
##            print results[1][:,:,stat_chunk_start:self.stat_chunk_end]
##            print "amounts.shape: ", amounts.shape, "buffer.shape: ", buffer.shape
##            print "buffer:"
##            print buffer
#            for fi, f in enumerate(SimulatorResults.functions):
#                stat = results[fi][:]
#                stat[:, :, stat_chunk_start:self.stat_chunk_end] = f(buffer)
##                print stat[:,:,stat_chunk_start:self.stat_chunk_end], "=", "std(", buffer, ")"
#
#        h5 = tables.openFile(self.filename)
#
#        amounts_chunk_start = self.start
#        stat_chunk_start = 0
#        # for each whole chunk
#        quotient = len(self.timepoints) // self.chunk_size
#        for i in range(quotient):
#            iteration(self.chunk_size)
#            amounts_chunk_start = self.amounts_chunk_end
#            stat_chunk_start = self.stat_chunk_end
#
#        # and the remaining timepoints           
#        remainder = len(self.timepoints) % self.chunk_size
#        if remainder > 0:
#            buffer = numpy.zeros((len(self.species_indices),
#                               len(self.compartment_indices),
#                               remainder,
#                               len(self.run_indices)),
#                               type)
#            iteration(remainder)
#
#        h5.close()
#        return (self.timepoints, results)




class Species(object):
    '''
    Contains values of an mcss simulation's species table entry.
    '''

    def __init__(self, species_index, species_name, simulation):
        self.species_index = species_index
        self.species_name = species_name

        self.simulation = simulation


    def __str__(self):
        return 'Species(species_index=%s, species_name=%s)' % (self.species_index, self.species_name)
        
        

class Rule(object):
    '''
    Contains values of an mcss simulation's rule_information table entry.
    '''

    def __init__(self, rule_template_index, rule_index, rule_id, rule_name, rule_x_target, rule_y_target, simulation):
        self.rule_template_index = rule_template_index
        self.rule_index = rule_index
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.rule_x_target = rule_x_target
        self.rule_y_target = rule_y_target

        self.simulation = simulation
    
    
    def __str__(self):
        return 'Rule(rule_template_index=%s, rule_index=%s, rule_id=%s, rule_name=%s, rule_x_target=%s, rule_y=target=%s)' % (
            self.rule_template_index, self.rule_index, self.rule_id, self.rule_name, self.rule_x_target, self.rule_y_target)
        

        
class RuleSet(object):
    '''
    Contains values of an mcss simulation's ruleset_information table entry.
    '''

    def __init__(self, ruleset_index, ruleset_name, ruleset_compartment_id, number_of_rules_in_ruleset, simulation):
        self.ruleset_index = ruleset_index
        self.ruleset_name = ruleset_name
        self.ruleset_compartment_id = ruleset_compartment_id
        self.number_of_rules_in_ruleset = number_of_rules_in_ruleset
        
        self.simulation = simulation
    
    
    def __str__(self):
        return 'RuleSet(ruleset_index=%s, ruleset_name=%s, ruleset_compartment_id=%s, number_of_rules_in_ruleset=%s)' % (
            self.ruleset_index, self.ruleset_name, self.ruleset_compartment_id, self.number_of_rules_in_ruleset)


        
class Run(object):
    '''
    Contains attributes of an mcss simulation's run node.
    '''

    def __init__(self,
                 attributes,
                 runNumber,
                 runIndex,
                 simulation
                 ):
        self.main_loop_start_time = attributes.main_loop_start_time
        self.number_of_compartments = attributes.number_of_compartments
        self.number_of_timepoints = attributes.number_of_timepoints
        self.preprocess_end_time = attributes.preprocess_end_time
        self.preprocess_start_time = attributes.preprocess_start_time
        self.run_end_time = attributes.run_end_time
        self.run_start_time = attributes.run_start_time
        self.simulated_time = attributes.simulated_time
        self.total_reactions_simulated = attributes.total_reactions_simulated
        self.main_loop_end_time = attributes.main_loop_end_time
        
        self.runNumber = runNumber
        self.runIndex = runIndex    
        self.simulation = simulation

        # timepoints, see also Run.listOfTimePoints(self)
        self.numberOfTimepoints = attributes.number_of_timepoints
        self.startTime = self.simulation.startTime
        self.stepTime = self.simulation.stepTime
        self.stopTime = self.numberOfTimepoints * self.stepTime # can be more than maxTime but that's ok because listOfTimepoints(stopTime) is exclusive 
        self.listOfTimepoints = listOfTimepoints(self.startTime, self.stopTime, self.stepTime) # the complete list of timepoints for this run 
#        print 'test', len(self.listOfTimepoints), self.listOfTimepoints
        self.listOfTimepointIndices = listOfTimepointIndices(self.startTime, self.stopTime, self.stepTime)
                
        # compartments
        self.listOfCompartments = []
        
        # amounts/levels
        self.hasAmounts = False
        
        # propensities
        self.hasPropensities = False
        
        # reactions
        self.hasReactions = False
        self.listOfReactions = []
        
        # volumes/positions
        self.hasVolumes = False
        self.listOfPositions = []


    def lastTimepoint(self):
        return self.listOfTimepoints[-1]
    

    def lastTimepointIndex(self):
        return self.listOfTimepointIndices[-1]
    

    def nearestTimepoint(self, time):
        return nearestTimepoint(self.listOfTimepoints, time)
    
    
    def nearestTimepointIndex(self, time):
        return nearestTimepointIndex(self.listOfTimepoints, time)       
    
    
    def listOfTimepointIndicesFromListOfTimepoints(self, startTime=None, stopTime=None, stepTime=None):
        ''' Returns the list of timepoint indices in this run (from startTime to stopTime inclusive, every stepSize timepoint). '''
        return listOfTimepointIndicesFromListOfTimepoints(self.listOfTimepoints, startTime, stopTime, stepTime)


    def listOfTimepointsFromListOfTimepoints(self, startTime=None, stopTime=None, stepTime=None):
        ''' Returns the list of timepoints in this run (from startTime to stopTime inclusive, every stepSize timepoint). '''
        return listOfTimepointsFromListOfTimepoints(self.listOfTimepoints, startTime, stopTime, stepTime)



    def listOfCompartmentIndices(self, listOfCompartmentNames=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfCompartments, 'compartment_index', listOfCompartmentNames, 'compartment_name')

    
    def listOfCompartmentNames(self, listOfCompartmentIndices=None):
        return listOfAttributeOfObjectFromListOfOtherAttributeOfObject(self.listOfCompartments, 'compartment_name', listOfCompartmentIndices, 'compartment_index')

    
    def listOfCompartmentsFromListOfCompartmentIndices(self, listOfCompartmentIndices=None):
        return [compartment for compartment in self.listOfCompartments if compartment.compartment_index in listOfCompartmentIndices] if listOfCompartmentIndices is not None else self.listOfCompartments


    def compartmentPositionBounds(self):
        #TODO extend with time
        xmax = max([compartment.compartment_x_position for compartment in self.listOfCompartments])
        xmin = min([compartment.compartment_x_position for compartment in self.listOfCompartments])
        ymax = max([compartment.compartment_y_position for compartment in self.listOfCompartments])
        ymin = min([compartment.compartment_y_position for compartment in self.listOfCompartments])
        return (xmin, xmax, ymin, ymax)
        
        
    def compartmentPositionBoundsFromListOfCompartments(self, listOfCompartments):
        raise NotImplementedError

        
    def amountsSlice(self, speciesIndex, compartmentIndex, firstTimepointIndexInclusive=0, lastTimepointIndexExclusive= -1, stepSize=1):
        '''
        Returns a list of quantities of 1 species in 1 compartment for a subset of timepoints.
        '''
        if not self.hasAmounts:
            raise AttributeError('Run%s has no amounts array, perhaps the simulation %s was run with the log_type parameter set to \'reactions\'.' % (self.runNumber, self.simulation.fileName))
        try:
            file = tables.openFile(self.simulation.fileName, 'r')
            # except exceptions here
            simulationNode = file.root
            runNode = simulationNode._f_getChild("run%s" % self.runNumber)
            amounts = runNode.amounts
#            amountsShape = amounts.shape; print amountsShape
            slice = amounts[speciesIndex, compartmentIndex, firstTimepointIndexInclusive:lastTimepointIndexExclusive:stepSize] 
        except Exception, e:
            print e
            raise NotImplementedError('Run.amountsSlice()')
        finally:
            file.close()
        return slice

    
    def volumesSlice(self, compartmentIndex, firstTimepointIndexInclusive, lastTimepointIndexExclusive, stepSize):
        if not self.hasVolumes:
            raise AttributeError('Run%s has no volumes array, perhaps the simulation %s was run with the log_volumes parameter set to \'0\'.' % (self.runNumber, self.simulation.fileName))
        
        slice = []
        try:
            file = tables.openFile(self.simulation.fileName, 'r')
            # except exceptions here
            simulationNode = file.root
            runNode = simulationNode._f_getChild("run%s" % self.runNumber)
            volumes = runNode.volumes
#            volumesShape = volumes.shape; print volumesShape
            slice = volumes[compartmentIndex, firstTimepointIndexInclusive:lastTimepointIndexExclusive:stepSize]
        except Exception, e:
            print e
            raise NotImplementedError('Run.volumesSlice()')
        finally:
            file.close()    
        return slice

    
    def reactions(self):
        if not self.hasReactions:
            raise AttributeError('Run%s has no reactions table, perhaps the simulation %s was run with the log_type parameter set to \'levels\'.' % (self.runNumber, self.simulation.fileName))
        return self.listOfReactions

    
    def positions(self):
        if not self.hasVolumes:
            raise AttributeError('Run%s has no positions table, perhaps the simulation %s was run with the log_volumes parameter set to \'0\'.' % (self.runNumber, self.simulation.fileName))
        return self.listOfPositions
    
    
    def __str__(self):
        return 'from start to %s: %s' % (self.stopTime, self.listOfTimepoints)    
    
    
        
class Compartment(object):
    '''
    Contains values of an mcss simulation run's compartment table entry.
    '''
    
    @classmethod
    def fromCompartment(cls, compartment):
        ''' Copy constructor, used for Simulation.initialCompartments() '''
        return Compartment(compartment.compartment_index,
                           compartment.compartment_id,
                           compartment.compartment_name,
                           compartment.compartment_x_position,
                           compartment.compartment_y_position,
#                           compartment.compartment_z_position,
                           compartment.compartment_template_index,
                           compartment.compartment_creation_time,
                           compartment.compartment_destruction_time,
                           compartment.run,
                           compartment.simulation
                           )


    def __init__(self, compartment_index, compartment_id, compartment_name, compartment_x_position, compartment_y_position, compartment_template_index, compartment_creation_time, compartment_destruction_time, run, simulation):
        self.compartment_index = compartment_index
        self.compartment_id = compartment_id
        self.compartment_name = compartment_name
        self.compartment_x_position = compartment_x_position
        self.compartment_y_position = compartment_y_position
#        self.compartment_z_position = compartment_z_position
        self.compartment_template_index = compartment_template_index
        self.compartment_creation_time = compartment_creation_time
        self.compartment_destruction_time = compartment_destruction_time        

        self.run = run
        self.simulation = simulation
            
            
    def index(self):
        return self.compartment_index
    
    
    def name(self):
        return self.compartment_name
    
    
    def xPosition(self):
        return self.compartment_x_position
    
    
    def yPosition(self):
        return self.compartment_y_position


    def zPosition(self):
        return self.compartment_z_position


    def coordinates(self):
        return (self.xPosition(), self.yPosition())


    def nameAndCoordinates(self):
        return "%s %s" % (self.compartment_name, self.coordinates())

    
    def __str__(self):
        return 'Compartment(compartment_index=%s, compartment_id=%s, compartment_name=%s, compartment_x_position=%s, compartment_y_position=%s, compartment_template_index=%s, compartment_creation_time=%s, compartment_destruction_time=%s)' % (
            self.compartment_index, self.compartment_id, self.compartment_name, self.compartment_x_position, self.compartment_y_position, self.compartment_template_index, self.compartment_creation_time, self.compartment_destruction_time)
    


class Reaction(object):
    '''
    Contains values of an mcss simulation's run reactions table entry.
    '''

    def __init__(self, time, species_index, species_amount, compartment_index, rule_index, run, simulation):
        self.time = time
        self.species_index = species_index
        self.species_amount = species_amount
        self.compartment_index = compartment_index
        self.rule_index = rule_index

        self.run = run
        self.simulation = simulation
    
    
    def __str__(self):
        return 'Reaction(time=%s, species_index=%s, species_amount=%s, compartment_index=%s, rule_index=%s)' % (
            self.time, self.species_index, self.species_amount, self.compartment_index, self.rule_index)
        


class Position(object):
    '''
    Contains values of an mcss simulation's run's positions table entry.
    '''

    def __init__(self, compartment_creation_time, compartment_index, compartment_x_position, compartment_y_position, run, simulation):
        self.compartment_creation_time = compartment_creation_time #TODO should this be movement time?
        self.compartment_index = compartment_index
        self.compartment_x_position = compartment_x_position
        self.compartment_y_position = compartment_y_position
    
        self.run = run
        self.simulation = simulation


    def __str__(self):
        return 'Position(compartment_creation_time=%s, compartment_index=%s, compartment_x_position=%s, compartment_y_position=%s)' % (
            self.compartment_creation_time, self.compartment_index, self.compartment_x_position, self.compartment_y_position)

    
#TODO nose


class Amounts(object):
    '''
    Holds a 4D array of amounts[species, compartments, timepoints, runs],
    and a collection of lists of the original indices and names whose 
    current indices correspond to the those in the array.
    '''
    
    def __init__(self, listOfAmountsInEachRun, listOfCompartmentIndices, listOfCompartmentNames, listOfRunIndices, listOfRunNumbers, listOfSpeciesIndices, listOfSpeciesNames, listOfTimepointIndices, listOfTimepoints, simulation):
        self.simulation = simulation
        self.listOfAmountsInEachRun = listOfAmountsInEachRun # list of amounts arrays, one for each run in listOfRunIndices
        self.listOfSpeciesIndices = listOfSpeciesIndices
        self.listOfSpeciesNames = listOfSpeciesNames
        self.listOfCompartmentIndices = listOfCompartmentIndices
        self.listOfCompartmentNames = listOfCompartmentNames
        self.listOfTimepointIndices = listOfTimepointIndices
        self.listOfTimepoints = listOfTimepoints
        self.listOfRunIndices = listOfRunIndices
        self.listOfRunNumbers = listOfRunNumbers


    # functions for obtaining index/indices for use with functions that extract amounts from listOfAmountsInEachRun

    def indexFromSpeciesIndex(self, speciesIndex):
        return self.listOfSpeciesIndices.index(speciesIndex)
    def indicesFromSpeciesIndices(self, speciesIndices):
        return [self.indexFromSpeciesIndex(index) for index in speciesIndices]
    def indexFromSpeciesName(self, speciesName):
        return self.listOfSpeciesNames.index(speciesName)
    def indicesFromSpeciesNames(self, speciesNames):
        return [self.indexFromSpeciesName(speciesName) for speciesName in speciesNames]
    
    def indexFromCompartmentIndex(self, compartmentIndex):
        return self.listOfCompartmentIndices.index(compartmentIndex)
    def indicesFromCompartmentIndices(self, compartmentIndices):
        return [self.indexFromCompartmentIndex(index) for index in compartmentIndices]
#    def indexFromCompartmentName(self, compartmentName):
#        return self.listOfCompartmentNames.index(compartmentName)
#    def indicesFromCompartmentNames(self, compartmentNames):
#        return [self.indexFromCompartmentName(compartmentName) for compartmentName in compartmentNames]
    
    def indexFromTimepointIndex(self, timepointIndex):
        return self.listOfTimepointsIndices.index(timepointIndex)
    def indicesFromTimepointIndices(self, timepointIndices):
        return [self.indexFromTimepointIndex(index) for index in timepointIndices]
    def indexFromTimepoint(self, timepoint):
        for i, t in enumerate(self.listOfTimepoints):
            if t == timepoint:
                return i
        raise ValueError('timepoint not found in listOfTimepoints')
    def indicesFromTimepoints(self, timepoints):
        return [self.indexFromTimepoint(timepoint) for timepoint in timepoints]
    
    def indexFromRunIndex(self, runIndex):
        return self.listOfRunIndices.index(runIndex)
    def indicesFromRunIndices(self, runIndices):
        return [self.indexFromRunIndex(index) for index in runIndices]
    def indexFromRunNumber(self, runNumber):
        return self.listOfRunNumbers.index(runNumber)
    def indicesFromRunNumbers(self, runNumbers):
        return [self.indexFromRunNumber(runNumber) for runNumber in runNumbers]
    

    # functions for extract amounts from listOfAmountsInEachRun

    def amountsOfOneSpeciesInAllCompartmentsAtOneTimepointInOneRun(self,
        speciesIndex,
        timepointIndex,
        runIndex):
        '''
        Returns a 1D array [compartment] for one species at one timepoint in 
        one run.
        '''
        return self.listOfAmountsInEachRun[runIndex][speciesIndex, :, timepointIndex] 
    
    def amountsOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(self,
        speciesIndex,
        runIndex):
        '''
        Returns a 2D array of amounts[compartment, timepoint] for one 
        species at all timepoints of one run.
        
        Usage:
        simulation = Simulation('simulation.h5')
        amounts = simulation.amounts(listOfSpeciesNames=['A','B'], listOfRunNumbers=[1])
        speciesIndex = amounts.indexFromSpeciesName('B')
        runIndex = amounts.indexFromRunNumber(1)
        print amounts.amountsOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(speciesIndex, runIndex)
        '''
        return self.listOfAmountsInEachRun[runIndex][speciesIndex, :, :]
    
    def amountsOfOneSpeciesInAllCompartmentsAtManyTimepointsInOneRun(self,
        speciesIndex,
        listOfTimepointIndices,
        runIndex):
        '''
        Returns a 2D array of amounts[compartment, timepoint] for one 
        species at *some* timepoints of one run.
        '''
        startTimeIndex, stopTimeIndex, stepTimeIndex = attributesOfListOfTimepointsIndices(listOfTimepointIndices)
        print startTimeIndex, stopTimeIndex, stepTimeIndex
        return self.listOfAmountsInEachRun[runIndex][speciesIndex, :, startTimeIndex:stopTimeIndex:stepTimeIndex]
    

    def amountsOfManySpeciesInManyCompartmentsAtManyTimepointInManyRuns(self,
        speciesIndices,
        compartmentIndicies,
        timepointIndices,
        runIndices):
        '''
        Returns a list of 3D arrays [species, compartment, timepoint] for 
        each species in each compartment at each timepoint for each run.
        
        Usage:
        simulation = Simulation('simulation.h5')
        amounts = simulation.amounts(listOfSpeciesNames=['A','B'], listOfRunNumbers=[1])
        speciesIndices = amounts.indicesFromSpeciesName(['A','B'])
        compartmentIndicies = amounts.indicesFromCompartmentIndices([0,1])
        timepointIndicies = amounts.indicesFromTimepoints([0])
        runIndicies = amounts.indicesFromRunNumbers([1])
        print amountsOfManySpeciesInManyCompartmentsAtManyTimepointInManyRuns(speciesIndices, compartmentIndicies, timepointIndicies, runIndicies)
        '''
        listOfAmountsInEachRun = []
        raise NotImplementedError
        return listOfAmountsInEachRun
    
    def functionOfAmountsOfManySpeciesInManyCompartmentsAtManyTimepointsInManyRuns(self,
        function,
        speciesIndices,
        compartmentIndicies,
        timepointIndices,
        runIndices):
        '''
        Returns a 3D array [species, compartment, timepoint] of a function 
        applied to the amount of each species in each compartment at each 
        timepoint for all runs.
        '''
        raise NotImplementedError
    
    def amountsOfOneSpeciesInOneCompartmentAtAllTimepointsInAllRuns(self,
        speciesIndex,
        compartmentIndex):
        ''' 
        Returns a 2D array [run x timepoint] for one species in one compartment.
        '''
        amounts = array([self.listOfAmountsInEachRun[ri][speciesIndex, compartmentIndex, :] for ri in range(len(self.listOfRunIndices))])#for ri, ori in enumerate(self.listOfRunIndices)])
        return amounts
    

#    def amountsOfManySpeciesInOneCompartmentAtAllTimepointsInAllRuns(self,
#        speciesIndices,
#        compartmentIndex):
#        '''
#        Returns a list of 2D arrays [species x timepoint] for each species 
#        in one compartment at all timepoints in each run.
#        '''
#        listOfAmountsInEachRun = array([self.listOfAmountsInEachRun[ri][speciesIndex, compartmentIndex, :] for ri in range(len(self.listOfRunIndices))])#for ri, ori in enumerate(self.listOfRunIndices)])
#        return listOfAmountsInEachRun
    

    # sum_compartments_at_same_xy_lattice_position = True
    def surfaceHistoryOfSumOfAmountsAtEachPositionOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(self,
        speciesIndex,
        runIndex):
        ''' Returns a 3D array [compartment_x_position, compartment_y_point, timepoint]. '''
        
#        self.listOfAmountsInEachRun[runIndex][speciesIndex, :, :]

#        listOfCompartments = self.simulation.listOfInitialCompartments()
        run = self.simulation.listOfRuns[runIndex]
        listOfCompartments = run.listOfCompartments

        print self.listOfTimepoints

        xmin, xmax, ymin, ymax = run.compartmentPositionBounds() 
        amounts = zeros(((xmax - xmin) + 1, (ymax - ymin) + 1, len(self.listOfTimepoints) - 1))
        print amounts.shape
        for ci, c in enumerate(listOfCompartments):
#            print amounts[c.compartment_x_position, c.compartment_y_position, :].shape
#            print self.listOfAmountsInEachRun[runIndex][speciesIndex, ci, :].shape
            amounts[c.compartment_x_position, c.compartment_y_position, :] = self.listOfAmountsInEachRun[runIndex][speciesIndex, ci, :] + amounts[c.compartment_x_position, c.compartment_y_position, :]

        surfaceHistory = SurfaceHistory(amounts, listOfCompartments, self.listOfTimepoints, self.listOfTimepointIndices)
        
        return surfaceHistory


    def surfaceHistoriesOfSumOfAmountsAtEachPositionOfManySpeciesInAllCompartmentsAtAllTimepointsInOneRun(self,
        listOfSpeciesIndicies,
        runIndex):
        ''' Returns a list of 3D arrays [species][compartment_x_position, compartment_y_point, timepoint]. '''
        surfaceHistories = []
        for speciesIndex in listOfSpeciesIndicies:
            surfaceHistories.append(self.surfaceHistoryOfSumOfAmountsAtEachPositionOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(speciesIndex, runIndex))
        return surfaceHistories
#        # create a MayaVi2 surface with a surfaceHistory (from SimulatorResults.getSurfaces(self))
#        zmax = numpy.max(results)
#        extent = [xmin, xmax, ymin, ymax, 0, zmax]
#        if zmax == 0: # not
#            print "%s never amounts to anything." % s.name
#        warp_scale = (1 / zmax) * 10 #FIXME magic number! # necessary?
#        surface = Surface(array, warp_scale, extent, s.name, self.timepoints)
#        surfaces.append(surface)




class Surface(object):
    def __init__(self, amounts, listOfCompartments):
        self.amounts = amounts
        self.listOfCompartments = listOfCompartments
    def compartmentsAt(self, x, y):
        return [compartment for compartment in self.listOfCompartments if compartment.x_position == x and compartment.y_position == y]
    
    
    
class SurfaceHistory(Surface):
    def __init__(self, amounts, listOfCompartments, listOfTimepoints, listOfTimepointIndices):
        Surface.__init__(self, amounts, listOfCompartments)
        self.listOfTimepoints = listOfTimepoints
        self.listOfTimepointIndices = listOfTimepointIndices
    def surfaceAt(self, timepointIndex):
        return Surface(self.amounts[:, :, timepointIndex], self.listOfCompartments)
    def indexFromTimepoint(self, timepoint):
        for i, t in enumerate(self.listOfTimepoints):
            if t == timepoint:
                return i
        raise ValueError('timepoint not found in listOfTimepoints')
    def indexFromTimepointIndex(self, timepointIndex):
        return self.listOfTimepointsIndices.index(timepointIndex)


def save_array_as_image(filename, array, colourmap=None, vmin=None, vmax=None, format=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib import cm

    figure = Figure(figsize=array.shape[::-1], dpi=1, frameon=False)
    FigureCanvas(figure) # essential even though it isn't used
    figure.figimage(array, cmap=cm.get_cmap(colourmap), vmin=vmin, vmax=vmax, origin=origin)
    figure.savefig(filename, dpi=1, format=format)
    
    
if __name__ == '__main__':
##    a = array([[0,1],[0,1,2]])
#    a = arange(1,28,1).reshape(3,3,3)
##    print a[(0,0,0)] # 1 
##    print a[(1,1,1)] # 14 
##    print a[(2,2,2)] # 27
##    print a[([0,1,2],0,0)] # 1 
#
#    indices = [0,1]
##    print a[(indices,0,indices)]

    simulation = Simulation.fromH5File('/home/jvb/phd/models/circularPattern_05.h5')
    print simulation.listOfListOfCompartmentsInAllRuns
#    print simulation.listOfTimepointsOfNonTruncatedRuns()
#    print simulation.listOfInitialCompartmentNames()
#    print simulation.listOfSpeciesNames()
#    print simulation.listOfRunNumbers()
    amounts = simulation.amounts()#listOfSpeciesNames=['FP1'], listOfTimepoints=[1200])
##    amounts.amountsOfOneSpeciesInOneCompartmentAtAllTimepointsInAllRuns()
#    print amounts.amountsOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(
#        amounts.indexFromSpeciesName('FP1'), amounts.indexFromRunNumber(1))
#    
#    print amounts.amountsOfOneSpeciesInOneCompartmentAtAllTimepointsInAllRuns(
#        amounts.indexFromSpeciesIndex(1), amounts.indexFromCompartmentIndex(1000))
#
#    print amounts.amountsOfOneSpeciesInAllCompartmentsAtOneTimepointInOneRun(
#        amounts.indexFromSpeciesIndex(4), amounts.indexFromTimepoint(1200), amounts.indexFromRunIndex(0))
#    

    print simulation.listOfTimepointsOfNonTruncatedRuns()
    print simulation.listOfRuns[0].number_of_timepoints
    print simulation.listOfRuns[-1].number_of_timepoints

#    speciesName = 'FP1'
#    surfaceHistory = amounts.surfaceHistoryOfSumOfAmountsAtEachPositionOfOneSpeciesInAllCompartmentsAtAllTimepointsInOneRun(
#        amounts.indexFromSpeciesName(speciesName),
#        amounts.indexFromRunNumber(1))
#    
##    print surfaceHistory.listOfTimepoints, len(surfaceHistory.listOfTimepoints)
##    print surfaceHistory.indexFromTimepoint(1200)
#    print surfaceHistory.amounts.shape
#    print surfaceHistory.surfaceAt(-1).amounts
#    print surfaceHistory.surfaceAt(-1).amounts.shape
#
#    save_array_as_image('/home/jvb/Desktop/surfaceHistory.surfaceAt(-1).png', surfaceHistory.surfaceAt(-1).amounts)
    
##    print 'fileName=%s' % simulation.fileName
##    print 'md5sum=%s' % simulation.md5sum
##    print 'originalFileName=%s' % simulation.originalFileName
##    print 'originalModelFileName=%s' % simulation.originalModelFileName
##    print
##    
##    for species in simulation.listOfSpecies:
##        print species
##    print
##    
##    for rule in simulation.listOfRules:
##        print rule
##    print
##    
##    for ruleSet in simulation.listOfRuleSets:
##        print ruleSet
##    print
##    
##    print 'startTime=%s' % simulation.startTime
##    print 'maxTime=%s' % simulation.maxTime
##    print
##    
##    print 'numberOfRuns=%s' % simulation.numberOfRuns
##    print len(simulation.listOfRuns)
##    
##    for run in simulation.listOfRuns:
##        print run
##    print
##    
##    for compartment in simulation.listOfRuns[0].listOfCompartments:
##        print compartment
##    print
##        
##    print simulation.listOfNumberOfCompartmentsInAllRuns
##    print simulation.listOfListOfCompartmentsInAllRuns
##    print
##    
##    print simulation.listOfListOfPositionsInAllRuns
##    print
##    
##    print simulation.listOfNumberOfReactionsInAllRuns
##    print simulation.listOfListOfReactionsInAllRuns
##    print
##    
##    print simulation.listOfInitialCompartments()
#
#    
##    listOfSpeciesIndices = range(0,2)
##    compartmentsIndices = range(1,3)
##    timepointsIndices = range(0,10)
##    runIndices = range(0,2)
##    amounts = zeros((len(listOfSpeciesIndices), len(compartmentsIndices), len(timepointsIndices), len(runIndices)))
##    print amounts.shape
##    # use index-arrays to extract amount across multiple runs?
#
#    #print 'simulation.stopTimeCommonToAllRuns()', simulation.stopTimeCommonToAllRuns()
#    
#    #print 'simulation.stopTimeIndexCommonToAllRuns()', simulation.stopTimeIndexCommonToAllRuns()
#    
#    #print 'simulation.listOfTimepointsCommonToAllRuns()', len(simulation.listOfTimepointsCommonToAllRuns()), simulation.listOfTimepointsCommonToAllRuns()
#    
#    #print 'simulation.listOfTimepointsIndicesCommonToAllRuns()', len(simulation.listOfTimepointsIndicesCommonToAllRuns()), simulation.listOfTimepointsIndicesCommonToAllRuns()
#    
##    print simulation.listOfTimepointsFromListOfTimepointsCommonToAllRuns(200, 250, 2)
#    #print listOfTimepointsFromListOfTimepoints(simulation.listOfTimepointsCommonToAllRuns(), 200, 505, 0.5)
#    
##    print simulation.listOfTimepointIndicesFromListOfTimepointsCommonToAllRuns(200, 250, 0.5)
#    
#    print simulation.listOfSpeciesNames([1,2,4])
#    print simulation.listOfSpeciesNames()
#    print simulation.listOfSpeciesNames([1,1,4])
#    
#    #print simulation.listOfRunIndices()
#    
#    #print simulation.listOfSpeciesNames()
#    #print simulation.speciesIndex('A')
#    #print simulation.listOfSpeciesIndices(['A','D'])
#    #
#    #print simulation.listOfInitialCompartments()
#    #print simulation.listOfInitialCompartmentIndices()
#    
##    for run in simulation.listOfRuns:
##        pass
#    run = simulation.listOfRuns[1]
##    #    print run.timepointIndex(500)
##    print run.listOfTimepointsFromListOfTimepoints(200, stepTime=4)
#    print run.listOfTimepointIndicesFromListOfTimepoints(0, 5000, 0.5)
#    print run.listOfTimepoints[1681]
##    print run.listOfCompartmentIndices()
##    print run.listOfCompartmentNames()
##    print attributesOfListOfTimepoints(run.listOfTimepoints)
#
##timepoints = listOfTimepoints(0,10,0.33)
##print timepoints
##n = 10
##print nearestTimepointIndex(timepoints, n)
##print nearestTimepoint(timepoints, n)

#    print listOfTimepoints(0,11,2)[listOfTimepointIndicesFromAnotherListOfTimepoints(listOfTimepoints(0,11,1), listOfTimepoints(0, 11, 2))]
