from pygameHelper import Component, GameObject, Rect, on_reset
from pygameHelper.event import Event
from typing import List

class Trigger(Component):
    """플레이어가 상호작용 할수있는"""
    def __init__(self, object: GameObject, width, height, key, **kwargs) -> None:
        self.object = object
        self.rect = Rect(0, 0, width, height)
        self.key = key
        self.type = kwargs.get("type", 0)
        self.rect.center = self.object.location.world_position
        self.on_interaction =  Event()
        trigger_object.append(self)

    def update(self):
        self.rect.center = self.object.location.world_position

    def delete(self):
        try:
            trigger_object.remove(self)
        except: pass

trigger_object: List[Trigger] = []

def reset():
    trigger_object.clear()

on_reset.add_lisner(reset)