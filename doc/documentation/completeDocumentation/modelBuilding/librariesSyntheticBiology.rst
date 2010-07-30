Libraries of Modules in Synthetic Biology
---------------------------------------------------------------

In a **Synthetic biology scenario** modules can describe the molecular interactions involved in a well characterised synthetic construct as a `Biobrick <http://partsregistry.org/Main_Page>`_  that can be reused in the development of different synthetic cellular designs. For example, the following library illustrates how two different *inverters* can be designed in an incremental manner and introduced in a library in order to facilitate their inclusion in different synthetic cellular designs::

     libraryOfModules inverters
  
           PostTransc({X},{c_1,c_2,c_3,c_4,c_5},{l}) =
           {
               r1: [ rnaX_RNAP ]_l -c_1-> [ rnaX ]_l
               r2: [ rnaX ]_l -c_2-> [ ]_l 
               r3: [ rnaX ]_l -c_3-> [ rnaX + proteinX_Rib ]_l
               r4: [ proteinX_Rib ]_l -c_4-> [ proteinX ]_l
               r5: [ proteinX ]_l -c_5-> [ ]_l 
           }

           Plac({X},{c_1,c_2,c_3,c_4},{l}) =
           {
               r1: [ Plac_geneX ]_l -c_1-> [ Plac_geneX + rnaX_RNAP ]_l
               r2: [ proteinLacI + Plac_geneX ]_l -c_2-> [ Plac_LacI_geneX ]_l 
               r3: [ Plac_LacI_geneX ]_l -c_3-> [ proteinLacI + Plac_geneX ]_l
               r4: [ IPTG + Plac_LacI_geneX ]_l -c_4-> [ proteinLacI_IPTG + Plac_geneX ]_l
           }  

           PR({X},{c_1,c_2,c_3,c_4,c_5},{l}) =
           {
               r1: [ PR_geneX ]_l -c_1-> [ PR_geneX + rnaX_RNAP ]_l
               r2: [ proteinCI2 + PR_geneX ]_l -c_2-> [ PR_CI2_geneX ]_l
               r3: [ PR_CI2_geneX ]_l -c_3-> [ proteinCI2 + PR_geneX ]_l
               r4: [ proteinCI2 + PR_CI2_geneX ]_l -c_4-> [ PR_CI4_geneX ]_l
               r5: [ PR_CI4_geneX ]_l -c_5-> [ proteinCI2 + PR_CI2_geneX ]_l
           }

           Inverter_LacI({X},{},{l}) =
           {
               PostTransc({LacI},{},{l}) from this
               Plac({X}{}{l}) from this
           }

           Inverter_CI({X},{},{l}) =
           {
               PostTransc({CI},{},{l}) from this
               PR({X}{}{l}) from this
           }

     endLibraryOfModules

The *inverters* library consists of  five modules:

  - The **PostTransc module** describes transcription elongation and termination (r1), RNA degradation (r2), translation initiation (r3), translation elongation and termination (r4) and protein degradation (5) . This module can be seen as having the object *rnaX_RNAP* as input and the object *proteinX* as output. The string-object *rnaX_RNAP* represents an RNA polymerase that has initiated transcription of the *geneX* and *proteinX* represents the protein product of *geneX*.

  .. figure:: PostTransc.png
     :scale: 200
     :alt: alternate text
     :align: center

     .. 

     BioBrick representation of our *PostTransc* module.

  - The **Plac module** describes the binding and debinding (r2 and r3) of the repressor  *proteinLacI* to and from the *lactose operon promoter*. This repressor  prevents the initiation of the transcription of the gene fused to the promoter represented as the production of the string-object *rnaX_RNAP* (r1). This module also considers the case when the repressor debinds from the promoter in the presence of the signal *IPTG* (r4). This module can be considered to have the repressor *proteinLacI* and signal *IPTG* as input and *rnaX_RNAP* as output.  

  .. figure:: Plac.png
     :scale: 200
     :alt: alternate text
     :align: center

     .. 

     BioBrick representation of our *Plac* module. 

  - The **PR module** describes the cooperative binding and debinding (rules r2 - r5) of the repressor CI to the *PR* promoter of the bacteriophage lambda. This repressor  prevents the initiation of the transcription of the gene fused to the promoter represented as the production of the string-object *rnaX_RNAP* (r1). This module can be considered to have the repressor *proteinCI* as input and *rnaX_RNAP* as output.

  .. figure:: PR.png
     :scale: 200
     :alt: alternate text
     :align: center

     .. 

     BioBrick representation of our *PR* module. 

  - The **Inverter_LacI module** uses the repressor *LacI* and the promoter *Plac* to construct a molecular inverter with input transcripts of the LacI gene, *rnaLacI_RNAP*, and output transcripts of the gene fused to the promoter *Plac*, *rnaX_RNAP*. This is achieved by composing the module *PostTransc* instantiated with LacI and its characteristic rates and the module *Plac*. 

  .. figure:: inverterLacI.png
     :scale: 200
     :alt: alternate text
     :align: center

     .. 

     BioBrick representation of the inverter using the LacI repressor. 


  - The **Inverter_CI module** uses the repressor *CI* and the promoter *PR* to construct a molecular inverter with input transcripts of the CI gene, *rnaCI_RNAP*, and output transcripts of the gene fused to the promoter *PR*, *rnaX_RNAP*. This is achieved by composing the module *PostTransc* instantiated with CI and its characteristic rates and the module *PR*. 

  .. figure:: inverterCI.png
     :scale: 200
     :alt: alternate text
     :align: center

     .. 

     BioBrick representation of the inverter using the CI repressor.
