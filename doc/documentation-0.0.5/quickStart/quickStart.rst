###################################
Quick Start 
###################################

To get started with using the Infobiotics Workbench we will walk through simulating an example model based on negative autoregulation (NAR) of gene with our stochastic simulator. Alternatively you can follow our `video tutorial <http://www.infobiotics.org/infobiotics-workbench/various/quick_start_video.mpeg>`_.

1. First you need to download and install *Infobiotics Workbench* from `here <http://www.infobiotics.org/infobiotics-workbench/download/download.html>`_. 

2. Download `this <http://www.infobiotics.org/infobiotics-workbench/various/NAR.zip>`_ archive file containing the `NAR model example and unzip it to your favourite location. 

3. Open the **Infobiotics Workbench** by double clicking on **Infobiotics Dashboard** icon located on your desktop or in the Applications menu. The following window will appear showing the different experiments available: *simulation*, *model checking* (PRISM and MC2) and *optimisation* - without the open model files shown. 

.. figure:: dashboard.png
   :scale: 100
   :alt: Specifying simulation parameters.
   :align: center

4. Clicking on the **Simulation** button on the toolbar opens up the dialog window below allowing you to specify your simulation parameters.

.. figure:: simulation_tab.png
   :scale: 100
   :alt: alternate text
   :align: center

5. Load the simulation parameter file **simulation.params** by selecting **Load** from the dialog toolbar and navigating to the location of the *NAR model*. 

6. Run your simulations by clicking on the **Perform** button at the bottom of the simulation dialog window.  

7. Once your simulations have finished the following tab will appear to allow you to plot the results.

.. figure:: plots_tab.png
   :scale: 100
   :alt: alternate text
   :align: center

8. Plot the average number of molecules over time for all species in all compartments by checking **All** under *Runs*, *Species* and *Compartments*, then clicking on the **first** button ('timeseries') in the bottom right corner.

9. A preview window will appear that allows you to combine the various timeseries in different ways. Select all the graphs (Ctrl-A) and click the **Stack** button to view each timeseries with the same time axis but individual molecules axes. 

.. figure:: preview_plots.png
   :scale: 100
   :alt: alternate text
   :align: center

10. The following window containing the graphs will appear. You can save this graph in any size you like by clicking on the *save resized* button in the bottom left corner.
   
.. figure:: molecule_plots.png
   :scale: 100
   :alt: alternate text
   :align: center

The **Infobiotics Workbench** is not limited to performing simulations, you can apply other techniques to analyse and manipulate your models. Visit the links below if you are interested in the different components of our workbench. 

.. toctree::
   :maxdepth: 1

   modelProperties
   optimization

For more details on how to use the **Infobiotics Workbench** you can read the `tutorials `tutorial <http://www.infobiotics.org/infobiotics-workbench/tutorial/tutorial.html>`_. 

