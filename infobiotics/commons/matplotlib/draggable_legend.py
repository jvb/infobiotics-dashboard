'''
Draggable legend for matplotlib figures from http://stackoverflow.com/q/2539477

Apparently included in upstream version of matplotlib, not in ETS yet though
(20100923). Usage then would be:

    leg = ax.legend() leg.draggable()

'''

class DraggableLegend:
    ''' Usage:
    
        def draw(self): 
            ax = self.figure.add_subplot(111)
            scatter = ax.scatter(np.random.randn(100), np.random.randn(100))

        legend = DraggableLegend(ax.legend())
    
    '''
    def __init__(self, legend):
        self.legend = legend
        self.gotLegend = False
        legend.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        legend.figure.canvas.mpl_connect('pick_event', self.on_pick)
        legend.figure.canvas.mpl_connect('button_release_event', self.on_release)
        legend.set_picker(self.my_legend_picker)

    def on_motion(self, evt):
        if self.gotLegend:
            dx = evt.x - self.mouse_x
            dy = evt.y - self.mouse_y
            loc_in_canvas = self.legend_x + dx, self.legend_y + dy
            loc_in_norm_axes = self.legend.parent.transAxes.inverted().transform_point(loc_in_canvas)
            self.legend._loc = tuple(loc_in_norm_axes)
            self.legend.figure.canvas.draw()

    def my_legend_picker(self, legend, evt): 
        return self.legend.legendPatch.contains(evt)   

    def on_pick(self, evt): 
        if evt.artist == self.legend:
            bbox = self.legend.get_window_extent()
            self.mouse_x = evt.mouseevent.x
            self.mouse_y = evt.mouseevent.y
            self.legend_x = bbox.xmin
            self.legend_y = bbox.ymin 
            self.gotLegend = 1

    def on_release(self, event):
        if self.gotLegend:
            self.gotLegend = False
