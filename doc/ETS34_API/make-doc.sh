easy_install virtualenv
easy_install virtualenvwrapper
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper_bashrc" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv ETS_trunk
workon ETS_trunk
easy_install ETSProjectTools
ets co ets
#mv `ls | grep ETS` ETS_trunk
name_and_version=`ls | grep ETS`
cd $name_and_version
mv -r ETS/* .
ets develop
pip install docutils
mkdir enthought
cp -r */enthought/* ./enthought/
endo --include-protected --rst -r enthought/
cd doc
google-chrome enthought.html
#rm -r enthought