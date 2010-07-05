import os.path
def shorten_path(path, width=80):
    if len(path) <= width:
        return path
    else:
        split = os.path.split(path)
        if len(split) == 1:
            return '...%s' % path[-(width-3):] 
        else:
            path = os.path.join('...', *split[1:])
        return shorten_path(path, width)

## {{{ http://code.activestate.com/recipes/148061/ (r6)
def wrap(text, width=80):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )


if __name__ == '__main__':
    
    # 2 very long lines separated by a blank line
    msg = """Arthur:  "The Lady of the Lake, her arm clad in the purest \
    shimmering samite, held aloft Excalibur from the bosom of the water, \
    signifying by Divine Providence that I, Arthur, was to carry \
    Excalibur. That is why I am your king!"
    
    Dennis:  "Listen. Strange women lying in ponds distributing swords is \
    no basis for a system of government. Supreme executive power derives \
    from a mandate from the masses, not from some farcical aquatic \
    ceremony!\""""
    
    # example: make it fit in 40 columns
    print(wrap(msg,40))
    
    # result is below
    """
    Arthur:  "The Lady of the Lake, her arm
    clad in the purest shimmering samite,
    held aloft Excalibur from the bosom of
    the water, signifying by Divine
    Providence that I, Arthur, was to carry
    Excalibur. That is why I am your king!"
    
    Dennis:  "Listen. Strange women lying in
    ponds distributing swords is no basis
    for a system of government. Supreme
    executive power derives from a mandate
    from the masses, not from some farcical
    aquatic ceremony!"
    """
    ## end of http://code.activestate.com/recipes/148061/ }}}
