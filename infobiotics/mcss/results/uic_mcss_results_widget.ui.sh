#!/bin/bash
file=simulation_results_dialog.ui
echo "executing 'pyuic4 -x -d $file -o ui_simulation_results_dialog.py'"
pyuic4 -x -d $file -o ui_mcss_results_widget.py && echo "compiled $file ok" || echo "compiling $file failed"
echo "execute 'pyrcc4 -o icons_rc.py icons.qrc' to regenerate icons"
