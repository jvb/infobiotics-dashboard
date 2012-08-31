from infobiotics.shared.traits_imports import *


class McssPlotOptions(HasTraits):
    pass


timeseries_options_view = View(
    VGroup(
        HGroup(
            Item('show_error_bars'),
            Label('every'),
            Item('error_bars_interval', show_label=False),
            Label('data points'),
            Spring(),
        ),
        HGroup(
            Item('show_confidence_interval'),
            Label('of'),
            Item('confidence_interval', editor=RangeEditor(mode='text'), show_label=False),
            Spring(),
        ),
    ),
    title='Timeseries options',
)


class TimeseriesOptions(McssPlotOptions):
    show_error_bars = Bool(False, desc='TODO')
    error_bars_interval = Int(10, desc='number of data points between error bars')
    show_confidence_interval = Bool(False, desc='TODO')
    confidence_interval = Range(0.0, 100.0, 1.0, desc='TODO')
    view = timeseries_options_view
    

class SurfaceOptions(McssPlotOptions):
    pass


class HistogramOptions(McssPlotOptions):
    pass


class ContinuousHistogramOptions(McssPlotOptions):
    pass



if __name__ == '__main__':
    TimeseriesOptions().configure_traits()
    