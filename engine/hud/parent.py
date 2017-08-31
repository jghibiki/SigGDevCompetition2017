
class ParentScreen:
    def __init__(self, children=[]):
        self.children = children

    def add_child(self, child):
        if child not in self.children: self.children.append(child)

    def rm_child(self, child):
        if child in self.children:
            for c in self.children:
                if c == child:
                    self.children.remove(c)
                    return

    def state(self, name):
        return self.parent.state(name)

