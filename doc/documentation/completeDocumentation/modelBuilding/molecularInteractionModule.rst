Molecular Interaction Modules
----------------------------------------------------------

A **molecular interaction module** consists of a set of rules representing a *general schema* that can be instantiated to produce specific molecular interactions. These rules may contain some *variables* for the name of the molecular species, stochastic constant values and comparment names so they can be reused intensively in our models by instantiating these variables with specific molecules, rates and compartments. 

A module is identified with a name, *moduleName* and three lists of variables for molecular species, *speciesVariables*, for stochastic constants, *constantVariables*, and for compartment names, *compartmentVariables*. The specification of a module enumerates the rules, *molecularInteractionRule*, with variables used to represent the schema of molecular interactions. In this respect, if the stochastic constant associated with a rule is a variable of the module the last part of a rule specification (const = value) is omitted. The definition of a module is specified as follows::

     moduleName(speciesVariables,constantVariables,comparmentVariables) =
          {
               molecularInteractionRule
               ...
               molecularInteractionRule
          }

The set of rules associated with a module can be specified using other modules. In this case it is necessary to specify the file containing the library of modules where the module definition is declared:: 

     moduleName(speciesVariables,constantVariables,comparmentVariables) =
          {
               moduleName_1(speciesVariables_1,constantVariables_1,comparmentVariables_1) from moduleLibraryFile
               ...
               moduleName_n(speciesVariables_n,constantVariables_n,comparmentVariables_n) from moduleLibraryFile
               molecularInteractionRule
               ...
               molecularInteractionRule
          }

This facilitates the hierarchical and incremental desing of complex modules and consequently, the parsimonious and modular specification of the molecular interactions associated with a *SP-system* model of a single cell. The modules used in the our *sender cell* are introduced below to illustrate the definition of modules::

   Pconst({X},{c_1},{l}) = 
   {
       r1: [ Pconst_geneX ]_l -c1-> [ Pconst_geneX + rnaX_RNAP ]_l
   }   
 

   PostTransc({X},{c_1,c_2,c_3,c_4,c_5},{l}) =
   {
       r1: [ rnaX_RNAP ]_l -c_1-> [ rnaX ]_l
       r2: [ rnaX ]_l -c_2-> [ rnaX + proteinX_Rib ]_l
       r3: [ rnaX ]_l -c_3-> [ ]_l
       r4: [ proteinX_Rib ]_l -c_4-> [ proteinX ]_l
       r5: [ proteinX ]_l -c_5-> [ ]_l
   }

