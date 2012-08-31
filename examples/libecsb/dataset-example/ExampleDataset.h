// simulation datasets definitions
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#ifndef EXAMPLEDATASET_H
#define EXAMPLEDATASET_H

#include <ecsb/ecsb.h>

namespace SimulationDatasets {

///////////////////////////////////
// "species information" dataset //
///////////////////////////////////

// species dataset entry
typedef struct {
	unsigned long si;  // species index
	char sn[255];  // species name
} SpeciesEntry;

// create species dataset datatype
hid_t createSpeciesDatatype(void);

///////////////////////////////////////
// "compartment information" dataset //
///////////////////////////////////////

// compartment dataset entry
typedef struct {
	unsigned long ci;  // compartment index
	char cid[255];  // compartment id
	char cn[255];  // compartment name
	unsigned long cx;  // compartment x position
	unsigned long cy;  // compartment y position
	unsigned long ct;  // compartment rule template index
} CompartmentEntry;

// create compartment dataset datatype
hid_t createCompartmentDatatype(void);

////////////////////////////////
// "rule information" dataset //
////////////////////////////////

// rule dataset entry
typedef struct {
	unsigned long rsi;  // ruleset index
	unsigned long ri;  // rule index
	char rid[255];  // rule id
	char rn[255];  // rule name
	long rx;  // rule x target
	long ry;  // rule y target
} RuleEntry;

// create rule dataset datatype
hid_t createRuleDatatype(void);

///////////////////////////////////
// "ruleset information" dataset //
///////////////////////////////////

// ruleset dataset entry
typedef struct {
	unsigned long rsi;  // ruleset index
	char rsn[255];  // ruleset name
	char rsc[255];  // ruleset compartment id
	unsigned long nr;  // number of rules in ruleset
} RulesetEntry;

// create ruleset dataset datatype
hid_t createRulesetDatatype(void);

/////////////////////////
// "reactions" dataset //
/////////////////////////

// reactions dataset entry
typedef struct {
	double t;  // time
	unsigned long si;  // species index
	unsigned long sl;  // species level
	unsigned long ci;  // compartment index
	unsigned long ri;  // rule index
} ReactionEntry;

// create reactions dataset datatype
hid_t createReactionDatatype(void);

////////////////////////////
// "propensities" dataset //
////////////////////////////

// propensities dataset entry
typedef struct {
	double *t;  // time
	unsigned long *ri;  // rule index (size: total rules)
	unsigned long *rsi;  // ruleset index (size: total rules)
	unsigned long *ci;  // compartment index (size: total rules)
	double *rp;  // rule propensity (size: total rules)
} PropensityEntry;

// create propensities dataset datatype
hid_t createPropensityDatatype(const unsigned long total_rules);

// convert propensities data entry to structure
void convertPropensityEntry(void *buffer, hid_t dtype,  PropensityEntry &entry, \
		const unsigned long index = 0);

///////////////////////
// "amounts" dataset //
///////////////////////

// amounts dataset entry
typedef struct {
 	double *t;  // time
	unsigned long *sl;  // species amounts (size: species x compartments)
} AmountEntry;

// create amounts dataset datatype
hid_t createAmountDatatype(const unsigned long num_species, \
		const unsigned long num_compartments);

// convert amounts data entry to structure
void convertAmountEntry(void *buffer, hid_t dtype, \
		AmountEntry &entry, const unsigned long index = 0);

};

#endif
