__all__ = [
    'y', 'year', 'years',
    'd', 'day', 'days',
    'MM', 'month', 'months',
    'h', 'hour', 'hours',
    'mm', 'minute', 'minutes',
    's', 'second', 'seconds',
    'ms', 'msecs', 'millisecs', 'milliseconds', 'millisecond',
    'us', 'usecs', 'microsecs', 'microseconds', 'microsecond',
    'ns', 'nsecs', 'nanosecs', 'nanoseconds', 'nanosecond',
    'ps', 'psecs', 'picosecs', 'picoseconds', 'picosecond',
    'fs', 'fsecs', 'femtosecs', 'femtoseconds', 'femtosecond',
    'asecs', 'attosecs', 'attoseconds', 'attosecond',
    'time_units'
]

from quantities.units.time import attosecond, femtosecond, picosecond, nanosecond, microsecond, millisecond, second, minute, hour, day, week, month, year

y = years = year
d = days = day
MM = months = month
h = hours = hour
mm = minutes = minute
s = seconds = second
ms = msecs = millisecs = milliseconds = millisecond
us = usecs = microsecs = microseconds = microsecond
ns = nsecs = nanosecs = nanoseconds = nanosecond
ps = psecs = picosecs = picoseconds = picosecond
fs = fsecs = femtosecs = femtoseconds = femtosecond
asecs = attosecs = attoseconds = attosecond

time_units = {
    'years':year,
    'months':month,
    'weeks':week,
    'days':day,
    'hours':hour,
    'minutes':minute,
    'seconds':second,
    'milliseconds':millisecond,
    'microseconds':microsecond,
    'nanoseconds':nanosecond,
    'picoseconds':picosecond,
    'femtoseconds':femtosecond,
    'attoseconds':attosecond,
}
