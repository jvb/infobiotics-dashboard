===========
 poptimizer
===========

------------------------------------------------------
structural and parameter optimizer for P system models
------------------------------------------------------

:Author: Hongqing Cao and Claudio Lima
:Date:   2010-02-06
:Copyright: Infobiotics
:Version: 0.1
:Manual section: 1

.. TODO: authors and author with name <email>

SYNOPSIS
========

  poptimizer PARAMETERFILE 

DESCRIPTION
===========

poptimizer is an application for optimizing the structure and parameters of stochastic P system models using evolutionary algorithms. poptimizer takes a library of modules that represent basic biological processes of interest and combines them in many different ways to discover a possible assembly that mimics the behavior of the target data. During the search process, each model is evaluated by simulating its behavior with the multicompartmental stochastic simulator mcss. poptimizer is being used to develop Systems and Synthetic Biology computational models of bacterial colonies and plant systems.

.. OPTIONS
.. =======

SEE ALSO
========

* mcss
* pmodelchecker
