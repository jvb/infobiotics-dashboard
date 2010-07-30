############################################
Model Specification using SBML
############################################

Genes are a good example of biological switches. A cell can contain hundreds of thousands of genes, each of which can be switched on or off in response to internal or external signals. One important aspect of genetic switches (and switches in general) is how quickly they can be switched on. This is known as the response time of the gene. This tutorial examines the response times of three models of gene regulation, all representing mechanisms found in biological cells. You will learn how to implement these three models and perform stochastic simulations in order to quantify their response times.


A simple model of gene regulation
###################################### 

We first look at the simple model of gene regulation pictured below.

	.. figure:: figures/simple_regulation_02.ss.png
	   :scale: 70
	   :alt: alternate text
	   :align: center

In this model a gene *G* (yellow box) produces proteins *P* (green box), which are also degraded. The expression of gene *G* can be repressed by the negative transcription factor *R* (green box), which binds with *G* to form a complex *R.G* (grey box containing *R* and *G* boxes). This prevents the gene *G* from producing proteins. The action of the negative transcription factor *R* can itself be inhibited by a protein *I* (green box), which binds to *R*, forming a complex *R.I* (grey box containing *R* and *I* boxes) and so prevents *R* binding to the gene *G*.

This model can be summarised by the P system reaction scheme:

	.. figure:: figures/reactions1.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

For each reaction, a stochastic reaction constant *k* is given. This reaction constant represents the average probability that a reaction will occur in an infinitesimal time interval. Since we are dealing with only one compartment, we don't explicitly define the compartment.

We will perform a stochastic simulation of this model of genetic decision making and analyse its behaviour. In order to do this we need to parameterise the model i.e. assign values to the reaction constants and initial numbers of molecules for each protein and gene. Initially, we use the biologically naive set of parameter values given in the following table.

	.. figure:: figures/parameters1.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

Now we perform stochastic simulation of the parameterised model. In order to assess the average behaviour of the system we perform 1,000 runs of the stochastic simulation and average the number of molecules over these 1,000 runs. The following figure shows the average number of protein molecules *P*.

	.. figure:: figures/simple_regulation_02.P.02.png
	   :scale: 60
	   :alt: alternate text
	   :align: center

As mentioned before, a common measure used to quantify the behaviour of a gene regulation network is *response time*. The response time is defined as the time taken to reach half the steady state concentration. From the above figure we can see that the steady state level of protein *P* is on average around 6.6 molecules. Therefore, the response time is the time taken to reach half this level i.e. 3.3 molecules, which is around 65 seconds.

Network motifs
##########################

A *network motif* is a recurring pattern in a network that occurs far more often than at random. The simple regulation network above in one such motif. Two other common motifs found in gene regulation networks are *negative autoregulation* and *positive autoregulation*. Schematic representations of these three motifs are shown below. 

	.. figure:: figures/motifs.png
	   :scale: 60
	   :alt: alternate text
	   :align: center

In negative autoregulation, the expressed protein *P* represses its own expression i.e. the *R* proteins in the simple regulation model are changed to *P*. 

	.. figure:: figures/reactions2.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

In positive autoregulation, the expressed protein *P* enhances its own expression i.e. the *I* proteins in the same model are changed to *P*. 

	.. figure:: figures/reactions3.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

The model parameters are the same as those for the simple regulation model given above.

Hands on
#################

.. toctree::
   :maxdepth: 1

   worksheets/worksheet1
   worksheets/worksheet2

