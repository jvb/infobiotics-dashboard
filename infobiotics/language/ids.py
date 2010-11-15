def id_generator(prefix=''):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1

compartment_id_generator = id_generator('c')
species_id_generator = id_generator('s')
rate_id_generator = id_generator('k')
reaction_id_generator = id_generator('r')
