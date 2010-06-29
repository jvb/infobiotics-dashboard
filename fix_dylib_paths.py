''' expects ldd.txt as input and outputs ldd_changes.sh and cp_libs.sh  '''

# 1. change @rpath to @executable_path/../Frameworks
paths = {}
for line in open('ldd.txt'):
    if line.startswith('dist'):
        lib = line.strip(':\n')
        paths[lib] = []
    else:
        old_path = line.strip().split()[0]
        if old_path.startswith('@rpath'):
            new_path = old_path.replace('@rpath', '@executable_path/../Frameworks')
            paths[lib].append((old_path, new_path))
output_file = open('ldd_changes.sh', 'w')
output_file.write('#!/bin/bash\n')
#chmod +x ldd_changes.txt
#./ldd_changes.sh
for lib, list_of_paths_to_change in paths.iteritems():
#    if lib.endswith('.dylib'):
#        print 'install_name_tool -id ""
    for old_path, new_path in list_of_paths_to_change:
        output_file.write('install_name_tool -change "%s" "%s" "%s"\n' % (old_path, new_path, lib)) 
output_file.close()

# 2. copy missing libs to Frameworks
output_file = open('cp_libs.sh', 'w')
output_file.write('#!/bin/bash\n')
#chmod +x ldd_changes.txt
#./ldd_changes.sh
import os.path
path_set = set()
for lib, list_of_paths_to_change in paths.iteritems():
    for old_path, new_path in list_of_paths_to_change:
        path = new_path.replace('@executable_path/../Frameworks', 'dist/InfobioticsDashboard.app/Contents/Frameworks')
        if not os.path.exists(path):
            path_set.add(path)
for path in path_set:
    output_file.write('cp %s dist/InfobioticsDashboard.app/Contents/Frameworks\n' % path.replace('dist/InfobioticsDashboard.app/Contents/Frameworks', '/Library/Frameworks/Python.framework/Versions/6.1/lib'))
output_file.close()
            
# repeat 1?

