__all__ = ['species', 'dna', 'gene', 'rna', 'transcript', 'protein']

from core import named
from enthought.traits.api import Either, Int, Property, Instance, Str
from quantities.quantity import Quantity
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna, generic_rna, generic_protein

class species(named):

    amount = Either(Int, Instance(Quantity))

    def __init__(self, quantity=0, **traits):
        self.quantity = quantity
        super(species, self).__init__(**traits)

    def __str__(self):
        return self.quantity

class sequenced(species):
    sequence = Property(Str)#Instance(Seq))
    def _get_sequence(self):
        return self._sequence

class dna(sequenced):
    def _set_sequence(self, sequence):
        self._sequence = Seq(sequence, generic_dna)

gene = dna # alias

class rna(sequenced):
    def _set_sequence(self, sequence):
        self._sequence = Seq(sequence, generic_rna)

transcript = rna # alias

class protein(sequenced):
    def _set_sequence(self, sequence):
        self._sequence = Seq(sequence, generic_protein)

