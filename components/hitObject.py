from pygameHelper import (
    Component, 
    event, 
    GameObject, 
    Rect, 
    ImageObject,
    TimerTask,
    on_reset
)

from typing import List, Optional

hit_objects: List[Optional['HitComponent']] = []
attack_objects: List[Optional['Attacker']] = []

def reset():
    hit_objects.clear()
    attack_objects.clear()

on_reset.add_lisner(reset)

class HitComponent(Component):
    """타격점"""
    def __init__(self, object: GameObject, rect: Rect, **kwargs):
        self.object: GameObject = object
        hit_objects.append(self)
        self.hit_event = event.Event()
        self.rect = rect
        self.type = kwargs.get('type', None)

    def delete(self):
        try:
            self.object.components.remove(self)
            hit_objects.remove(self)
        except: pass

class Attacker(Component):
    """공격자"""
    def __init__(self, object: GameObject, rect: Rect, **kwargs):
        self.object: GameObject = object
        attack_objects.append(self)
        self.hit_event = event.Event()
        self.rect = rect
        self.type = None
        self.except_object = kwargs.get('except_object', None)

    def hit_check(self, status, hit_power, ignore_tag=None) -> List['HitComponent']:
        hit: List['HitComponent'] = []
        for hit_object in hit_objects:
            if hit_object.object == self.object: continue
            if hit_object.object == self.except_object: continue
            if hit_object.type != None: continue
            if ignore_tag != None:
                if hit_object.object.tag == ignore_tag: continue
            if self.rect.colliderect(hit_object.rect):
                hit_object.hit_event.invoke(self, status, hit_power)
                hit.append(hit_object)
        return hit
    
    def delete(self):
        try:
            self.object.components.remove(self)
            attack_objects.remove(self)
        except: pass

class DamageEffect(Component):
    """빨간색 이펙트"""
    def __init__(self, image: ImageObject):
        self.image = image
        self.invincibility_visible = TimerTask(300)

    def update(self):
        if self.invincibility_visible.not_update_run():
            self.image.set_cellophane(False)
        else:
            self.image.set_cellophane(True)

    def reset(self):
        self.invincibility_visible.reset()