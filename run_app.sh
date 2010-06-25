#!/bin/bash
export DYLD_PRINT_LIBRARIES=1
dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard 2&> dist/DYLD_PRINT_LIBRARIES.txt
unset DYLD_PRINT_LIBRARIES
cat dist/DYLD_PRINT_LIBRARIES.txt | grep freetype
