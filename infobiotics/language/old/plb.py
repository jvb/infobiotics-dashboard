'''
The name of this module is the name of the library.

Can put metadata in the module docstring (this), comments or variables, e.g.:

Author: Jonathan Blakes
Date: 15th June 2010
Description: A example library containing basic gene regulatory mechanisms in traited fashion

'''

# Author: Jonathan Blakes
# Date: 15th June 2010
# Description: A example library containing basic gene regulatory mechanisms in traited fashion

author = 'Jonathan Blakes'
date = '15th June 2010'
description = 'A example library containing basic gene regulatory mechanisms \
in traited fashion'

from rule import Rule

def LocalRule(reactants, products, constant, label):
    ''' Reduces syntax for declaring Rules with reactants and products in the 
    same compartment (but not by much).
    
    Actually a module!
    
    '''
    return Rule(
        reactantsInside=reactants, 
        reactantsLabel=label,
        productsInside=products,
        productsLabel=label,
        constant=constant,
    )

def LocalDegradation(reactant, c_degradation, label):
    return LocalRule(
        reactants={reactant:1},
        products={},
        constant=c_degradation,
        label=label,
    )

def bind(*args):
    return '.'.join(args)

#def unbound(c):
#    return tuple(c.split('.'))

def LocalComplexation(left_molecule, right_molecule, c_binding, c_unbinding, label):
    complex = bind(left_molecule,right_molecule)
    binding = LocalRule(
        reactants={left_molecule:1,right_molecule:1},
        products={complex:1},
        constant=c_binding,
        label=label,
    )
    unbinding = Rule(
        reactants={complex:1},
        products={left_molecule:1,right_molecule:1},
        constant=c_unbinding,
        label=label,
    )
    return binding, unbinding


def LocalTranslation(rna, protein, constant, label):
    return LocalRule({rna:1}, {protein:1}, constant, label)


def UnReg(geneX, rnaX, c_transcription, label):
    return LocalRule(
        reactants={geneX:1}, 
        products={geneX:1, rnaX:1}, 
        constant=c_transcription,
        label=label,
    )

def PosReg(proteinX, geneY, rnaY, c_binding, c_unbinding, c_bound_transcription, label):
    ''' A module representing the positive regulation of a protein X over a gene Y. '''
    r1, r2 = LocalComplexation(proteinX, geneY, c_binding, c_unbinding, label)
    complex = bind(proteinX,geneY)
    r3 = LocalRule(
        reactants={complex:1},
        products={complex:1,rnaY:1},
        constant=c_bound_transcription,
        label=label,
    )
    return r1, r2, r3 


def NegReg(proteinX, geneY, c_binding, c_unbinding, label):
    ''' A module representing the negative regulation of a protein X over a gene Y. '''
    r1, r2 = LocalComplexation(proteinX, geneY, c_binding, c_unbinding, label)
    return r1, r2

def CoopNegReg(proteinX, geneY, c_binding, c_unbinding, c_binding2, c_unbinding2, c_bound_transcription, c_bound_transcription2, label):
    return (
        PosReg(proteinX, geneY, rnaY, c_binding, c_unbinding, c_bound_transcription, label),
        PosReg(proteinX, bind(proteinX,geneY), rnaY, c_binding2, c_unbinding2, c_bound_transcription2, label),
    )

def PostTransc(rnaX, proteinX, c_rnaX_degradation, c_translation, c_proteinX_degradation, label):
    ''' A module representing some post transcriptional processes such as rna degradation, translation and protein degradation. '''
    return (
        LocalDegradation(rnaX, c_rnaX_degradation, label),
        LocalTranslation(rnaX, proteinX, c_translation, label),
        LocalDegradation(proteinX, c_proteinX_degradation, label),
    )


# transcriptional motifs

def NAR(proteinX, geneX, rnaX, c_transcription, c_binding, c_unbinding, label):
    return (
        UnReg(geneX, rnaX, c_transcription, label), 
        NegReg(proteinX, geneX, c_binding, c_unbinding, label),
    )

#rsaL_NAR = NAR('rsaL', 'mrsaL', 'RsaL', 0.1, 0.5, 0.2, 'PAO1')
##print rsaL_NAR
#
#def rsaL_NAR():
#    return NAR('rsaL', 'mrsaL', 'RsaL', 0.1, 0.5, 0.2, 'PAO1')
##print rsaL_NAR
#
#def rsaL_NAR_partial(c_transcription, c_binding, c_unbinding):
#    return NAR('rsaL', 'mrsaL', 'RsaL', c_transcription, c_binding, c_unbinding, 'PAO1')
##print rsaL_NAR_partial
#
#def rsaL_NAR_defaults(gene='rsaL', rna='mrsaL', protein='RsaL', c_transcription=0.1, c_binding=0.5, c_unbinding=0.2, label='PAO1'):
#    return NAR(gene, rna, protein, c_transcription, c_binding, c_unbinding, label)
##print rsaL_NAR_defaults
#
#for r in rsaL_NAR():
#    print r

def CoopNAR(proteinX, geneX, rnaX, c_transcription, c_binding, c_unbinding, c_binding2, c_unbinding2, c_bound_transcription, c_bound_transcription2, label):
    return (
        UnReg(geneX, rnaX, c_transcription, label), 
        CoopNegReg(proteinX, geneX, c_binding, c_unbinding, c_binding2, c_unbinding2, c_bound_transcription, c_bound_transcription2, label),
    )

def PAR(proteinX, geneX, rnaX, c_transcription, c_binding, c_unbinding, c_bound_transcription, label):
    return (
        UnReg(geneX, rnaX, c_transcription, label), 
        CoopNegReg(proteinX, geneX, c_binding, c_unbinding, c_bound_transcription, label),
    )


'''
TODO defining modules as rules has the following advantages:
1. they can't have state
2. we can piggyback the args and kwargs parameters =- use Python's own parameters mechanism  
3. we can mimic partial application by creating a module function that calls another module function with some parameters 'fixed' and other open.
4. they must be global to be used declaratively in SPsystem definitions.
5. they can be imported using Python's own import mechanism
6. we can write programs that create modules!
'''
