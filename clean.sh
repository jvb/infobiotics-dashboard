#!/bin/bash

echo "removing .pyc files"
/usr/bin/find . -name "*.pyc" -delete

echo "removing build directories"
rm -rf build/ dist/ debian/ tmp*/ 
#2&>/dev/null

echo "removing debian packages"
rm infobiotics-dashboard*.deb infobiotics-dashboard*.dsc infobiotics-dashboard*.tar.gz infobiotics-dashboard*.tar.gz.cdbs-config_list 2&>/dev/null

echo "removing distribute eggs"
bash rm distribute-* 2&>/dev/null

echo "removing setup configuration"
rm setup.cfg 2&>/dev/null

echo "removing dashboard eggs"
rm -rf InfobioticsDashboard.egg-info/ 2&>/dev/null

echo "removing PKG-INFO"
rm PKG-INFO 2&>/dev/null

# used for comparing different builds
#rm duh duh_ 2&>/dev/null

