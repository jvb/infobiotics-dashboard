__all__ = ['species', 'dna', 'gene', 'rna', 'transcript', 'protein', 'transcription_factor', 'tf']

from infobiotics.commons.quantities.api import Quantity, molecules
#from id_generators import id_generator
from quantities import markup
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna, generic_rna, generic_protein

class species(object):
#    _id_generator = id_generator('s')

    def __init__(self, name, amount=0 * molecules, **kwargs):
        self.name = name
        self.amount = amount
        for k, v in kwargs.items(): setattr(self, k, v)
        
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        if isinstance(amount, int):
            self._amount = amount * molecules
            self._concentration = False
        elif isinstance(amount, Quantity):
            if amount.size > 1:
                raise ValueError('Species amounts should be single numbers, not arrays.')
            # quantity.rescale() raises ValueError if conversion not possible
            try:
                amount.rescale('mole')
                self._amount = amount
                self._concentration = False
            except ValueError:
                try:
                    amount.rescale('molar')
                    self._amount = amount
                    self._concentration = True
                except ValueError:
                    raise ValueError('Dimensionality of species amount (%s) not in molar, moles or molecules.' % amount.dimensionality)
        else:
            raise ValueError('Species amount must be an integer (number of molecules) or a quantity (in units of molecules, moles or molar concentration).')

    def repr(self, indent='', id=''):
        return indent + "%s%s%sspecies(name='%s', amount=%s * %s)" % (indent, id, '=' if id != '' else '', self.name, self.amount.magnitude, self.amount.dimensionality)

    def str(self, indent=''):
        # adapted from Quantity.__str__
        if markup.config.use_unicode:
            dims = self.amount.dimensionality.unicode
        else:
            dims = self.amount.dimensionality.string
        if dims.startswith('molecule'):
#            return '%s = %d %s' % (self.id, self.amount.magnitude, dims)
#        return '%s = %s %s' % (self.id, str(self.amount.magnitude), dims)
#            return '%d %s %s' % (self.amount.magnitude, dims, self.name)
#        return '%s = %s %s' % (str(self.amount.magnitude), dims, self.name)
            return indent + "%d %s '%s'" % (self.amount.magnitude, dims, self.name)
        return indent + "%s = %s '%s'" % (str(self.amount.magnitude), dims, self.name)


class sequenced(species):
    ''' http://www.biopython.org/wiki/Seq '''
    @property
    def sequence(self):
        return self._sequence
    
    @sequence.setter
    def sequence(self, sequence):
        raise NotImplementedError 


class dna(sequenced):
    def sequence(self, sequence):
        self._sequence = Seq(sequence, generic_dna)

gene = dna # alias


class rna(sequenced):
    def sequence(self, sequence):
        self._sequence = Seq(sequence, generic_rna)

transcript = rna # alias


class protein(sequenced):
    def sequence(self, sequence):
        self._sequence = Seq(sequence, generic_protein)

tf = transcription_factor = protein
