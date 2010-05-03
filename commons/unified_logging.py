#TODO rename module to 'logging'?
''' A unified means of logging.

This module uses a set of global defaults for creating new loggers.

These defaults can be changed by assignment (ideally before getLogger() gets
called for the first time), for example: 

    import unified_logging
    unified_logging.level = unified_logging.INFO
    unified_logging.handler = unified_logging.FileHandler(filename)
    
The default level can be changed using the defcon(level) function where a level
of 5 = DEBUG and 1 = CRITICAL, e.g. unified_logging.defcon(3) sets 
default_level to WARNING.  

'''

import logging # namespace
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL # constants
from logging import disable, shutdown # functions

default_level = logging.ERROR

stream_handler = logging.StreamHandler()
#file_handler = logging.FileHandler('log')
default_handler = stream_handler
#default_handler = file_handler

# see 15.6.15. Formatter Objects at http://docs.python.org/library/logging.html
custom_format = '"%(message)s" %(module)s:%(lineno)s(%(funcName)s) \
%(name)s(%(levelno)s) \
%(asctime)s,%(msecs).3f [%(thread)d:%(process)d] \'%(pathname)s\''  
simple_format = '"%(message)s" %(module)s:%(lineno)s(%(funcName)s) [%(name)s(%(levelno)s)]'
default_format = simple_format
default_date_format = '%Y%m%d;%H:%M:%S'

def getLogger(name='', level=None, handler=None, format=None, date_format=None):
    ''' More flexible getLogger method than in standard logging module. '''
        
    # use, possibly changed, defaults 
    if level is None:
        level = default_level
    if handler is None:
        handler = default_handler
    if format is None:
        format = default_format
    if date_format is None:
        date_format = default_date_format
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler.setFormatter(logging.Formatter(format, date_format))
    logger.addHandler(handler)
    
    return logger


#def from_defcon(defcon_level):
#    ''' Translate DEFCON levels to logging levels. '''
#    if defcon_level < 1:
#        defcon_level = 1
#    elif defcon_level > 5:
#        defcon_level = 5
#    if defcon_level == 5:
#        return logging.DEBUG 
#    elif defcon_level == 4:
#        return logging.INFO
#    elif defcon_level == 3:
#        return logging.WARNING 
#    elif defcon_level == 2:
#        return logging.ERROR 
#    elif defcon_level == 1:
#        return logging.CRITICAL
#    
#def set_default_level(defcon_level):
#    ''' Set the default level. '''
#    global default_level
#    default_level = from_defcon(defcon_level)
#
#def inc_default_level():
#    ''' Increment the default level. '''
#    global default_level
#    default_level = inc_level(default_level)
#        
#def dec_default_level():
#    ''' Decrement the default level. '''
#    global default_level
#    default_level = dec_level(default_level)
#
#def inc_level(level):
#    if logging.DEBUG <= level < logging.INFO:
#        return logging.INFO
#    elif logging.INFO <= level < logging.WARNING:
#        return logging.WARNING
#    elif logging.WARNING <= level < logging.ERROR:
#        return logging.ERROR
#    elif logging.ERROR <= level < logging.CRITICAL:
#        return logging.CRITICAL
#
#def dec_level(level):
#    if logging.INFO <= level < logging.WARNING:
#        return logging.DEBUG
#    elif logging.WARNING <= level < logging.ERROR:
#        return logging.INFO
#    elif logging.ERROR <= level < logging.CRITICAL:
#        return logging.ERROR
#    elif logging.CRITICAL <= level:
#        return logging.CRITICAL
