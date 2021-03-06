from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
from infobiotics.dashboard.pmodelchecker.editor import PModelCheckerResultsEditor

def edit_pmodelchecker_results_file(file, application=None):
    if application is not None:
        application.workbench.edit(
            obj=PModelCheckerResults(file_name=file),
            kind=PModelCheckerResultsEditor,
            use_existing=False,
        )
    else:
        PModelCheckerResults(file_name=file).edit()
        