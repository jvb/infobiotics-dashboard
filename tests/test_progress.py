import unittest2 as unittest


class TestProgress(unittest.TestCase):

    def test_mcss(self):
        from infobiotics.api import mcss as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/simulation.params')
        e.perform()
        
    def test_mcss_gui(self):
        from infobiotics.api import mcss as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/simulation.params')
        e._interaction_mode = 'gui'
        e.perform()

    
    def test_prism(self):
        from infobiotics.api import prism as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_prism.params')
        e.perform()
        
    def test_prism_gui(self):
        from infobiotics.api import prism as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_prism.params')
        e._interaction_mode = 'gui'
        e.perform()

    
    def test_mc2(self):
        from infobiotics.api import mc2 as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_mc2.params')
        e.perform()
        
    def test_mc2_gui(self):
        from infobiotics.api import mc2 as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_mc2.params')
        e._interaction_mode = 'gui'
        e.perform()

    
    def test_poptimizer(self):
        from infobiotics.api import poptimizer as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/optimisation.params')
        e.perform()
        
    def test_poptimizer_gui(self):
        from infobiotics.api import poptimizer as experiment
        e = experiment('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/optimisation.params')
        e._interaction_mode = 'gui'
        e.perform()
    


if __name__ == "__main__":
    unittest.main()
