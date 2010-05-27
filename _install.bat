#!/bin/bash
echo "Installing to local Python distribution."
echo "Please see README.txt for system-specific installation instructions."
easy_install pip
REM pip install --upgrade numpy
REM pip install --upgrade http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz/download
pip install .
