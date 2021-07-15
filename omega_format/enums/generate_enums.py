import json
import os
from enum import Enum, IntEnum
from pathlib import Path

import perception_types as PerceptionTypes
import reference_types as ReferenceTypes

def relevant_enum_classes(module):
    return [getattr(module, cls_name) for cls_name in dir(module)
            if not cls_name.startswith('_') and not cls_name in ['Enum', 'IntEnum'] and issubclass(getattr(module, cls_name), Enum)]


def enum2c(obj, c_name='VVM'):
    c_name = c_name + obj.__name__
    if issubclass(obj, IntEnum):
        c = f'\nenum class {c_name} ' + '{\n'
        c += ',\n'.join([f'  {e.name} = {e.value}' for e in obj])
        c += '\n};\n'
        return c
    elif issubclass(obj, Enum):
        c = f'\nclass {c_name} ' + '{\n'
        c += 'public:\n'
        c += ''.join([f"  const char* {e.name} = \"{e.value}\";\n" for e in obj])
        c += '};\n'
        return c
    else:
        raise ValueError


def save_as_c(module, filename):
    path = Path(os.path.dirname(os.path.realpath(__file__))) / filename
    with open(path, 'w') as f:
        text_to_write = "#pragma once\n"
        text_to_write += "// auto-generated file from .py original\n"
        text_to_write += ''.join([enum2c(c) for c in relevant_enum_classes(module)])
        f.write(text_to_write)
    print('saved {} file'.format(filename))


def save_as_json_file(module, filename):
    path = Path(os.path.dirname(os.path.realpath(__file__))) / filename
    with open(path, 'w') as f:
        json.dump({cls.__name__: {e.name: e.value for e in cls} for cls in relevant_enum_classes(module)},
                  f, indent=4, sort_keys=False)
    print('saved {} file'.format(filename))


def main():
    save_as_json_file(PerceptionTypes, 'perception_types.json')
    save_as_json_file(ReferenceTypes, 'reference_types.json')
    save_as_c(PerceptionTypes, 'perception_types.h')
    save_as_c(ReferenceTypes, 'reference_types.h')


if __name__ == '__main__':
    main()
