import json
import os
from enum import Enum
from pathlib import Path

from . import perception_types as PerceptionTypes
from . import reference_types as ReferenceTypes


def relevant_enum_classes(module):
    return [getattr(module, cls_name) for cls_name in dir(module)
            if not cls_name.startswith('_') and cls_name not in ['Enum', 'IntEnum', 'get_versions_with_clean'] and issubclass(getattr(module, cls_name), Enum)]

def save_as_json_file(module, filename):
    path = Path(os.path.dirname(os.path.realpath(__file__))) / filename
    with open(path, 'w') as f:
        json.dump({cls.__name__: {e.name: e.value for e in cls} for cls in relevant_enum_classes(module)},
                  f, indent=4, sort_keys=False)
    print('saved {} file'.format(filename))


def generate_enums():
    save_as_json_file(PerceptionTypes, 'perception_types.json')
    save_as_json_file(ReferenceTypes, 'reference_types.json')


if __name__ == '__main__':
    generate_enums()
