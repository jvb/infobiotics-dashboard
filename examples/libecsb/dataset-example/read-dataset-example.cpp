// test libecsb hdf5 dataset functions
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#include "ExampleDataset.h"

using namespace ECSB;
using namespace SimulationDatasets;

int main(int argc, char **argv)
{
	unsigned long i, j, k, entries, buffer_size, buffer_index;
	unsigned long chunk_size = 5;  // data buffer size for chunked datasets
	char *model_file;
	unsigned long num_species, num_compartments, num_rules;
	double simulation_time;

	/////////////////////////////
	// initialisation routines //
	/////////////////////////////

	// declare variables
	hid_t dfile;  // hdf5 file
	hid_t dset;  // hdf5 dataset
	hid_t dtype;  // hdf5 datatype

	// open datafile
	dfile = openDatafile("dataset-example.h5");
	
	////////////////////////
	// attributes example //
	////////////////////////
	
	// read some attributes
	readAttribute("model file", model_file, dfile);
	readAttribute("number of species", num_species, dfile);
	readAttribute("number of compartments", num_compartments, dfile);
	readAttribute("number of rules", num_rules, dfile);
	readAttribute("simulation time", simulation_time, dfile);
	
	// just print attributes
	printf("*** attributes ***\n");
	printf("model file = %s\n", model_file);
	printf("number of species = %ld\n", num_species);
	printf("number of compartments = %ld\n", num_compartments);
	printf("number of rules = %ld\n", num_rules);
	printf("simulation time = %f\n", simulation_time);
	
	/////////////////////////////
	// species dataset example //
	/////////////////////////////
	
	// open dataset
	dset = openDataset("species information", dfile);
	
	// create datatype
	dtype = createSpeciesDatatype();
	
	// create data buffer
	buffer_size = getDatasetSize(dset);
	SpeciesEntry *species_buffer = (SpeciesEntry *) \
			createDataBuffer(buffer_size, dtype);
	
	// read data to buffer
	readDataset(species_buffer, dset);
	
	// access data in buffer
	printf("\n*** species dataset ***\n");
	for(i = 0; i < buffer_size; i++) {
		// just print data here
		printf("index=%ld name=%s\n", species_buffer[i].si, \
				species_buffer[i].sn);
	}
	
	// close dataset
	closeDataset(dset);
	
	// free data buffer memory
	freeDataBuffer(species_buffer);
	
	/////////////////////////////////
	// compartment dataset example //
	/////////////////////////////////
	
	// open dataset
	dset = openDataset("compartment information", dfile);
	
	// create datatype
	dtype = createCompartmentDatatype();
	
	// create data buffer
	buffer_size = getDatasetSize(dset);
	CompartmentEntry *compartment_buffer = (CompartmentEntry *) \
			createDataBuffer(buffer_size, dtype);
	
	// read data to buffer
	readDataset(compartment_buffer, dset);
	
	// access data in buffer
	printf("\n*** compartment dataset ***\n");
	for(i = 0; i < buffer_size; i++) {
		// just print data here
		printf("index=%ld id=%s name=%s x=%ld y=%ld template=%ld\n", \
				compartment_buffer[i].ci, compartment_buffer[i].cid, \
				compartment_buffer[i].cn, compartment_buffer[i].cx, \
				compartment_buffer[i].cy, compartment_buffer[i].ct);
	}
	
	// close dataset
	closeDataset(dset);
	
	// free data buffer memory
	freeDataBuffer(compartment_buffer);
	
	///////////////////////////////
	// reactions dataset example //
	///////////////////////////////
		
	// open dataset
	dset = openDataset("reactions", dfile);
	
	// create datatype
	dtype = createReactionDatatype();
	
	// create data buffer
	buffer_size = chunk_size;
	ReactionEntry *reaction_buffer = (ReactionEntry *) \
			createDataBuffer(buffer_size, dtype);
	
	// read data to buffer
	printf("\n*** reactions dataset ***\n");
	buffer_index = 0;
	while((entries = readDataset(reaction_buffer, dset, dtype, \
			buffer_index, buffer_size)))
		// access data in buffer
		for(i = 0; i < entries; i++) {
			// just print data here
			printf("%f %ld %ld %ld %ld\n", reaction_buffer[i].t, \
					reaction_buffer[i].si, reaction_buffer[i].sl, \
					reaction_buffer[i].ci, reaction_buffer[i].ri);
		}
		
	// close dataset
	closeDataset(dset);
	
	// free data buffer memory
	freeDataBuffer(reaction_buffer);
	
	//////////////////////////////////
	// propensities dataset example //
	//////////////////////////////////
		
	// open dataset
	dset = openDataset("propensities", dfile);
	
	// create datatype
	dtype = createPropensityDatatype(num_rules);
	
	// create data buffer
	buffer_size = chunk_size;
	void *propensity_buffer = createDataBuffer(buffer_size, dtype);
		
	// read data to buffer
	printf("\n*** propensities dataset ***\n");
	PropensityEntry propensity_entry;
	buffer_index = 0;
	while((entries = readDataset(propensity_buffer, dset, dtype, \
			buffer_index, buffer_size)))
		// access data in buffer
		for(i = 0; i < entries; i++) {
			convertPropensityEntry(propensity_buffer, dtype, \
					propensity_entry, i);
			// just print data here
			printf("time=%f", *propensity_entry.t);
			for(j = 0; j < num_rules; j++)
				printf(" [%ld,%ld,%ld,%f]", propensity_entry.ri[j], \
						propensity_entry.rsi[j], propensity_entry.ci[j], \
						propensity_entry.rp[j]);
			printf("\n");
		}
	
	// close dataset
	closeDataset(dset);
	
	// free data buffer memory
	freeDataBuffer(propensity_buffer);
	
	////////////////////////////
	// amounts dataset example //
	////////////////////////////
		
	// open dataset
	dset = openDataset("amounts", dfile);
	
	// create datatype
	dtype = createAmountDatatype(num_species, num_compartments);
	
	// create data buffer
	buffer_size = chunk_size;
	void *amount_buffer = createDataBuffer(buffer_size, dtype);
		
	// read data to buffer
	printf("\n*** amounts dataset ***\n");
	AmountEntry amount_entry;
	buffer_index = 0;
	while((entries = readDataset(amount_buffer, dset, dtype, \
			buffer_index, buffer_size)))
		// access data in buffer
		for(i = 0; i < entries; i++) {
			convertAmountEntry(amount_buffer, dtype, amount_entry, i);
			// just print data
			printf("time=%f", *amount_entry.t);
			for(j = 0; j < num_species; j++)
				for(k = 0; k < num_compartments; k++)
					printf(" [%ld,%ld,%ld]", j, k, \
							get2DArrayEntry(amount_entry.sl, num_compartments, \
							j, k));
			printf("\n");
		}
	
	// close dataset
	closeDataset(dset);
	
	// free data buffer memory
	freeDataBuffer(amount_buffer);
	
	//////////////////////////
	// termination routines //
	//////////////////////////
	
	// close datafile
	closeDatafile(dfile);

	return 0;
}
