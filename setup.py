# download and install Distribute use setuptools on bootstrap script
from distribute_setup import use_setuptools
use_setuptools()

# use Distribute setup function
from distutils.core import setup

setup(
    name='InfobioticsDashboard',
    version=open('VERSION.txt').read(),
    packages=['infobiotics',],
    license='GNU GPL v3',
    long_description=open('README.txt').read(),
)
