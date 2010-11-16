__all__ = ['compartment_id_generator', 'species_id_generator', 'reaction_id_generator', 'rate_id_generator']

def id_generator(prefix=''):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1

compartment_id_generator = id_generator('c')
species_id_generator = id_generator('s')
reaction_id_generator = id_generator('r')
rate_id_generator = id_generator('k')


if __name__ == '__main__':
    for g in (compartment_id_generator, species_id_generator, reaction_id_generator, rate_id_generator):
        for i in range(3):
            print g.next(),
        print
