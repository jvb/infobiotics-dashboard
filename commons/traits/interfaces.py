# enthought.traits.has_traits.CHECK_INTERFACES
# 0: (default) does not check whether classes implement their declared interfaces.
# 1: verifies that classes implement the interfaces they say they do, and logs a warning if they don't.
# 2: verifies that classes implement the interfaces they say they do, and raises an InterfaceError if they don't.
import enthought.traits.has_traits
# setup a logger
from commons.api import logging
logger = logging.get_logger('enthought.traits.interface_checker')
enthought.traits.has_traits.CHECK_INTERFACES = 0
enthought.traits.has_traits.CHECK_INTERFACES = 1
enthought.traits.has_traits.CHECK_INTERFACES = 2

