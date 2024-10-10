class ObjectBorders:

    def __init__(self):
        self.borders = []


class ObjectBorder:

    def __init__(self, width = None, type = None, outline_id = None):
        self.width = width
        self.type = type
        self.outline_id = outline_id
        self.use_complete_outline = None
        self.corner_reference = []
