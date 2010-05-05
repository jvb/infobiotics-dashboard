from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    
    packages=find_packages(
        exclude=[
            "*.tests", "*.tests.*", "tests.*", "tests", # http://packages.python.org/distribute/setuptools.html#using-find-packages
            'expect',
            'thirdparty',
        ]
    ),

    scripts=[
        'bin/infobiotics-dashboard.py',
    ],

    install_requires=[
        'EnthoughtBase==3.0.4',
        'AppTools==3.3.1',
        'Traits==3.3.0',
        'EnvisageCore==3.1.2',
        'TraitsGUI==3.3.0',
        'EnvisagePlugins==3.1.2',
        'TraitsBackendQt==3.3.0',
#        'numpy>=1.2.1', # can't be easy_installed
        'Mayavi==3.3.1',
        'configobj==4.7.2',
        'tables==2.1.2',
        'which==1.1.0',
        'winpexpect==1.2',
        'pexpect==2.4',
#        'Matplotlib==0.99.1', # can't be easy_installed either
    ],

    name='InfobioticsDashboard',
    author='Jonathan Blakes',
    author_email='jvb@cs.nott.ac.uk',
    license='COPYING.txt',#LICENSE.txt',
    url='http://www.infobiotics.org/infobiotics-workbench/',
    description='Infobiotics Dashboard is a graphical front-end to the Infobiotics Workbench, a suite of tools for modelling and designing multi-cellular biological systems.',
    long_description=open('README.txt').read(),
    version=open('VERSION.txt').read(),
    keywords='biology, modelling, simulation',
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',          
    ],
)
