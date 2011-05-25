// simulation datasets definitions
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#include "ExampleDataset.h"

#include <iostream>
#include <stdlib.h>

using namespace SimulationDatasets;

///////////////////////////////////
// "species information" dataset //
///////////////////////////////////

// create species dataset datatype
hid_t SimulationDatasets::createSpeciesDatatype(void)
{
	hid_t dtype;
	
	// initialise datatype
	if((dtype = H5Tcreate(H5T_COMPOUND, (size_t) sizeof(SpeciesEntry))) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
		
	// insert members
	if(H5Tinsert(dtype, "species index", HOFFSET(SpeciesEntry, si), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	hid_t dspace = H5Screate(H5S_SCALAR);
	hid_t stype = H5Tcopy(H5T_C_S1);
	H5Tset_size(stype, strlen("species name"));
	H5Tset_strpad(stype, H5T_STR_NULLTERM);
	if(H5Tinsert(dtype, "species name", HOFFSET(SpeciesEntry, sn), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tclose(stype);
	H5Sclose(dspace);

	return dtype;
}

///////////////////////////////////////
// "compartment information" dataset //
///////////////////////////////////////

// create compartment dataset datatype
hid_t SimulationDatasets::createCompartmentDatatype(void)
{
	hid_t dtype;
	
	// initialise datatype
	if((dtype = H5Tcreate(H5T_COMPOUND, (size_t) sizeof(CompartmentEntry))) \
			< 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
		
	// insert members
	if(H5Tinsert(dtype, "compartment index", HOFFSET(CompartmentEntry, ci), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	hid_t dspace = H5Screate(H5S_SCALAR);
	hid_t stype = H5Tcopy(H5T_C_S1);
	H5Tset_size(stype, strlen("compartment id"));
	H5Tset_strpad(stype, H5T_STR_NULLTERM);
	if(H5Tinsert(dtype, "compartment id", HOFFSET(CompartmentEntry, cid), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tset_size(stype, strlen("compartment name"));
	if(H5Tinsert(dtype, "compartment name", HOFFSET(CompartmentEntry, cn), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "compartment x position", \
			HOFFSET(CompartmentEntry, cx), H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "compartment y position", \
			HOFFSET(CompartmentEntry, cy), H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "compartment template index", \
			HOFFSET(CompartmentEntry, ct), H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tclose(stype);
	H5Sclose(dspace);

	return dtype;
}

////////////////////////////////
// "rule information" dataset //
////////////////////////////////

// create rule dataset datatype
hid_t SimulationDatasets::createRuleDatatype(void)
{
	hid_t dtype;
	
	// initialise datatype
	if((dtype = H5Tcreate(H5T_COMPOUND, (size_t) sizeof(RuleEntry))) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
		
	// insert members
	if(H5Tinsert(dtype, "rule template index", HOFFSET(RuleEntry, rsi), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "rule index", HOFFSET(RuleEntry, ri), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	hid_t dspace = H5Screate(H5S_SCALAR);
	hid_t stype = H5Tcopy(H5T_C_S1);
	H5Tset_size(stype, strlen("rule id"));
	H5Tset_strpad(stype, H5T_STR_NULLTERM);
	if(H5Tinsert(dtype, "rule id", HOFFSET(RuleEntry, rid), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tset_size(stype, strlen("rule name"));
	if(H5Tinsert(dtype, "rule name", HOFFSET(RuleEntry, rn), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "rule x target", HOFFSET(RuleEntry, rx), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "rule y target", HOFFSET(RuleEntry, ry), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tclose(stype);
	H5Sclose(dspace);

	return dtype;
}

///////////////////////////////////
// "ruleset information" dataset //
///////////////////////////////////

// create ruleset dataset datatype
hid_t SimulationDatasets::createRulesetDatatype(void)
{
	hid_t dtype;
	
	// initialise datatype
	if((dtype = H5Tcreate(H5T_COMPOUND, (size_t) sizeof(RulesetEntry))) \
			< 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
		
	// insert members
	if(H5Tinsert(dtype, "ruleset index", HOFFSET(RulesetEntry, rsi), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	hid_t dspace = H5Screate(H5S_SCALAR);
	hid_t stype = H5Tcopy(H5T_C_S1);
	H5Tset_size(stype, strlen("ruleset name"));
	H5Tset_strpad(stype, H5T_STR_NULLTERM);
	if(H5Tinsert(dtype, "ruleset name", HOFFSET(RulesetEntry, rsn), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tset_size(stype, strlen("ruleset compartment id"));
	if(H5Tinsert(dtype, "ruleset compartment id", HOFFSET(RulesetEntry, rsc), \
			stype) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "number of rules in ruleset", \
			HOFFSET(RulesetEntry, nr), H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	H5Tclose(stype);
	H5Sclose(dspace);

	return dtype;
}

/////////////////////////
// "reactions" dataset //
/////////////////////////

// create reactions dataset datatype
hid_t SimulationDatasets::createReactionDatatype(void)
{
	hid_t dtype;
	
	// initialise datatype
	if((dtype = H5Tcreate(H5T_COMPOUND, (size_t) sizeof(ReactionEntry))) \
			< 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
		
	// insert members
	if(H5Tinsert(dtype, "time", HOFFSET(ReactionEntry, t), \
			H5T_NATIVE_DOUBLE) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "species index", HOFFSET(ReactionEntry, si), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "species amount", HOFFSET(ReactionEntry, sl), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "compartment index", HOFFSET(ReactionEntry, ci), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	if(H5Tinsert(dtype, "rule index", HOFFSET(ReactionEntry, ri), \
			H5T_NATIVE_ULONG) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}

	return dtype;
}

////////////////////////////
// "propensities" dataset //
////////////////////////////

// create propensities dataset datatype
hid_t SimulationDatasets::createPropensityDatatype( \
		const unsigned long total_rules)
{
	hid_t dtype;
	
	// initialise datatype
	size_t size = doubleOffset(1) + 3 * uLongOffset(total_rules) + \
				doubleOffset(total_rules);
	if((dtype = H5Tcreate(H5T_COMPOUND, size)) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}

	return dtype;
	// insert members
/*	size = 0;
	if(H5Tinsert(dtype, "time", size, H5T_NATIVE_DOUBLE) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}
	hsize_t dims[1] = { total_rules };
	
		H5::ArrayType a1(H5::PredType::NATIVE_ULONG, 1, dims);
		size += doubleOffset(1);
		dtype.insertMember("rule index", size, a1);
		size += uLongOffset(total_rules);
		dtype.insertMember("ruleset index", size, a1);
		size += uLongOffset(total_rules);
		dtype.insertMember("compartment index", size, a1);
		H5::ArrayType a2(H5::PredType::NATIVE_DOUBLE, 1, dims);
		size += uLongOffset(total_rules);
		dtype.insertMember("rule propensity", size, a2);
		return dtype;
	}
	catch(H5::DataTypeIException error) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}*/
}

// convert propensities data entry to structure
void SimulationDatasets::convertPropensityEntry(void *buffer, \
		hid_t dtype, PropensityEntry &entry, const unsigned long index)
{
/*	try {
		// get entry in buffer
		DS_BYTE *row = ((DS_BYTE *) buffer) + index * dtype.getSize();
		
		// set structure variables
		entry.t = (double *) (row + \
				getEntryOffset(dtype, "time"));
		entry.ri = (unsigned long *) (row + \
				getEntryOffset(dtype, "rule index"));
		entry.rsi = (unsigned long *) (row + \
				getEntryOffset(dtype, "ruleset index"));
		entry.ci = (unsigned long *) (row + \
				getEntryOffset(dtype, "compartment index"));
		entry.rp = (double *) (row + \
				getEntryOffset(dtype, "rule propensity"));
	}
	catch(H5::DataTypeIException error) {
		std::cerr << "error: couldn't access datatype entry\n";
		exit(1);
	}*/
}

///////////////////////
// "amounts" dataset //
///////////////////////

// create amounts dataset datatype
hid_t SimulationDatasets::createAmountDatatype( \
		const unsigned long num_species, const unsigned long num_compartments)
{
	hid_t dtype;
	
	// initialise datatype
	size_t size = doubleOffset(1) + \
				num_species * uLongOffset(num_compartments);
	if((dtype = H5Tcreate(H5T_COMPOUND, size)) < 0) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}

	return dtype;
/*	try {
		// initialise datatype
		size_t size = doubleOffset(1) + \
				num_species * uLongOffset(num_compartments);
		H5::CompType dtype = H5::CompType(size);
		
		// insert members
		size = 0;
		dtype.insertMember("time", size, H5::PredType::NATIVE_DOUBLE);
		hsize_t dims[2] = { num_species, num_compartments };
		H5::ArrayType a1(H5::PredType::NATIVE_ULONG, 2, dims);
		size += doubleOffset(1);
		dtype.insertMember("species amounts", size, a1);
		return dtype;
	}
	catch(H5::DataTypeIException error) {
		std::cerr << "error: couldn't create datatype\n";
		exit(1);
	}*/
}

// convert amounts data entry to structure
void SimulationDatasets::convertAmountEntry(void *buffer, hid_t dtype, \
		AmountEntry &entry, const unsigned long index)
{
/*	try {
		// get entry in buffer
		DS_BYTE *row = ((DS_BYTE *) buffer) + index * dtype.getSize();
		
		// set structure variables
		entry.t = (double *) (row + \
				getEntryOffset(dtype, "time"));
		entry.sl = (unsigned long *) (row + \
				getEntryOffset(dtype, "species amounts"));
	}
	catch(H5::DataTypeIException error) {
		std::cerr << "error: couldn't access datatype entry\n";
		exit(1);
	}*/
}
