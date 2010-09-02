#!/bin/bash
file=simulation_results_dialog.ui
pyuic4 -x $file -o ui_simulation_results_dialog.py && echo "compiled $file ok"