#!/bin/sh

# run as root

# add repositories
cat > /etc/apt/sources.list.d/infobiotics-workbench.list <<HERE
# This file lists the repositories for the Infobiotics Workbench.
#
# These repositories should work with most recent Debian/Ubuntu-based Linux
# distributions.
#
# If you have any problems with these repositories, you can let us know at 
# Jonathan.Blakes@nottingham.ac.uk

# Infobiotics
deb http://www.infobiotics.org/infobiotics-apt stable contrib
deb-src http://www.infobiotics.org/infobiotics-apt stable contrib

# Traits 3, Mayavi2 3
#deb http://archive.ubuntu.com/ubuntu natty main universe
#deb-src http://archive.ubuntu.com/ubuntu natty main universe
#deb http://archive.ubuntu.com/ubuntu natty-updates main universe
#deb-src http://archive.ubuntu.com/ubuntu natty-updates main universe
HERE

apt-get update

# install from Ubuntu 12.04 Precise repositories
#apt-get install python-qt4 python-qt4-gl python-qscintilla2 default-jre

# install from Ubuntu 11.04 Natty repositories
#apt-get install -t natty infobiotics-workbench

