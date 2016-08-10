from   __future__  import print_function, unicode_literals
from   collections import Mapping
from   datetime    import datetime
import re

def write_properties(props, fp, separator='=', comment=None, timestamp=True):
    if isinstance(props, Mapping):
        items = (k, props[k] for k in props)
    else:
        items = props
    if comment is not None:
        print('#' + escape_comment(comment), file=fp)
    if timestamp:
        if not isinstance(timestamp, datetime):
            try:
                from dateutil.tz import tzlocal
            except ImportError:
                tz = None
            else:
                tz = tzlocal()
            timestamp = datetime.now(tz)
        ### TODO: Make strftime use the C locale (or, failing that, convert the
        ### return value to Latin-1)
        print(timestamp.strftime('#%a %b %d %H:%M:%S %Z %Y'), file=fp)
        ### Squash the double-space around %Z when the timestamp is naive?
    for k,v in items:
        print(join_key_value(k, v, separator), file=fp)

def escape_comment(comment):
    ###
    comment = re.sub(r'(\r\n?|\n)(?![#!])', r'\1#', comment)
    ### Convert non-Latin-1 characters to \uXXXX escape sequences
    ### Should this add the leading '#' as well?

def join_key_value(key, value, separator='='):
    # Escapes `key` and `value` the same way as java.util.Properties.store()
    return escape(key) \
        + separator \
        + re.sub(r'^ +', lambda m: r'\ ' * m.end(), _base_escape(value))

_escapes = {
    '\t': r'\t',
    '\n': r'\n',
    '\f': r'\f',
    '\r': r'\r',
    '!': r'\!',
    '#': r'\#',
    ':': r'\:',
    '=': r'\=',
    '\\': r'\\',
}

def _esc(m):
    c = m.group()
    try:
        return _escapes[c]
    except KeyError:
        c = ord(c)
        if c > 0xFFFF:
            # Does Python really not have a decent builtin way to calculate
            # surrogate pairs?
            assert c <= 0x10FFFF
            c -= 0x10000
            return r'\u{:04x}\u{:04x}'.format(
                0xD800 + (c >> 10),
                0xDC00 + (c & 0x3FF)
            )
        else:
            return r'\u{:04x}'.format(c)

def _base_escape(field):
    return re.sub(r'[^\x20-\x7E]|[\\#!=:]', _esc, field)

def escape(field):
    # Escapes `field` so that it can be used as either a key or a value
    return _base_escape(field).replace(' ', r'\ ')
