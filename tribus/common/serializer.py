from yaml import SafeLoader, SafeDumper, Mark
from yaml import dump as _dump
from yaml import load as _load


def dump(value):
    return _dump(value, Dumper=SafeDumper)

yaml_dump = dump


def load(value):
    return _load(value, Loader=SafeLoader)

yaml_load = load


def yaml_mark_with_path(path, mark):
    # yaml c ext, cant be modded, convert to capture path
    return Mark(
        path, mark.index,
        mark.line, mark.column,
        mark.buffer, mark.pointer)
