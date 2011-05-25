// test libecsb hdf5 dataset functions
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#include "ExampleDataset.h"

#include <string.h>

using namespace ECSB;
using namespace SimulationDatasets;

//////////////////
// example data //
//////////////////

// test species data
#define NUM_SPECIES	4
unsigned long species_index[NUM_SPECIES] = { 1, 2, 3, 4 };
char species_name[4][255] = { "A", "B", "C", "D" };

// test compartment data
#define NUM_COMPARTMENTS 3
unsigned long compartment_index[NUM_COMPARTMENTS] = { 1, 2, 3 };
char compartment_id[3][255] = { "c0", "c1", "c2" };
char compartment_name[3][255] = { "cytoplasm", "apoplast", "cytoplasm" };
unsigned long compartment_x[NUM_COMPARTMENTS] = { 0, 0, 0 };
unsigned long compartment_y[NUM_COMPARTMENTS] = { 0, 1, 2 };
unsigned long compartment_template[NUM_COMPARTMENTS] = { 0, 1, 0 };

// test amounts data
#define NUM_TIMEPOINTS 10
unsigned long amounts[NUM_SPECIES][NUM_COMPARTMENTS];

// test propensities data
#define NUM_RULES 3
#define NUM_RULE_APPLICATIONS 7

// test reaction data
#define NUM_REACTIONS 27

int main(int argc, char **argv)
{
// 	unsigned long i, j, k, entries, buffer_index;
// 	unsigned long chunk_size = 10;  // data buffer size for chunked datasets
// 
// 	/////////////////////////////
// 	// initialisation routines //
// 	/////////////////////////////
// 
// 	// declare variables
// 	H5::H5File dfile;  // hdf5 file
// 	H5::DataSet dset;  // hdf5 dataset
// 	H5::DataSpace dspace;  // hdf5 dataspace
// 	H5::CompType dtype;  // hdf5 datatype
// 
// 	// create datafile
// 	dfile = createDatafile("dataset-example.h5");
// 
// 	////////////////////////
// 	// attributes example //
// 	////////////////////////
// 
// 	// write some attributes
// 	writeAttribute("model file", "model1.xml", dfile);
// 	writeAttribute("number of species", NUM_SPECIES, dfile);
// 	writeAttribute("number of compartments", NUM_COMPARTMENTS, dfile);
// 	writeAttribute("number of rules", NUM_RULES, dfile);
// 	writeAttribute("simulation time", 143.865, dfile);
// 
// 	/////////////////////////////
// 	// species dataset example //
// 	/////////////////////////////
// 
// 	// create datatype
// 	dtype = createSpeciesDatatype();
// 
// 	// create dataspace
// 	entries = NUM_SPECIES;
// 	dspace = createDataspace(entries);
// 
// 	// create dataset
// 	dset = createDataset("species information", dfile, dtype, dspace);
// 
// 	// create data buffer
// 	SpeciesEntry *species_buffer = (SpeciesEntry *) \
// 			createDataBuffer(entries, dtype);
// 
// 	// create data entry
// 	SpeciesEntry *species_entry = (SpeciesEntry *) \
// 			createDataEntry(dtype);
// 
// 	// write data to buffer
// 	buffer_index = 0;
// 	for(i = 0; i < entries; i++) {
// 		// assign data to entry
// 		species_entry->si = species_index[i];
// 		strncpy(species_entry->sn, species_name[i], 255);
// 
// 		// copy data to buffer
// 		writeDataset(species_entry, species_buffer, dset, dtype, \
// 				dspace, buffer_index, entries);
// 	}
// 
// 	// close dataset
// 	closeDataset(dfile, dset, dtype, species_buffer, buffer_index, \
// 			entries);
// 
// 	// free data entry memory
// 	freeDataEntry(species_entry);
// 
// 	// free data buffer memory
// 	freeDataBuffer(species_buffer);
// 
// 	/////////////////////////////////
// 	// compartment dataset example //
// 	/////////////////////////////////
// 
// 	// create datatype
// 	dtype = createCompartmentDatatype();
// 
// 	// create dataspace
// 	entries = NUM_COMPARTMENTS;
// 	dspace = createDataspace(entries);
// 
// 	// create dataset
// 	dset = createDataset("compartment information", dfile, dtype, dspace);
// 
// 	// create data buffer
// 	CompartmentEntry *compartment_buffer = (CompartmentEntry *) \
// 			createDataBuffer(entries, dtype);
// 
// 	// create data entry
// 	CompartmentEntry *compartment_entry = (CompartmentEntry *) \
// 			createDataEntry(dtype);
// 
// 	// write data to buffer
// 	buffer_index = 0;
// 	for(i = 0; i < entries; i++) {
// 		// assign data to entry
// 		compartment_entry->ci = compartment_index[i];
// 		strncpy(compartment_entry->cid, compartment_id[i], 255);
// 		strncpy(compartment_entry->cn, compartment_name[i], 255);
// 		compartment_entry->cx = compartment_x[i];
// 		compartment_entry->cy = compartment_y[i];
// 		compartment_entry->ct = compartment_template[i];
// 
// 		// copy data to buffer
// 		writeDataset(compartment_entry, compartment_buffer, dset, dtype, \
// 				dspace, buffer_index, entries);
// 	}
// 
// 	// close dataset
// 	closeDataset(dfile, dset, dtype, compartment_buffer, buffer_index, \
// 			entries);
// 
// 	// free data entry memory
// 	freeDataEntry(compartment_entry);
// 
// 	// free data buffer memory
// 	freeDataBuffer(compartment_buffer);
// 
// 	///////////////////////////////
// 	// reactions dataset example //
// 	///////////////////////////////
// 
// 	// create datatype
// 	dtype = createReactionDatatype();
// 
// 	// create dataspace
// 	entries = chunk_size;
// 	dspace = createDataspace(entries);
// 
// 	// create dataset
// 	dset = createDataset("reactions", dfile, dtype, dspace);
// 
// 	// create data buffer
// 	ReactionEntry *reaction_buffer = (ReactionEntry *) \
// 			createDataBuffer(entries, dtype);
// 
// 	// create data entry
// 	ReactionEntry *reaction_entry = (ReactionEntry *) \
// 			createDataEntry(dtype);
// 
// 	// write data to buffer
// 	buffer_index = 0;
// 	for(i = 0; i < NUM_REACTIONS; i++) {
// 		// assign data to entry
// 		reaction_entry->t = i;
// 		reaction_entry->si = i + 1;
// 		reaction_entry->sl = i + 2;
// 		reaction_entry->ci = i + 3;
// 		reaction_entry->ri = i + 4;
// 
// 		// copy data to buffer
// 		writeDataset(reaction_entry, reaction_buffer, dset, dtype, \
// 				dspace, buffer_index, chunk_size);
// 	}
// 
// 	// close dataset
// 	closeDataset(dfile, dset, dtype, reaction_buffer, buffer_index, \
// 			chunk_size);
// 
// 	// free data entry memory
// 	freeDataEntry(reaction_entry);
// 
// 	// free data buffer memory
// 	freeDataBuffer(reaction_buffer);
// 
// 	//////////////////////////////////
// 	// propensities dataset example //
// 	//////////////////////////////////
// 
// 	// create datatype
// 	dtype = createPropensityDatatype(NUM_RULES);
// 
// 	// create dataspace
// 	entries = NUM_RULE_APPLICATIONS;
// 	dspace = createDataspace(entries);
// 
// 	// create dataset
// 	dset = createDataset("propensities", dfile, dtype, dspace);
// 
// 	// create data buffer
// 	void *propensity_buffer = createDataBuffer(entries, dtype);
// 
// 	// create data entry
// 	void *propensity_entry = createDataEntry(dtype);
// 
// 	// write data to buffer
// 	PropensityEntry pe;
// 	buffer_index = 0;
// 	for(i = 0; i < entries; i++) {
// 		// assign data to entry
// 		convertPropensityEntry(propensity_entry, dtype, pe);
// 		*pe.t = 26 + i;
// 		for(j = 0; j < NUM_RULES; j++) {
// 			pe.ri[j] = 27 + i;
// 			pe.rsi[j] = 28 + i;
// 			pe.ci[j] = 29 + i;
// 			pe.rp[j] = 30 + i;
// 		}
// 
// 		// copy data to buffer
// 		writeDataset(propensity_entry, propensity_buffer, dset, dtype, \
// 				dspace, buffer_index, chunk_size);
// 	}
// 
// 	// close dataset
// 	closeDataset(dfile, dset, dtype, propensity_buffer, buffer_index, \
// 			chunk_size);
// 
// 	// free data entry memory
// 	freeDataEntry(propensity_entry);
// 
// 	// free data buffer memory
// 	freeDataBuffer(propensity_buffer);
// 
// 	/////////////////////////////
// 	// amounts dataset example //
// 	/////////////////////////////
// 
// 	// create datatype
// 	dtype = createAmountDatatype(NUM_SPECIES, NUM_COMPARTMENTS);
// 
// 	// create dataspace
// 	entries = chunk_size;
// 	dspace = createDataspace(entries);
// 
// 	// create dataset
// 	dset = createDataset("amounts", dfile, dtype, dspace);
// 
// 	// create data buffer
// 	void *amount_buffer = createDataBuffer(entries, dtype);
// 
// 	// create data entry
// 	void *amount_entry = createDataEntry(dtype);
// 
// 	// write data to buffer
// 	AmountEntry le;
// 	buffer_index = 0;
// 	for(i = 0; i < entries; i++) {
// 		// assign data to entry
// 		convertAmountEntry(amount_entry, dtype, le);
// 		*le.t = i;
// 		for(j = 0; j < NUM_SPECIES; j++)
// 			for(k = 0; k < NUM_COMPARTMENTS; k++)
// 				get2DArrayEntry(le.sl, NUM_COMPARTMENTS, j, k) = i + j + k;
// 
// 		// copy data to buffer
// 		writeDataset(amount_entry, amount_buffer, dset, dtype, \
// 				dspace, buffer_index, chunk_size);
// 	}
// 
// 	// close dataset
// 	closeDataset(dfile, dset, dtype, reaction_buffer, buffer_index, \
// 			chunk_size);
// 
// 	// free data entry memory
// 	freeDataEntry(amount_entry);
// 
// 	// free data buffer memory
// 	freeDataBuffer(amount_buffer);
// 
// 	//////////////////////////
// 	// termination routines //
// 	//////////////////////////
// 
// 	// close datafile
// 	closeDatafile(dfile);

	return 0;
}
