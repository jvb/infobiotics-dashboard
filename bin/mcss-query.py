import tables

def species_names(*indices):
    return [name for index, name in root.species_information.cols[:] if index in indices]

def species_indices(*names):
    return [index for index, name in root.species_information.cols[:] if name in names]

def main(argv):
    file = argv[1]
    f = tables.openFile(file)
    global root
    root = f.root
    print species_names(0, 1)
    print species_indices('A', 'c')
    f.close()
    return 0
    
if __name__ == '__main__':
    import sys
    sys.argv.insert(1, '/home/jvb/dashboard/examples/modules/module1.h5')
    exit(main(sys.argv))
