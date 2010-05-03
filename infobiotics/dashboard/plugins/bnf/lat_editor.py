from bnf_editor import BNFEditor


class LATEditor(BNFEditor):

#    key_bindings = Instance(KeyBindings) # The key bindings used by the editor
    wildcard = 'Lattice (*.lat)'
    untitled_prefix='lattice '
    text = '''lattice onePoint
    
    dimension 2
    xmin      0
    xmax      0
    ymin      0
    ymax      0

    basis
        (a,0)
        (0,a)
    endBasis

    vertices
        (a/2,a/2)
        (-a/2,a/2)
        (-a/2,-a/2)
        (a/2,-a/2)
    endVertices

    neighbours
        (1,0)
        (-1,0)
        (0,1)
        (0,-1)
    endNeighbours

endLattice
'''
