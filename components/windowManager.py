from pygameHelper import Component, GameObject, Event, on_reset
from typing import Dict

windows: Dict[str, 'WindowManager'] = {}

def reset():
    windows.clear()

on_reset.add_lisner(reset)

class WindowManager(Component):
    """UI 화면 전환 틀"""
    def __init__(self, object: GameObject, key: str):
        self.object = object
        self.on_open = Event()
        self.on_close = Event()
        windows[key] = self