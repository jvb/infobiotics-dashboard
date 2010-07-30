*******************************************
Specification of Multi-cellular Systems
******************************************* 

Finally, a model of a multi-cellular system with cell types represented by the *SP-systems*,  *SP*\ :sub:`1`, ..., *SP*\ :sub:`n` and spatial distribution captured in a finite point lattice *Lat* is specified as a **Lattice Population P-system** which distributes many clones of the different cell types over the corresponding lattice points.

The polygon associated with each point is used to represent the shape of the correspoding cell. The neighbours associated with each point is used when a rule of the form below moving objects to the outside of a compartment is applied in the outermost membrane of a SP-system. In this case one the SP-system located in the neighbour points is chosen randomly and the corresponding objects are placed in its outermost compartment. 

An LPP-system enumerates the SP-systems representing the different individual cell types, the finite point lattice describing the geometry of the multi-cellular system and a **position function** that assigns a SP-system with each point of the lattice. 

The model of a multi-cellular system as a LPP-system must be specified in a text file with the extension, *.lpp*.  The different components of the model are specified according to the following format::


   LPPsystem modelName

       SPsystems
          ...
       endSPsystems

       lattice latticeName from latticeFile

       spatialDistribution
           ...
       endSpatialDistribution

   endLPPsystem

The model of the multi-cellular system is identified with *modelName*. In the block *SPsystems ... endSPsystems* the models of the **individual cell types** as SP-systems must be enumerated stating the file where they are defined. An individual cell type modelled as a  SP-system identified with *cellTypeName* in file *fileName.sps* is declared as::

  SPsystem cellTypeName from fileName.sps 

Recall that the individual cell types can also be specified in SBML format. In this case the declaration of a cell type is exactly as above except that the extension of the file containing the model must have the extension *.sbml*. 

The **finite point lattice** capturing the geometry of the multi-cellular system is introduced by specifying an identifier *latticeName* and the file where it is defined using the key word *from*.

Finally, the **spatial distribution** of the different clones of cell types over the lattice points is specified within the block *spatialDistribution ... endSpatialDistribution*. Each SP-system identified with *SPsystemName* is associated with a set of positions occupied by cells of the corresponding type. This is specified using the block *positions for SPsystemName ... endPositions*::

          positions for boundaryCell
             parameters
                ...
             endParameters
             coordinates
                ...
             endCoordinates
          endPositions

Here the coordinates of the lattice points are declared in the block:: 

   coordinates 
      x = coordinate1 
      y = coordinate2
   endCoordinates

The values coordinate1 and coordinate2 can be specified as mathematical formulas using parameters. These parameters can be defined as taking values within a given range [ *lowerBound* ... *upperBound* ] with a specified *step* within the block *parameters ... endParameters* as *parameter parameterName = lowerBound : step : upperBound*::

             parameters
                parameter parameterName = lowerBound:step:upperBound
                ...
             endParameters

For example::

   LPPsystem pulsePropagation
      
      SPsystems
          SPsystem senderCell from senderCell.sps
          SPsystem pulsingCell from pulsingCell.sps
          SPsystem boundaryCell from pulsingCell.sps
      endSPsystems

      lattice rectangular from lattice.lat

      spatialDistribution

          positions for boundaryCell
             parameters
                parameter i = 0:1:51
                parameter j = 0:11:11
             endParameters
             coordinates
                x = i
                y = j
             endCoordinates
          endPositions
			
          positions for boundaryCell
             parameters
                parameter i = 0:51:51
                parameter j = 0:1:10
             endParameters
             coordinates
                x = i
                y = j
             endCoordinates
          endPositions

          positions for senderCell
             parameters
                parameter i = 1:1:5
                parameter j = 1:1:10
             endParameters
             coordinates
                x=i
                y=j
             endCoordinates
          endPositions

          positions for pulsingCell
             parameters
                parameter i=6:1:50
                parameter j=1:1:10
             endParameters
		
             coordinates
                x=i
                y=j
             endCoordinates

          endPositions

      endSpatialDistribution
   endLPPsystem  