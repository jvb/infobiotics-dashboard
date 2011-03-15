from infobiotics.shared.traits_imports import * 
from infobiotics.dashboard.plugins.mcss_results.mcss_results_groups import * 
from infobiotics.dashboard.plugins.mcss_results.mcss_results_actions import *


mcss_results_view = View(
    VGroup(
        data_group,
        timepoints_group,
        data_options_group,
        plot_type_group,
        plot_options_group,
        show_border=True,
    ),
    buttons=['OK', show_script_action, save_data_action, plot_action],
    resizable = True,
    title = 'mcss results'
)
