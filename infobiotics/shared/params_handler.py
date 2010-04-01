from infobiotics.shared.api import \
    Controller, Property, Str, property_depends_on 
from params import Params

class ParamsHandler(Controller):

    title = Property(Str)

    @property_depends_on('model._params_file')
    def _get_title(self):
        path = self.model._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            if dirname == '':
                return basename
            else:
                return '%s (%s)' % (basename, dirname)
        else:
            return self.model._parameters_name
            
    def init(self, info):
        info.ui.title = self.title 
    
    def traits_view(self):
        raise NotImplementedError
    
    def load(self, info): 
        file=None
        pass
        info.object.load(file)
    
    def save(self, info):
        file=None
        pass
        info.object.save(file)
