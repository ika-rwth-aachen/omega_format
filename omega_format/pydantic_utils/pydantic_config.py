from functools import cached_property

class PydanticConfig:
    arbitrary_types_allowed = True
    keep_untouched = (cached_property, )
