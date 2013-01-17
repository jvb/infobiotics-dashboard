def values_for_EnumEditor(l):
    ''' Returns a dict of strings mapped to themselves prefixed by a zero-padded 
    integer and a colon, in order for a TraitsUI EnumEditor to display them in
    their original order rather than alphabetically. '''
    w = len(str(len(l)))
    import string
    return dict((s, '%s:%s' % (string.zfill(i + 1, w), s)) for i, s in enumerate(l))
