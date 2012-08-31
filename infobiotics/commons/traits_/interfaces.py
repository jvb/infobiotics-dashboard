# traits.has_traits.CHECK_INTERFACES
# 0: (default) does not check whether classes implement their declared interfaces.
# 1: verifies that classes implement the interfaces they say they do, and logs a warning if they don't.
# 2: verifies that classes implement the interfaces they say they do, and raises an InterfaceError if they don't.
import traits.has_traits
# setup a logger
from infobiotics.commons.api import logging
logger = logging.getLogger('traits.interface_checker')
traits.has_traits.CHECK_INTERFACES = 0
traits.has_traits.CHECK_INTERFACES = 1
traits.has_traits.CHECK_INTERFACES = 2

