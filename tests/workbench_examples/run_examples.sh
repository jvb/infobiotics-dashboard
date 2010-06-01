#!/bin/bash

mcss ./modules/module1.params && cat ./modules/module1.params | grep h5

mcss ./pulsePropagation/mcss_example/pulsePropagation.params
pmodelchecker ./pulsePropagation/pmodelchecker_example/pulse_MC2.params

mcss ./motifs/pulse/mcss_example/IFFL_Model.params
pmodelchceker ./motifs/pulse/pmodelchecker_example/IFFL_PRISM.params
pmodelchecker ./motifs/pulse/pmodelchecker_example/IFFL_MC2.params

mcss ./motifs/CONST/mcss_example/constitutiveExpressionModel.params
pmodelchecker ./motifs/CONST/pmodelchecker_example/Const_PRISM.params
pmodelchecker ./motifs/CONST/pmodelchecker_example/Const_MC2.params

mcss ./motifs/PAR/mcss_example/positiveAutoregulation.params
pmodelchecker ./motifs/PAR/pmodelchecker_example/PAR_PRISM.params
pmodelchecker ./motifs/PAR/pmodelchecker_example/PAR_MC2.params

mcss ./motifs/NAR/mcss_example/negativeAutoregulation.params
pmodelchecker ./motifs/NAR/pmodelchecker_example/NAR_MC2.params
pmodelchecker ./motifs/NAR/pmodelchecker_example/NAR_PRISM.params

