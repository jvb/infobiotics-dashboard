import os

def shorten_path(path, width=80):
    if len(path) <= width:
        return path
    else:
        split = os.path.split(path)
        head, tail = split
        if head == '' or head == '...':
            almost_half = (width - 3) // 2
            return '%s...%s' % (path[:almost_half], path[len(path) - almost_half:]) 
        else:
            path = os.path.join('...', os.sep.join(head.split(os.sep)[2:]), tail)
        return shorten_path(path, width)
# test
#print shorten_path('/home/jvb/dashboard/examples/NAR-pmodelchecker/negativeAutoregulationModel.lpp', 30)
#print shorten_path('/home/jvb/dashboard/examples/NAR-pmodelchecker/negativeAutoregulationModel.lpp', 40)
#print shorten_path('/home/jvb/dashboard/examples/NAR-pmodelchecker/negativeAutoregulationModel.lpp', 50)
#print shorten_path('/home/jvb/dashboard/examples/NAR-pmodelchecker/negativeAutoregulationModel.lpp', 60)
#exit()

def wrap_path(path):
    dirs = path.split(os.sep)
    path = ''
    for dir in dirs:
        if not dir:
            continue
        if len(path.split(os.linesep)[-1]) + len(dir) <= 80 + len(os.sep):
            path = os.sep.join([path, dir])
        else:
            path += os.sep + os.linesep + dir
    return path
#for i, path in enumerate(paths):
#    dirs = path.split(os.sep)
#    path = ''
#    for dir in dirs:
#        if not dir:
#            continue
#        if len(path.split(os.linesep)[-1]) + len(dir) <= 80 + len(os.sep):
#            path = os.sep.join([path, dir])
#        else:
#            path += os.sep + os.linesep + dir
#    paths[i] = path
#paths = os.linesep.join(paths)
def wrap_paths(paths, joiner=os.linesep):
    for i, path in enumerate(paths):
        paths[i] = wrap_path(path)
    return joiner.join(paths)
# test
#paths = [
#    '/home/jvb/eclipse/workspaces/infobiotics/infobiotics-dashboard/examples/pmodelchecker/Const/modelCheckingPRISM',
#    '/home/jvb/eclipse/workspaces/infobiotics/',
#]
#print wrap_paths(paths)
#exit()

    
def wrap(text, width=80, splitter=' ', joiner=os.linesep):
    '''A word-wrap function that preserves existing line breaks and most spaces 
    in the text. Expects that existing line breaks are posix newlines (\n).

    Adapted from http://code.activestate.com/recipes/148061/ (r6)
    
    '''
    return reduce(
        lambda line, word, width=width: '%s%s%s' % (
            line,
            [' ', joiner][(len(line) - line.rfind(os.linesep) - 1 + len(word.split(os.linesep, 1)[0]) >= width)],
            word
         ),
        text.split(splitter)
    )
    
    
if __name__ == '__main__':
    
    # 2 very long lines separated by a blank line
    text = '''Arthur:  "The Lady of the Lake, her arm clad in the purest \
shimmering samite, held aloft Excalibur from the bosom of the water, \
signifying by Divine Providence that I, Arthur, was to carry \
Excalibur. That is why I am your king!"

Dennis:  "Listen. Strange women lying in ponds distributing swords is \
no basis for a system of government. Supreme executive power derives \
from a mandate from the masses, not from some farcical aquatic \
ceremony!\"'''
    
    # example: make it fit in 40 columns
    print(wrap(text, 40))
#    import textwrap
#    print textwrap.TextWrapper(width=40, break_long_words=True).fill(text)
    
    # result is below
    '''
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
    '''
