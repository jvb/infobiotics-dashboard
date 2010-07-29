#######################
Creating Models of Gene Regulation in CellDesigner
#######################

In this section we will show, step-by-step, how to create models using the CellDesigner package. Once we have these models, we will be able perform stochastic simulations on it and analyse the results. 

Implementing a Simple Gene Regulation Model 
#######################

The model we will be creating first is the model of simple gene regulation described previously. The following tables summarize the reaction scheme and parameters for this model.

	.. figure:: ../figures/reactions1.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

	.. figure:: ../figures/parameters1.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

The following figure shows an annotated screenshot of CellDesigner with the complete model.

	.. figure:: ../figures/celldesigner-02.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

Follow the steps below and you should end up with something very similar. As you work through the steps, don't forget to save your model on a regular basis. Also, undo (**Edit->Undo** on the menubar or Ctrl-Z) can be very useful sometimes!

Step-by-step instructions:

  1. Open up CellDesigner (we're using version 4 here). You should find an icon on your desktop, or look in the Programs menu.

  2. Create a new model by selecting **File->New** from the menubar. In the dialogue box that appears, enter a name for the model. The name should only contain alphanumeric characters and underscores for spaces. Since we're creating a model of simple gene regulation, enter *simple_regulation* as the name, then click **OK**. If you want to change the model name or dimensions of the model canvas later, you can reopen this dialogue by selecting **Component->Model Information** from the menubar.

  3. Save the model by selecting **File->Save** from the menubar (or pressing Ctrl-S) then clicking **Save**. As you work through the rest of the steps below, don't forget to periodically save the model. Note: you might get a 'libSBML Consistency Check' warning when trying to save or load the model. Just ignore it and click **Save**.

  4. Create the gene *G* by left clicking once on the **Gene** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *G* and click **OK**. A yellow rectangle containing the letter *G* should appear on the canvas. Species can be moved around the canvas by pointing to them, holding down the left mouse button and dragging them to a new location.

  5. Set the initial amount of molecules to 1 for gene *G* by right clicking once on the newly created gene then choosing **Edit Species** from the menu that appears. In the dialogue box that pops up change *0.0* in the fourth text box (below the **Amount** radio button) to *1.0*. Click **Update** then **Close**.

  6. Create the protein *P* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *P* and click **OK**. A green rectangle containing the letter *P* should appear on the canvas. Since, by default, all initial amounts of species are set to 0 we don't need to set the initial amount of this species.

  7. Create the reaction between the gene *G* and protein *P* by left clicking once on the **State Transition** icon in the reaction toolbar. Now move the pointer to gene *G* on the canvas and left click once on one of the square anchor points which appears around the edge of gene *G*. Now move the pointer to protein *P* on the canvas and left click once on one of the anchor points which appears around protein *P*. An arrow should appear between gene *G* and protein *P* representing the reaction between these two species. The point where each end of the arrow is anchored can be changed by left clicking once on the reaction arrow, moving the pointer to one of the anchor boxes which appears at each end of the arrow, holding down the left mouse button and dragging the anchor box to a new position.

  8. Add gene *G* as a product of the reaction you've just created between gene *G* and protein *P* by left clicking once on the **Add Product** icon in the reaction toolbar, then moving the pointer over the reaction arrow connecting gene *G* and protein *P*. Left click the arrow once, then move the pointer to gene *G* and left click one of the anchor boxes which appears around the edge of gene *G*. A second reaction arrow should appear from the arrow between gene *G* and protein *P* back to gene *G*.

  9. Set the stochastic reaction constant for the reaction between gene *G* and protein *P* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k1* for the **id** and *0.1* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  10. Add the degradation reaction for protein *P* by left clicking once on the **Degradation** icon in the toolbar. Now move the pointer to protein *P* on the canvas and left click the protein once. A reaction arrow and degradation symbol should appear attached to protein *P*. Before doing anything else, move back up to the toolbar and left click the **Select Move** icon to switch back to selection mode. As with any other species, you can move the pointer over the degradation symbol on the canvas, hold down the left mouse button, and drag it to a new position on the canvas.

  11. Set the stochastic reaction constant for the degradation reaction for protein *P* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k2* for the **id** and *0.01* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  12. Create the repressor protein *R* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *R* and click **OK**. A green rectangle containing the letter *R* should appear on the canvas.

  13. Set the initial amount of molecules to *1* for repressor *R* by right clicking once on the newly created protein and choosing **Edit Species** from the menu that appears. In the dialogue box that pops up change *0.0* in the fourth text box (below the **Amount** radio button) to *1.0*. Click **Update** then **Close**.

  14. Create the repressor-gene complex by left clicking once on the **Complex** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *R.G* and click **OK**. A grey rectangle containing the letters *R.G* should appear on the canvas. Now move the pointer back to the species toolbar and create a new repressor protein *R* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *R* and click **OK**. A green rectangle containing the letter *R* should appear on the canvas. Move the pointer over the new *R* protein, hold down the left mouse button, and drag the protein into the grey *R.G* complex box. Now create a new gene *G* by left clicking once on the **Gene** icon in the species toolbar then move the pointer to the model canvas and left click on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *G* and click **OK**. A yellow rectangle containing the letter *G* should appear on the canvas. Drag this gene into the grey *R.G* complex box. The complex box can be resized by left clicking on the black border of the grey complex box. A small white square should appear in each corner of the complex box. Move the pointer over one of these squares, hold down the left mouse button, and drag the mouse until the complex box is a reasonable size but still contains the *R* protein and *G* gene you dragged inside it.

  15. Create the reaction which associates the repressor *R* and gene *G* into the *R.G* complex by left clicking once on the **Heterodimer Association** icon in the reaction toolbar. Now move the mouse first over the yellow gene *G* on the model canvas and left click once on one of the square anchor points which appears around the edge of the gene *G* box. Now move the pointer to the green repressor *R*, and again left click once on one of the anchor points which appears. Finally, move the pointer to the edge of the grey *R.G* complex box and click on one of the anchor points that appears. A reaction arrow coming from the gene *G* and repressor *R* and leading to the *R.G* complex should appear.

  16. Set the stochastic reaction constant for the association reaction between gene *G*, repressor *R* and complex *R.G* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k3* for the **id** and *1.0* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  17. Create the reaction which dissociates the complex *R.G* into the repressor *R* and gene *G* by left clicking once on the **Dissociation** icon in the reaction toolbar. Now move the mouse first over the grey *R.G* complex box on the model canvas and left click once on one of the square anchor points which appears around the edge of the *R.G* complex box. Now move the pointer to the yellow gene *G* box, and again left click once on one of the anchor points which appears. Finally, move the pointer to the green repressor *R* box and click on one of the anchor points that appears. A reaction arrow coming from the *R.G* complex and leading to the gene *G* and repressor *R* boxes should appear.

  18. Set the stochastic reaction constant for the dissociation reaction between complex *R.G* and gene *G* and repressor *R* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k4* for the **id** and *1.0* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  19. Create the inhibitor protein *I* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *I* and click **OK**. A green rectangle containing the letter *I* should appear on the canvas.

  20. Set the initial amount of molecules to *1* for inhibitor *I* by right clicking once on the newly created protein and choosing **Edit Species** from the menu that appears. In the dialogue box that pops up change *0.0* in the fourth text box (below the **Amount** radio button) to *1.0*. Click **Update** then **Close**.

  21. Create the repressor-inhibitor complex by left clicking once on the **Complex** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *R.I* and click **OK**.  A grey rectangle containing the letters *R.I* should appear on the canvas. Now move the pointer back to the toolbar and create a new repressor protein *R* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *R* and click **OK**. A green rectangle containing the letter *R* should appear on the canvas. Move the pointer over the new *R* protein, hold down the left mouse button, and drag the protein into the grey *R.I* complex box. Now create a new inhibitor *I* by left clicking once on the **Generic Protein** icon in the species toolbar then moving the pointer to the model canvas and left clicking on an empty space on the canvas. A dialogue box will appear asking for the name of the species. Enter *I* and click **OK**. A green rectangle containing the letter *I* should appear on the canvas. Drag this inhibitor into the grey *R.I* complex box. The complex box can be resized as before.

  22. Create the reaction which associates the repressor *R* and inhibitor *I* into the *R.I* complex by left clicking once on the **Heterodimer Association** icon in the reaction toolbar. Now move the mouse first over the green repressor *R* box on the model canvas and left click once on one of the square anchor points which appears around the edge of the repressor *R* box. Now move the pointer to the green inhibitor *I* box, and again left click once on one of the anchor points which appears. Finally, move the pointer to the edge of the grey *R.I* complex box and click on one of the anchor points that appears. A reaction arrow coming from the repressor *R* and inhibitor *I* and leading to the *R.I* complex should appear.

  23. Set the stochastic reaction constant for the association reaction between repressor *R*, inhibitor *I* and complex *R.I* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k5* for the **id** and *1.0* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  24. Create the reaction which dissociates the complex *R.I* into the repressor *R* and inhibitor *I* by left clicking once on the **Dissociation** icon in the reaction toolbar. Now move the mouse first over the grey *R.I* complex box on the model canvas and left click once on one of the square anchor points which appears around the edge of the *R.I* complex box. Now move the pointer to the green repressor *R* box, and again left click once on one of the anchor points which appears. Finally, move the pointer to the green inhibitor *I* box and click on one of the anchor points that appears. A reaction arrow coming from the *R.I* complex and leading to the repressor *R* and inhibitor *I* boxes should appear.

  25. Set the stochastic reaction constant for the dissociation reaction between complex *R.I*, and repressor *R* and inhibitor *I* by pointing to the reaction arrow then right clicking it and selecting **Edit KineticLaw** from the menu that appears. Select the **Parameters** button from the dialogue box, then select **New**. In the dialogue box that pops up, enter *k6* for the **id** and *1.0* for the **value**. Then close all the dialogue boxes by clicking **Add** then **Close**, **Update**, **Close** and **Close**.

  26. Export the model as SBML Level 2 by selecting **File->Export Pure Level 2 Version 1** from the menubar and replacing *untitled* by *simple_regulation.sbml* in the **Selection** text box, then click **Save**.

**Congratulations** - you now have a model of simple gene regulation which is ready to simulate!

Implementing negative and positive gene regulation
#######################

We now implement the other two models (negative autoregulation and positive autoregulation). The reaction schemes are

	.. figure:: ../figures/reactions2.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

for the negative autoregulation and

	.. figure:: ../figures/reactions3.png
	   :scale: 50
	   :alt: alternate text
	   :align: center

for the positive autoregulation. You don't need to redraw each model. Instead, save the simple regulation model you implemented before under a different name e.g. *negative_autoregulation* (**File->Save As** in the CellDesigner menubar), edit the model information (**Component->Model Information** in the menubar), and then rename the appropriate species (right click the species and select **Change Identity**).
