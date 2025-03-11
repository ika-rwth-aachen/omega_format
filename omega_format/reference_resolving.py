import numpy as np
from h5py import Group
from copy import deepcopy
from collections import UserDict, UserList
from .settings import get_settings
from pydantic import BaseModel, ConfigDict
from typing import Any, Callable, Generator


__all__ = ['ReferenceDict', 'require_group', 'ReferenceElement', 'InputClassBase', 'ListWithProperties', 'DictWithProperties', 'value_or_first_element', 'ReferenceNotResolved', 'ReferenceNotResolvable', 'raise_not_resolved']


def require_group(h5file, group_str):
    require_group = False if get_settings().ALLOW_MISSING_TL_GROUPS and group_str not in h5file.keys() else True
    return require_group


def value_or_first_element(value):
    if isinstance(value, np.ndarray):
        return value[0] # maybe check case of empty dataset here
    else:
        return value


def is_not_overridden(o):
    if hasattr(o, 'overridden_by') and getattr(o, 'overridden_by') is not None:
        return False
    else:
        return True

class InputClassBase(BaseModel):
    """

    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')
    def resolve(self, input_recording=None):
        """
        Iteratively searches for every `ReferenceDict` in the Class and resolves its references.
        """
        if input_recording is None:
            raise ValueError('You have to provide a `ReferenceRecording` for this function to work!')
        for p, v in vars(self).items():
            if isinstance(v, ReferenceDict) or isinstance(v, ReferenceElement):
                v.resolve(input_recording)
            elif isinstance(v, DictWithProperties) and len(v) > 0 and isinstance(list(v.values())[0], InputClassBase):
                for o in v.values():
                    o.resolve(input_recording)

    @classmethod
    def convert2objects(cls, file, group_name=None, check_require=False, validate=True, legacy=None):
        """Converts list of dicts to list of objects of type `object_class`"""
        if require_group(file, group_name) or not check_require:
            return DictWithProperties({int(k): cls.from_hdf5(o, validate=validate, legacy=legacy) for k, o in file[group_name].items() if k!='converterVersion'})
        else:
            return DictWithProperties()

    @classmethod
    def resolve_func(cls, ir, i):
        raise NotImplementedError()

    def __repr__(self):
        return self.__repr_name__()

    def __pretty__(self, fmt: Callable[[Any], Any], **kwargs: Any) -> Generator[Any, None, None]:
        yield self.__repr_name__()

    def __str__(self):
        return self.__repr_name__()


class ListWithProperties(UserList):
    """
    This list is designed to only take objects of the same class. It enables the direct access to attributes of
    the objects in the list as a list of the attributes, where the position of the attributes corresponds to the
    position of the object in the list.
    It also implements `.values()` to be compatible to the interacting with `DictWithProperties`
    """
    if False:
        def __getattr__(self, name):
            try:
                if len(self) > 0 and self[0] is not None:
                    return ListWithProperties([getattr(o, name) for o in self])
            except AttributeError:
                return super().__getattribute__(name)

    def values(self):
        return self

    def items(self):
        return enumerate(self)

    def __deepcopy__(self, memodict={}):
        return ListWithProperties([deepcopy(o, memodict) for o in self])

    def __getstate__(self): return self.__dict__
    def __setstate__(self, d): self.__dict__.update(d)

class DictWithProperties(UserDict):
    """
    This dict is designed to only take objects of the same class. It enables the direct access to attributes of
    the objects in the dict as a list of the attributes, where the position of the attributes corresponds to the
    position of the object in the dict. It also propagets the `cut_to_timespan` directive, that cuts all objects in
    the dict to the specified timespan.
    """

    def __deepcopy__(self, memodict={}):
        return DictWithProperties({k: deepcopy(v, memodict) for k, v in self.items()})

    def cut_to_timespan(self, birth: int, death: int):
        """
        cuts all objects that themself support `cut_to_timespan` to their timespans defined by birth and death.
        """
        for k in list(self.keys()):
            if hasattr(self[k], 'in_timespan') and callable(self[k].in_timespan) and not self[k].in_timespan(birth,
                                                                                                             death, ):
                del self[k]
            elif hasattr(self[k], 'in_timespan'):
                self[k].cut_to_timespan(birth, death)

    def to_hdf5(self, group: Group):
        for idx, o in self.items():
            ig = group.create_group(str(idx))
            o.to_hdf5(ig)

    def __getstate__(self): return self.__dict__
    def __setstate__(self, d): self.__dict__.update(d)


class ReferenceDict(DictWithProperties):
    """
    `ReferenceDict` is a dict and handles the referencing to objects of type `object_class`. The keys are the identifiers
    of the referenced object (the reference). When the `resolve` function is called, the values of the keys get assigned
    the pointer to the object. The object has to implement the function `resolve_func`. The resolving is done only when
    `resolve` is called and is for the remaining period static. It does not automatically register chaning of identifiers.
    """

    def __init__(self, ids, object_class: InputClassBase):
        super().__init__()
        self.object_class = object_class
        for i in ids:
            if isinstance(i, np.ndarray):
                i = tuple(i)
            elif not isinstance(i, tuple):
                i = int(i)
            self.data[i] = None

    def resolve(self, input_recording):
        """
        finds the corresponding objects to the identifiers (keys of dict) and sets them as value. If no object could
        be found an `ReferenceNotResolvable` is raised.
        """
        for k in self.keys():
            self[k] = self.object_class.resolve_func(input_recording, k)
            
        
            

    def __deepcopy__(self, memodict={}):
        return ReferenceDict(list(self.keys()), self.object_class)

    def reset(self):
        for k in self.keys():
            self[k] = None

    def __getitem__(self, item):
        res = super().__getitem__(self, key=item)
        if res is None:
            raise ReferenceNotResolved(self.__class__)
        else:
            return res

    @property
    def is_resolved(self):
        return np.all(o is not None for o in self.values())

    @property
    def reference(self):
        return np.array(list(self.data.keys()))


class ReferenceElement():
    """
    `ReferenceElement` is the analog of `ReferenceDict` in cases only exactly one object should be referenced.
    """
    
    object_class: Any
    reference: Any
    

    def __init__(self, id: int, object_class: InputClassBase):
        self.object_class = object_class
        self.reference = id
        self._value = None

    def resolve(self, input_recording):
        """
        finds the corresponding object to the identifier `reference` and sets the pointer as `value`. If no object could
        be found an `ReferenceNotResolvable` is raised.
        """
        if np.all(self.reference == -1) or (isinstance(self.reference, str) and self.reference.endswith('-1')):
            self._value = None
        else:
            self._value = self.object_class.resolve_func(input_recording, self.reference)

    def __deepcopy__(self, memodict={}):
        return ReferenceElement(self.reference, self.object_class)

    def reset(self):
        self._value = None

    @property
    def is_resolved(self):
        return self._value is not None

    @property
    def value(self):
        if np.all(self.reference == -1):
            return None
        elif self.is_resolved:
            return self._value
        else:
            raise ReferenceNotResolved(self.__class__)


class ReferenceNotResolvable(ValueError):
    def __init__(self, cls, id):
        super().__init__(f'The Reference could not be resolved. Object of class={cls.__name__} with id={id} not found.')


class ReferenceNotResolved(Exception):
    def __init__(self, from_cls):
        super().__init__(f'The reference you are trying to access is not resolved. Call `resolve` on the {from_cls.__name__} object.')


def raise_not_resolved(resolve_func):
    """
    Only use on overrides of `resolve_func` of `InputClassBase` classes. It add more meaningful error messages when the reference can not be resolved.
    """
    def wrap(cls, snip, id):
        try:
            return resolve_func(cls, snip, id)
        except KeyError as e:
            raise ReferenceNotResolvable(cls, id) from e
        except TypeError as e:
            raise ReferenceNotResolvable(cls, id) from e
    return wrap
