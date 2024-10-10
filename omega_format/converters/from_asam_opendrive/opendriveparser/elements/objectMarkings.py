class ObjectMarkings:

    def __init__(self):
        self.marking = []


class ObjectMarking:

    def __init__(self, side = None, weight = None, color = None, space_length = None,
                 line_length = None, start_offset = None, stop_offset = None):
        self.side = side
        self.weight = weight
        self.width = None
        self.color = color
        self.z_offset = None
        self.space_length = space_length
        self.line_length = line_length
        self.start_offset = start_offset
        self.stop_offset = stop_offset
        self.corner_reference = []


class MarkingCornerReference:

    def __init__(self, id = None):
        self.id = id
