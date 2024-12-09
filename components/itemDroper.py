from pygameHelper import Component, GameObject, Vector
from objects.dropedItem import DropedItem
from components.itemInfo import ItemInfo
import random

class ItemDroper(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

    def drop_item(self, info: ItemInfo, **kwargs):
        if info.is_zero(): return
        droped_item = DropedItem(self.object.name+"_droped", self.object.location.world_position, info.index, info.count, info.durability)
        droped_item.instantiate()
        if "pos" in kwargs:
            droped_item.location.position += kwargs["pos"]
        if "rand" in kwargs:
            droped_item.physics.add_force(Vector((random.random()-0.5)*8, 5))
        return droped_item