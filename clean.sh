#!/bin/bash

# remove PKG_INFO, setup.cfg, .pyc and .class files; build, debian, dist and tmp directories; Debian packages; distribute and InfobioticsDashboard eggs  


# individual files

echo "removing PKG-INFO"
rm PKG-INFO 2&>/dev/null

echo "removing setup configuration"
rm setup.cfg 2&>/dev/null


# sets of files

echo "removing .pyc files"
find . -name "*.pyc" -delete

echo "removing .class files"
find . -name "*.class" -delete


# directories

echo "removing build directories"
rm -rf build/ dist/ debian/ tmp*/ 2&>/dev/null


# Debian packages

echo "removing Debian packages"
rm infobiotics-dashboard*.deb infobiotics-dashboard*.dsc infobiotics-dashboard*.tar.gz infobiotics-dashboard*.tar.gz.cdbs-config_list 2&>/dev/null


# distribute and InfobioticsDashboard eggs

echo "removing distribute eggs"
rm distribute-* 2&>/dev/null

echo "removing dashboard eggs"
rm -rf InfobioticsDashboard.egg-info/ 2&>/dev/null


