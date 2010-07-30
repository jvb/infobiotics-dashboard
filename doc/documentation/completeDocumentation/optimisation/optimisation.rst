######################################
Structure/parameter Optimisation
######################################

=========
Aims 
=========

The POptimizer is developed for Optimizing both the structure and the parameters of system biological models automatically by using evolutionary algorithms. 

=================
Data to process 
=================

Currently the POptimizer can process two types of input data from the cell system biological data with single compartment: 

  1. the time series data of multiple target objects under one initial state 
  2. the time series data of multiple target objects under different initial states 

=================
Models to build 
=================

The models built by the POptimizer can have flexible model structure and parameters. The basic structure for each model takes the form of set of modules. Those elementary modules are instantiated or copied from the model library. The user can define their own non-fixed module library or fixed module library based on the field knowledge where the former means that all the modules in this library act as the building blocks to combine into various modules during the evolution which the latter means that all the modules in this library are attached into each model with fix structures and parameters. 

In addition the structure of each module in non-fixed module library can be partially fixed by fixing some rules and all the parameters within the module can be fixed or non-fixed by defining their specific range ( the parameter is fixed if the lower bound and the upper bound are the same otherwise non-fixed). The parameter can have the linear scale value or logarithmic scale value. 

============================================================================
Five parameter optimization methods based on evolutionary algorithms (EAs) 
============================================================================

The POptimizer can provide five alternative population-based evolutionary algorithms to do the parameter optimization. The five methods are: 
  1) DE (Differential Evolution) 
  2) ODE (Opposition-based DE) 
  3) GA (Genetic Algorithm) 
  4) EDA (Estimation of Distribution Algorithm) 
  5) CMA-ES (Covariance Matrix Adaptation - Evolution Strategy) 

Please see the file Parameter Optimization methods.doc to get more details. 

================================
Two fitness calculation method 
================================

The POptimizer can provide two alternative fitness calculation methods which are: 

  1) Random Weighted Sum 
  2) Equally Weighted Sum 

Please see the file Fitness Calculation methods.doc to get more details. 

