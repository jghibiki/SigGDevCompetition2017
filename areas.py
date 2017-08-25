
class Area:
    def __init__(self, coordinates, name):
        self.coordinates = coordinates
        self.name = name


class MeetingArea(Area):
    instance = None
    def __init__(self, coordinates, name="Meeting Area"):
        Area.__init__(self, coordinates, name)
        MeetingArea.instance = self

Areas = [

#    MeetingArea([ (x, y) for x in range(10) for y in range(10) ])

]

