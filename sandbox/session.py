class Session(object):
    ''' Alter behaviour of some operations depending on whether the user is using
    the GUI, a Python shell or running a script (possibly in the GUI). '''
    is_interactive = True # if not interactive: never wait for user input
    has_gui = False # if not has_gui: 
    
session = Session() # default session
