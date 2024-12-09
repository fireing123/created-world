from pygameHelper.objects.object import Object
from pygameHelper.location import Parent

class ParentObject(Object):
    def __init__(self):
        super().__init__("parent", 0, "top")
        self.visible = False
        self.location = Parent(self)
        
    def set_parent(self):
        pass