set ETS_TOOLKIT=qt4
python setup.py py2exe
7z x -odist\enthought\tvtk\tvtk_classes C:\Python26\Lib\site-packages\enthought\tvtk\tvtk_classes.zip
dist\infobiotics-dashboard.exe
type dist\infobiotics-dashboard.exe.log
type dist\pexpect_error.log