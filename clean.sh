#!/bin/bash
find -name "*.pyc" -delete
rm -rf build/ dist/ debian/ tmp*/
rm infobiotics-dashboard*.deb infobiotics-dashboard*.dsc infobiotics-dashboard*.tar.gz infobiotics-dashboard*.tar.gz.cdbs-config_list
#rm distribute-*
#rm setup.cfg
#rm -rf InfobioticsDashboard.egg-info/
#rm PKG-INFO
