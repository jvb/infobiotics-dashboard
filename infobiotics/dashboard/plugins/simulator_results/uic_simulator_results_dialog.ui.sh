#!/bin/bash
file=simulation_results_dialog.ui
echo "executing 'pyuic4 -x $file -o ui_simulation_results_dialog.py'"
pyuic4 -x $file -o ui_simulation_results_dialog.py && echo "compiled $file ok" || echo "compiling $file failed"
echo "execute 'pyrcc4 -o icons_rc.py icons.qrc' to regenerate icons"
