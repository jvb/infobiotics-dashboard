############################################
Multi-compartmental Stochastic Simulations
############################################

===============
Introduction
===============

mcss is an application for simulating multi-compartment stochastic P system models. mcss takes a model specified in SBML and simulates it using the multi-compartment Gillespie algorithm. A large number of spatially-distributed compartments containing many chemical species, reactions and transportation channels can be simulated. Templates can be specified which define a set of reactions which can be reproduced in many compartments. mcss is being used to develop Systems/Synthetic Biology computational models of plant systems and bacterial colonies.

===============
Installlation
=============== 

For instructions on how to compile and install mcss, see the README file included with the mcss distribution. 

================
Running mcss
================

Once installed, mcss is run by typing the following command:: 
$ mcss PARAMETER_FILE PARAMETER=VALUE PARAMETER=VALUE ... 
where PARAMETER_FILE is the filename of an mcss parameter file. Parameters specified on the command line following the filename override the parameters in the parameter file. For example, to run the module1 model provided in the examples directory of the mcss distribution, change to this directory and type:: 
$ mcss module1.params 
mcss saves the output of the simulation as a HDF5 data file, the filename of which can be specified in the parameter file. For example, after running the module1 model as described above, the file module1.h5 is created containing the results of the simulation. The mcss-postprocess application, which is included in the mcss distribution, can be used to extract information from the HDF5 output file. Alternatively, the standard HDF5 utilities can be used to examine this file. See http://hdf.ncsa.uiuc.edu/HDF5/ for more information on HDF5. 

=======================
mcss parameter files
=======================

The mcss parameter file is used to provide information to mcss and control various aspects of the simulation. It is in an XML format which has the general form::

  <parameters>
    <parameterSet name="SimulationParameters">
      <parameter name="PARAMETER NAME" value="PARAMETER VALUE"/>
      <parameter name="PARAMETER NAME" value="PARAMETER VALUE"/>
      ...
    </parameterSet>
  </parameters> 

See the parameter files for the example models for some examples. The allowed parameters are given in the table below. 

=========================
Model specification
=========================

CellDesigner v3.5.2 (http://www.celldesigner.org/) is used to graphically design a model, which is then exported as SBML Level 2. See the example models supplied with the mcss distribution for some examples. Once the model has been designed, export it from CellDesigner by selecting "Export Pure Level 2 Version 1" from the File menu. 

Compartment specification
-------------------------------------------------------------

In mcss, compartment names are used to provide information on the templates the compartment defines or uses, and the position of the compartment. This information is given in the SBML name attribute in a number of colon-separated fields. The names of compartments can be changed in CellDesigner by right clicking the compartment and selecting "Change Identity...". 

Compartments must be named as follows::

  name:t:a,b,...:x,y 

where, 
  * name is a string (not necessarily unique) which describes the compartment, 
  * t is a unique non-negative integer identifying the template the compartment defines, 
  * a,b,... is a comma-separated list of non-negative integers giving the identifiers of the templates the compartment uses, 
  * x,y is the position of the compartment, where x and y are non-negative integers. 
Some of these field may be empty, depending on the role of the compartment in the model. 

For example, all of the following are valid compartment names: 
  * bacteria:1:: 
  * bacteria::1:0,1 
  * reaction1:2::0,0 
  * reaction2:3:2:0,1 
  * compartment::2,3:1,3 
In the first example, "bacteria:1::", the first colon-separated field indicates that the compartment has the name bacteria. The second field indicates that this compartment defines a template with identifier 1. Compartments which define a template are automatically assumed to use the template they define. The third field is empty, indicating that this compartment uses no templates other than the one it defines. The fourth field is also empty, indicating that this compartment is a pure template which defines a set of rules but will not itself be included in the model. 

In the second example, "bacteria::1:0,1", the first field indicates that the compartment has the name bacteria. The second field is empty, indicating that this compartment does not define any templates. The third field indicates that the compartment uses the set of rules defined by the template with identifier 1. The fourth field indicates that the compartment is located at position (0,1). 

In the third example, "reaction1:2::0,0", the first field indicates that the compartment has the name reaction1. The second field indicates that this compartment defines a template with identifier 2. The third field is empty, indicating that this compartment uses no templates other than the one it defines. The fourth field indicates that the compartment is located at position (0,0). 

In the fourth example, "reaction2:3:2:0,1", the first field indicates that the compartment has the name reaction2. The second field indicates that this compartment defines a template with identifier 3. The third field indicates that, in addition to the template it defines, this compartment also uses the set of rules defined by the template with identifier 2. The fourth field indicates that the compartment is located at position (0,1). 

In the fifth example, "compartment::2,3:1,3", the first field indicates that the compartment has the name compartment. The second field is empty, indicating that this compartment does not define any templates. The third field indicates that the compartment uses the set of rules defined by the templates with identifiers 2 and 3. The fourth field indicates that the compartment is located at position (1,3). 

See the example models included with the mcss distribution for more examples. 

Reaction specification
---------------------------------------------------
A number of different unimolecular and bimolecular reactions can be simulated. See the reaction1 model in the examples directory for examples of all the reactions that can be simulated. 

Reactions whose reactants and products are all in the same compartment must be named as follows:: 

  name 

where name is a string (not necessarily unique, may be empty) which identifies the reaction. To specify this name in CellDesigner, right click the reaction and select "Change Identity...". 

Reactions whose products are in a different compartment to their reactants must be named as follows:: 

  name:x,y 

where name is a string (not necessarily unique, may be empty) which identifies the reaction, and x,y is a vector specifying the offset to compartment the products are to be placed in, where x and y are integers. For example, if a reactions named re1:1,0 is defined in a compartment with position (1,3), then the reaction will place its products in the compartment at position (1,3)+(1,0)=(2,3) i.e. the compartment on its right. If the reaction was named re1:0,-1 then its products would be placed in the compartment at position (1,3)+(0,-1)=(1,2) i.e. the compartment above. 

A reaction constant must also be specified for each reaction. To specify this constant in CellDesigner, right click on the reaction and select "Edit Reaction...". Now click the KineticLaw Edit button. Due to a bug in libSBML, the "math" box at the top must contain something, so enter the id of the reaction constant. Click on the New button to create a new parameter, and enter the id (arbitrary) of the reaction constant, for example "c1", and a value for this constant. Only create one parameter for each reaction. 

Reaction constants can also be sampled from distributions. Create the constant as described above, entering the id of the reaction constant, and in the same window, change the "constant" option from true to false. The distribution type and parameters are specified in the "name" box. Distribution-based reaction constants must be named as follows:: 

  type:mean:sd 

where type is a string describing the distribution to be used, mean is the distribution mean, and sd is the distribution standard deviation. The following strings are valid for the type attribute: gaussian (Gaussian distribution). For example, the name gaussian:0.3:0.1 indicates that the value of the reaction constant will be sampled from a Gaussian distribution with mean 0.3 and standard deviation 0.1. Negative reaction constant values are set to zero. 

Species specification
----------------------------------------------------------
Species can be named arbitrarily. To set the initial amount of molecules present for a species, in CellDesigner right click on the species and select "Edit Species...", where you will see a box where you can enter the initial amount. By default, initial amounts are only set for species in the template compartment, although you can set the duplicate_initial_amounts parameter in the parameter file to 1 to reproduce the initial amounts in all compartments which use this template. If you want the amount of a species to be constant then you can select the constant option in the "Edit Species..." dialogue in CellDesigner. The level of this species will then always stay at its initial amount, even if the species is involved in any reactions.

License
---------------------------------
The mcss distribution, including all source code, model examples, and documentation, are the copyright of Jamie Twycross, and released under the GNU GPL version 3 license. 

Credits
------------------------------------
mcss was written by Jamie Twycross, with contributions from Francisco Romero-Campero, Jonathan Blakes and James Smaldon. It is being used on Systems Biology research projects in the Centre for Plant Integrative Biology and the School of Computer Science, University of Nottingham, U.K. This work is funded by grants from the BBSRC grant BB/D0196131. 

For further information or any questions please contact jpt AT cpib.ac.uk. 

copyright 2008, 2009 Jamie Twycross, released under GNU GPL version 3. 