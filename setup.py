'''
Setup script for Infobiotics Dashboard.

Install:                         python setup.py install
Build source package (.tar.gz):  python setup.py sdist
Build binary package (.egg):     python setup.py bdist_egg

distutils:                  http://docs.python.org/distutils/introduction.html
setuptools (easy_install):  http://peak.telecommunity.com/DevCenter/setuptools
pip:                        http://pypi.python.org/pypi/pip/
virtualenv:                 http://pypi.python.org/pypi/virtualenv
virtualenvwrapper:          http://www.doughellmann.com/docs/virtualenvwrapper/
eggs:                       http://mrtopf.de/blog/python_zope/a-small-introduction-to-python-eggs/
'''

#from ez_setup import use_setuptools
#use_setuptools()

from setuptools import setup, find_packages

setup(

    # packages (any folder with an __init__.py)
#    packages=[
#        'infobiotics',
#    ],
    packages=find_packages(
        exclude=[
#            'ez_setup', 
#            'examples', 
            'tests', 
        ],
    ),
    
    # single modules that are not in packages
    py_modules=[
        'setup',
        'ez_setup',
    ], 

#    data_files=[
#        ('/home/jvb/bin',['bin/dashboard']),
#    ],
#    # other files (not Python modules)
#    package_data={'': ['*.*']}, #TODO logos    
#    package_data={'infobiotics': ['*.*']}, #TODO logos    
#    package_data={'mypackage': ['data/*.xml']},
#    include_package_data=True,
    
    package_data={'dashboard':['images/*.png']},
    
    # dependencies via easy_install
    install_requires=[
        'setuptools',
        'numpy',
        'tables',
        'matplotlib',
        'EnthoughtBase',
        'Traits',
        'TraitsGUI',
        'TraitsBackendQt',
        'Mayavi',
        'EnvisageCore',
        'EnvisagePlugins',
        'AppTools',
    ],
    #FIXME cannot require PyQt (Qt, Python), VTK, HDF5
    # or mcss, pmodelchecker, poptimizer 

    name='infobiotics-dashboard',
#    version=open('VERSION','r').read(),
    version='0.1a3',
    author='Jonathan Blakes',
    author_email='jvb@cs.nott.ac.uk',
    url='http://www.infobiotics.org/workbench/dashboard', #TODO
#    download_url='http://www.infobiotics.org/workbench/dashboard' #TODO
    license='GNU GPL V3',

#    description='Short description.', #TODO
#    long_description='''\
#Long description in reSTructured text format.
#    ''', #TODO

#    keywords='keyword1, keyword2', #TODO
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
    
#    zip_safe=True, # ?

#    # console anf gui scripts that need to be called 
#    entry_points='''
#    # -*- Entry points: -*-
#    ''',

)
