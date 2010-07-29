############################################
Model Formal Analysis using Model Checking
############################################

.. *******************************
.. Model Analysis using PRISM
.. ******************************* 


.. *******************************
.. Model Analysis using MC2
.. ******************************* 



===============
Introduction
===============

*pmodelchecker* is an application that facilitates the use of formal model analysis using *Model Checking* of spatio-temporal properties of P system models developed within the  *Infobiotics workbench*. *pmodelchecker* receives as input a model developed as specified in section and a list of temporal logic formulas formalising some spatio-temporal properties to be  checked against the dynamics of the model. 

*pmodelchecker* uses two different stochastic model checkers, PRISM and MC2. When using PRISM it generates a model in the *reactive modules language* needed in PRISM in order to check the input logic formulas. When using MC2 it generates the needed simulation samples by running *mcss*, the multicomparmental simulator introduced in the previous section. 
   
===============
Installlation
=============== 

For instructions on how to compile and install *pmodelchecker*, see the README file included with the *pmodelchecker* distribution.

=======================
Running pmodelchecker
=======================

In order to run *pmodelchecker* after its installation run the following command::

$ pmodelchecker PARAMETER_FILE

where *PARAMETER_FILE* is an xml file declaring the input parameters required to perform model checking using one of the two stochastic model checkers integrated in Infobiotics, PRISM or MC2. For example, in order to run the examples in the directory *PRISMexamples/* browse to this directory provided in the directory *examples/* of the *pmodelchecker* distribution and type one of the commands below depending on which example you want to run::

   $ pmodelchecker NAR1.params

   $ pmodelchecker NAR2.params

In a similar manner to run the examples for MC2 browse to the directory *MC2examples/* inside the directory *examples/* provided in the *pmodelchecker* distribution and type the command below::

   $ pmodelchecker NAR_MC2.params

The output, probabilities or expected values for temporal logic formulas, is produced into the result file specified as in the parameter file as explained below. 

=============================
pmodelchecker parameter files
=============================

The *pmodelchecker* parameter file provides information to determine which specific model checker to use, PRISM or MC2, and some parameters to control the application of these model checkers like the use of verification versus approximation or the number of samples to consider in the case of a simulative or approximative approach.

The parameter file is in an XML format which has the general form::

  <parameters>
    <parameterSet name="SimulationParameters">
      <parameter name="PARAMETER NAME" value="PARAMETER VALUE"/>
      <parameter name="PARAMETER NAME" value="PARAMETER VALUE"/>
      ...
    </parameterSet>
  </parameters> 

The specific parameters are given in the table below:


+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  PARAMETER NAME                  | DESCRIPTION                             | VALUE          | RESTRICTIONS                      |
+==================================+=========================================+================+===================================+
|  **model_specification**         | Name of the file containing the model   | String         |  None                             |
|                                  | specification as an LPP-system          |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **temporal_formulas**           | Name of the file containing the         | String         |  None                             |
|                                  | temporal logic formulas formalising the |                |                                   |
|                                  | properties to check                     |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **model-checker**               | Name of the model checker to use        | String         |  None                             |
|                                  | PRISM or MC2                            |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **PRISM_model**                 | Name of the file where to output the    | String         |  Only when using                  |
|                                  | translation of our model into the PRISM |                |  PRISM                            |
|                                  | language                                |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **task**                        | Task to perform when using PRISM as     |  Translate/    |  Only when using                  |
|                                  | model checker. Translate LPP-system     |  Build/        |  PRISM                            |
|                                  | into the PRISM languge, build the       |  Verify/       |                                   |
|                                  | corresponding Markov chain, verify or   |  Approximate   |                                   |
|                                  | approximate the input properties        |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **model_parameters**            | A string stating the values of the      |  String        | Only when using                   |
|                                  | parameters in the model as follows      |                | PRISM                             |
|                                  | param=lb:ub:s,param=lb:ub:s, ... where  |                |                                   |
|                                  | lb is the lowe bound, up is the upper   |                |                                   |
|                                  | bound and s is the step                 |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **formula_parameters**          | A string stating the values of the      |  String        | Only when using                   |
|                                  | parameters in the formulas as follows   |                | PRISM                             |
|                                  | param=lb:ub:s,param=lb:ub:s, ... where  |                |                                   |
|                                  | lb is the lowe bound, up is the upper   |                |                                   |
|                                  | bound and s is the step                 |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **states_file**                 | Name of the file where to output the    |  String        | Only when using                   |
|                                  | states of the Markov chain generated    |                | PRISM with task                   |
|                                  | from the LPP-system                     |                | Build or Verify                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **transitions_file**            | Name of the file where to output the    |  String        | Only when using                   |
|                                  | transitions of the Markov chain         |                | PRISM with task                   |
|                                  | generated from the LPP-system           |                | Build or Verify                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **number_samples**              | Number of simulations to generate when  |  Integer       | Only when using                   |
|                                  | taking an approximate or simulative     |                | PRISM with task                   |
|                                  | approach to model checking              |                | Approximate or                    |
|                                  |                                         |                | whenever using                    |
|                                  |                                         |                | MC2                               |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **precision**                   | Precision to achieve whith respect to   |  Double        | Only when using                   |
|                                  | real value when generating an estimate  |                | PRISM with task                   |
|                                  | using approximate or simulative model   |                | Approximate                       |
|                                  | checking                                |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **confidence**                  | Confidence to achieve whith respect to  |  Double        | Only when using                   |
|                                  | real value when generating an estimate  |                | PRISM with task                   |
|                                  | using approximate or simulative model   |                | Approximate                       |
|                                  | checking                                |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **pathMC2**                     | Location of the executable file for MC2 |  String        | Only when using                   |
|                                  |                                         |                | MC2                               |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **simulations_generatedHDF5**   | Flag to determine if the simulations    |  true/false    | Only when using                   |
|                                  | needed to run MC2 are available in      |                | MC2                               |
|                                  | HDF5 format                             |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **simulations_generatedMC2**    | Flag to determine if the simulations    |  true/false    | Only when using                   |
|                                  | needed to run MC2 are available in      |                | MC2                               |
|                                  | MC2 format                              |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **simulations_file_hdf5**       | Name of the file containing the         |  String        | Only when using                   |
|                                  | simulations in HDF5 format or where to  |                | MC2 and the flag                  |
|                                  | write them when using mcss              |                | simulations_generatedMC2 = false  |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **simulations_file_MC2**        | Name of the file containing the         |  String        | Only when using                   |
|                                  | simulations in MC2 format or where to   |                | MC2                               |
|                                  | write them                              |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **mcss_params_file**            | Name of the file containing the         |  String        | Only when using MC2 and the flag  |
|                                  | parameters to run mcss in order to      |                | simulations_generatedHDF5 = false |
|                                  | generate the necessary simulations      |                | and simulations_generatedMC=false |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+
|  **results_file**                | Name of the file where to write the     |  String        | None                              |
|                                  | answers to the temporal logic formulas  |                |                                   |
|                                  | generated by the model checker          |                |                                   |
+----------------------------------+-----------------------------------------+----------------+-----------------------------------+


.. =====================================
.. Temporal logic formulas specification
.. =====================================




License
------------------------------------------

The *pmodelchecker* distribution, including all source code, model examples, and documentation, are the copyright of of the Infobiotics Team (Hongqing Cao, Claudio Lima, Natalio Krasnogor, Francisco Romero-Campero, Jamie Twycross, and Jonathan Blakes) and is released under the GNU GPL version 3 license.

Credits
-------------------------------------------

*pmodelchecker* was written by Francisco J. Romero-Campero and is being used on Systems/Synthetic Biology research projects in the University of Nottingham, U.K. 

For further information or any questions please contact fxc AT cs.nott.ac.uk.

*copyright 2009 Infobiotics Team, released under GNU GPL version 3.*



 
