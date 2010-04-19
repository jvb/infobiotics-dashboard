from infobiotics.shared.api import \
    Controller, Property, Str, property_depends_on, FileDialog, OK, os, \
    Bool, Property, property_depends_on, can_access, DelegatesTo

class ParamsHandler(Controller):

    title = Property(Str, depends_on='model._params_file, model._cwd')

    def _get_title(self):
        path = self.model._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            dirname = os.path.relpath(dirname, self.model._cwd)
            if dirname == '':
                return basename
            else:
                return '%s (%s)' % (basename, dirname)
        else:
            return self.model._parameters_name

    def _title_changed(self, title):
        if self.info is not None and self.info.initialized:
            self.info.ui.title = title
            
    def init(self, info):
        info.ui.title = self.title 
    
    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        fd = FileDialog(
            wildcard=self.wildcard, 
            title='Load %s parameters' % self.model._parameters_name,
            default_directory = os.path.dirname(self.model._params_file),
        )
        if fd.open() == OK:
#            self.model.load(fd.path)
            info.object.load(fd.path)

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        fd = FileDialog(
            action='save as', 
            wildcard=self.wildcard,
            title='Save %s parameters' % self.model._parameters_name,
            default_directory = os.path.dirname(self.model._params_file),
        )
        if fd.open() == OK:
#            self.model.save(fd.path)
            info.object.save(fd.path)
            
    wildcard = Str(desc='an appropriate wildcard string for a WX or Qt open and save dialog looking for params files.')
        
    def _wildcard_default(self):
        wildcards = [
            ('Experiment parameters', ['*.params']), 
            ('All files', ['*']),
        ] 
        try:
            import os
            toolkit = os.environ['ETS_TOOLKIT']
        except KeyError:
            toolkit = 'wx'
        wildcard = ''
        if toolkit == 'qt4':
            for i, w in enumerate(wildcards):
                # qt4: 'py and test (*.py *.test)||\ntest (*.test)||\npy (*.py)'
                wildcard += '%s (%s)' % (w[0], ' '.join(w[1])) 
                if i < len(wildcards) - 1:
                    wildcard += '||'#\n'
        else: # assume os.environ['ETS_TOOLKIT'] == ('wx' and not 'null')
            for i, w in enumerate(wildcards):
                # wx: 'py and test (*.py *.test)|*.py;*.test|\ntest (*.test)|*.test|\npy (*.py)|*.py'#|
                w2 = ';'.join(w[1])
                wildcard += '%s (%s)|%s' % (w[0], w2, w2)
                if i < len(wildcards) - 1:
                    wildcard += '|'#\n'
        return wildcard
    
    
if __name__ == '__main__':
    execfile('params.py')
    