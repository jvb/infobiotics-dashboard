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

from logging import \
    DEBUG, INFO, WARN, ERROR, CRITICAL, \
    getLogger, disable, \
    StreamHandler, Formatter, \
    shutdown

default_handler = StreamHandler()
default_level = DEBUG
default_date_format = '%Y%m%d;%H:%M:%S'
# see 15.6.15. Formatter Objects at http://docs.python.org/library/logging.html
#default_header = '"<message>" on <time> from <logger> (level=<level>) at line of <function> in <module> (<path>) <pid>'
#default_format = '"%(message)s\" on %(asctime)s,%(msecs).3f from %(name)s (level=%(levelno)s) at line %(lineno)s of %(funcName)s in %(module)s (%(pathname)s) pid=%(process)d' 
default_header = 'message \
logger(level) module:line(function) time [thread:pid] \'path/to/module.py\''
default_format = '"%(message)s" %(module)s:%(lineno)s(%(funcName)s) \
%(name)s(%(levelno)s) \
%(asctime)s,%(msecs).3f [%(thread)d:%(process)d] \'%(pathname)s\''  

def get_logger(name='', level=None, handler=None, format=None, date_format=None):
    ''' Returns a named logger.

    e.g. unified_logging.get_logger
    '''
        
    # use, possibly changed, defaults 
    if level is None:
        level = default_level
    if handler is None:
        handler = default_handler
    if format is None:
        format = default_format
    if date_format is None:
        date_format = default_date_format
        
    logger = getLogger(name)
    logger.setLevel(level)
    handler.setFormatter(Formatter(format, date_format))
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

if __name__ == '__main__':
    pass

    logger1 = get_logger()
    disable(0)
    logger1.log(9, 'custom')
    logger1.log(19, 'testing')
    logger1.warn('warning')
    