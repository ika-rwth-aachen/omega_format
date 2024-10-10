class Signals:

    def __init__(self):
        self.signal = []
        self.signal_reference = []


class Signal:

    def __init__(self):
        self.s = None
        self.t = None
        self.id = None
        self.name = None
        self.dynamic = None
        self.orientation = None
        self.z_offset = None
        self.country = None
        self.country_revision = None
        self.type = None
        self.subtype = None
        self.value = None
        self.unit = None
        self.height = None
        self.width = None
        self.text = None
        self.h_offset = None
        self.pitch = None
        self.roll = None
        self.physical_position = None
        self.reference = []
        self.dependency = []
        self.validity = []
