import unified_logging

# must change default handler *before* getting logger with default handler
#unified_logging.handler = unified_logging.FileHandler('/home/jvb/Desktop/logger')

# get a *new* 'named' logger with default handler
logger = unified_logging.get_logger('uses_unified_logging')

# test messages
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")