from infobiotics.commons.traits_.api import RelativeFile

class ParamsRelativeFile(RelativeFile):
    ''' Extends RelativeFile to provide default traits values for Params
    subclasses particularly "directory_name='directory'" and 'auto_set=True'. '''
    
    def __init__(self,
        value='',
        filter=[],
        auto_set=True,
        entries=5,
        exists=False,
        exists_name='',
        directory='',
        directory_name='directory',
        absolute=False,
        readable=None,
        writable=None,
        executable=None,
        **metadata
    ):
        super(ParamsRelativeFile, self).__init__(
            value,
            filter,
            auto_set=auto_set,
            entries=entries,
            exists=exists,
            exists_name=exists_name,
            directory=directory,
            directory_name=directory_name,
            absolute=absolute,
            readable=readable,
            writable=writable,
            executable=executable,
            **metadata
        )
