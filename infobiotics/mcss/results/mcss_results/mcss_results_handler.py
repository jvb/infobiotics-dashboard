from infobiotics.shared.traits_imports import * 


class McssResultsHandler(Handler):
    
    repr = Str

    script_view = View(
        Item('repr', show_label=False, style='custom'),
        resizable=True,
        title='mcss results script',
    )  
    
    def show_script(self, info):
        self.repr = info.object.__repr__()
        self.edit_traits(view=self.script_view, handler=self, kind='nonmodal')


    def plot(self, info):
        info.object.plot()


    def save_data(self, info):
        info.object.save_data()
