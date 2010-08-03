#!/bin/bash
rm DYLD_PRINT_LIBRARIES.txt
export DYLD_PRINT_LIBRARIES=1
dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard 2&> DYLD_PRINT_LIBRARIES.txt
unset DYLD_PRINT_LIBRARIES
cat DYLD_PRINT_LIBRARIES.txt | grep -C1 "loaded: /Library"
