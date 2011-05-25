from params_relative_file import ParamsRelativeFile

ModelFile = ParamsRelativeFile(desc='the model to simulate',
    readable=True,
    filter=[
        'All model files (*.lpp *.sbml)',
        'Lattice population P system files (*.lpp)',
        'P system XML files (*.xml)',
        'Systems Biology Markup Language files (*.sbml)',
        'All files (*)'
    ],
    entries=10,
)
