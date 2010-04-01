''' A unified means of logging.

The unified_logging module uses a set of defaults to

These defaults can be changed by assignment (ideally before getLogger() gets
called for the first time), for example: 

    import unified_logging
    unified_logging.level = unified_logging.INFO
    unified_logging.handler = unified_logging.FileHandler(filename)
    
The default level can be changed using the defcon(level) function where a level
of 5 = DEBUG and 1 = CRITICAL, e.g. unified_logging.defcon(3) sets 
level to WARNING.  

'''

from __future__ import with_statement

from logging import *

date_format = '%Y%m%d;%H:%M:%S'
def date_format_default():
    return date_format

format = '%(asctime)s|%(levelname)-8s|%(name)s>> %(message)s' 
def format_default():
    return format

level = DEBUG
def level_default():
    return level

handler = StreamHandler()
def handler_default():
    return handler

def get_logger(name, handler=None, format=None, date_format=None, level=None):
    ''' Returns a named logger.
    
    '''
        
    # use, possibly changed, defaults 
    if handler is None:
        handler = handler_default()
    if format is None:
        format = format_default()
    if date_format is None:
        date_format = date_format_default()
    if level is None:
        level = level_default()
        
    logger = getLogger(name)

    handler.setFormatter(Formatter(format, date_format))
    
    logger.addHandler(handler)
    
    logger.setLevel(level)
    
    return logger

def defcon(level):
    if level < 1:
        level = 1
    elif level > 5:
        level = 5
    if level == 5:
        level = DEBUG 
    elif level == 4:
        level = INFO
    elif level == 3:
        level = WARNING 
    elif level == 2:
        level = ERROR 
    elif level == 1:
        level = CRITICAL
        
def read_log_file(filename):
    with open(file, 'r') as log: 
        for line in log.readlines():
            info_message = line.split('>')
            datetime, logger_name, level = datetime_name_level 
