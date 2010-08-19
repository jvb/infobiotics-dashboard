from __future__ import with_statement
import subprocess, tempfile, os.path
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Str, List, Int
from enthought.traits.ui.api import View, Item, CodeEditor
from infobiotics.mcss.mcss_params import McssParams


cwd = os.path.join(os.getcwd(), '../examples/autoregulation')

class LPPEditor(HasTraits):
    content = Str
    error = Str
    error_lines = List(Int)

    view = View(
        Item('content', 
            show_label=False,
            editor=CodeEditor(
                squiggle_lines='error_lines',
            )
        ),
        width=640, height=480,
        resizable=True,
    )
    
    def _content_changed(self): #TODO in thread
        self.check_syntax()
        
    def check_syntax(self):
        ''' Runs mcss on content to check syntax. 
        
        Writes changed content to an temporary file for model_file.
        Writes a temporary params file for mcss that includes model_file and 
        data_file.
        Doing this in a Windows-compatible manner means closing all tempfiles.
        
        Runs mcss with params_file and max_time=0, returning 1 on a syntax error.
        
        '''
        m = tempfile.NamedTemporaryFile(dir=cwd, suffix='.lpp') 
        model_file = m.name
        m.close()
        assert not os.path.exists(model_file)
        
        # write model_file
        with open(model_file, 'w') as f:
            f.write(self.content)
        assert os.path.exists(model_file)
        
        d = tempfile.NamedTemporaryFile(dir=cwd, suffix='.h5')
        data_file = d.name
        d.close()
        assert not os.path.exists(data_file)
        
        p = tempfile.NamedTemporaryFile(dir=cwd, suffix='.params')
        params_file = p.name
        p.close()
        assert not os.path.exists(params_file)
        
        McssParams(
            directory=cwd, # overcomes directory preference 
            model_file=model_file, 
            data_file=data_file,
        ).save(params_file) # save file
        assert os.path.exists(params_file)
        #TODO assert params file is closed
        
        p = subprocess.Popen(
            ['mcss', params_file, 'max_time=0'],
            cwd=cwd,
            stderr=subprocess.PIPE,
        )

        returncode = p.wait()
        if returncode == 1:
            self.error = p.stderr.read()
        else:
            self.error = ''
        
        # remove temporary files
        for path in (model_file, data_file, params_file):
            if os.path.exists(path):
                os.remove(path)
            assert not os.path.exists(path)

    def _error_changed(self):
        if self.error != '':
            print 'ERROR', self.error
            error_line = int(self.error.split('line: ')[1])
            self.error_lines = [error_line]
        else:
            self.error_lines = []
        
if __name__ == '__main__':
    lpp = 'bacterialColonies.lpp'
    with open(os.path.join(cwd, lpp)) as f: #TODO universal newlines
        LPPEditor(
            content=f.read(),
        ).configure_traits()
