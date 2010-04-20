import os.path
from common.files import split_directories, path_join_overlapping

directory = 'infobiotics/dashboard/tests' 
file = 'dashboard/tests/models/module1.sbml'

d = split_directories(directory, isdir=True)
f = split_directories(file)
print path_join_overlapping([d, f])
file = os.path.basename(file)
print os.path.join(path_join_overlapping([d, f]), file)
print path_join_overlapping([split_directories(os.getcwd(), isdir=True), d, f, [file]])
print path_join_overlapping([d, f])
print path_join_overlapping([f])
