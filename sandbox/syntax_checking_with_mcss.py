from __future__ import with_statement
import os.path, tempfile, subprocess, time, sys
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Str, List, Int
from enthought.traits.ui.api import View, Item
from infobiotics.mcss.mcss_params import McssParams
from infobiotics.language.lpp_editor import LPPEditor as CodeEditor

cwd = os.path.join(os.getcwd(), '../examples/autoregulation')
#cwd = os.path.join(os.getcwd(), '../examples/QS2')

class LPPEditor(HasTraits):
    content = Str
    error = Str
    error_lines = List(Int)
    help_lines = List(Int)
    line = Int
    help = Str
    obj = Str
    model_file = Str

    def _obj_changed(self, obj):
        self.model_file = obj
        with open(os.path.join(cwd, obj)) as f:
            self.content = f.read()

    view = View(
        Item('content',
            show_label=False,
            editor=CodeEditor(
                squiggle_lines='error_lines',
                mark_lines='help_lines',
                line='line',
                foldable=True,
            )
        ),
        Item('help', show_label=False),
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
        self.model_file = m.name
        m.close()
        assert not os.path.exists(self.model_file)

        # write model_file
        with open(self.model_file, 'w') as f:
            f.write(self.content)
        assert os.path.exists(self.model_file)

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
            model_file=self.model_file,
            data_file=data_file,
        ).save(params_file) # save file
        assert os.path.exists(params_file)
        #TODO assert params file is closed

        p = subprocess.Popen(
            ['mcss', params_file, 'max_time=0'],
            cwd=cwd,
            universal_newlines=True,
            stdout=subprocess.PIPE, # for alphabet errors
            stdin=subprocess.PIPE, # for responding to alphabet errors 
            stderr=subprocess.PIPE, # for syntax errors
        )

        returncode = None
        while returncode is None:
            try:
                out, err = p.communicate('y\n') # change the alphabet
                self.error = err
                if out.startswith('Warning missing objects in the alphabet from P system '):
                    system = out.split('\n')[0].split('system ')[1]
                    suggested_alphabet = [line.strip() for line in out.split('alphabet')[2].split('endAlphabet')[0].split('\n') if line.strip() != '']
#                    print system, suggested_alphabet #TODO
            except OSError:
                pass
            except ValueError:
                pass
            time.sleep(0.001)
            returncode = p.poll()

        # remove temporary files
        for path in (self.model_file, data_file, params_file):
            if os.path.exists(path):
                os.remove(path)
            assert not os.path.exists(path)

    def _error_changed(self, error):
        if error != '':
            if 'according to BNF failed in line: ' in error:
                #Parsing of file Bacteria.sps according to BNF failed in line: 46
                file = error.split('Parsing of file ')[1].split(' according')[0]
                line = int(error.split('according to BNF failed in line: ')[1])
                if file == self.model_file:
                    self.error_lines = [line]
                else:
                    self.help_lines = lines(file, self.content)
                    self.help = error

            elif 'Unable to open file: ' in error:
                file = error.split('file: ')[1].strip()
                self.error_lines = lines(file, self.content)
                self.help = "Unable to open '%s'" % file

            elif 'Error: unknown file extension in file: ' in error:
                file = error.split('in file: ')[1].split()[0].strip()
                self.error_lines = lines(file, self.content)
                self.help = "Unknown extension for '%s' ('.sps' or '.sbml' known)" % file

            elif 'Error: P system ' in error:
                system = error.split('Error: P system ')[1].split(' not defined')[0]
                self.error_lines = lines(system, self.content)
                self.help = "'%s' not defined."

            elif "terminate called after throwing an instance of 'mu::ParserError'" in error:
                self.error_lines = [self.line + 1]
                self.help = "Error parsing coordinate parameters."

            elif 'Position (' in error:
                self.error_lines = [self.line + 1]
                self.help = self.error.strip()

            else:
                sys.stderr.write(error)
        else:
            self.error_lines = []
            self.help_lines = []
            self.help = ''

def lines(sub, string):
    return [i + 1 for i, line in enumerate(string.split('\n')) if sub in line]


if __name__ == '__main__':
    LPPEditor(
        obj='bacterialColonies.lpp',
    ).configure_traits()
