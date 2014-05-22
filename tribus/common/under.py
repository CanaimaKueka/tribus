import string

_SAFE_CHARS = set(string.ascii_letters + string.digits + ".-")
_CHAR_MAP = {}
for i in range(256):
    c = chr(i)
    _CHAR_MAP[c] = c if c in _SAFE_CHARS else "_%02x_" % i
_quote_char = _CHAR_MAP.__getitem__


def quote(unsafe):
    return "".join(map(_quote_char, unsafe))
