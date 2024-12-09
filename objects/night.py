from pygameHelper import (
    GameObject, 
    Manger, 
    Surface, 
    TimerTask,
    Event
)

import pygame

day_color = (6, 108, 240)
night_color = (0, 2, 74)

class Night(GameObject):
    def __init__(self, visible):
        super().__init__("night", 4, "night", visible, [0, 0], 0, "parent")

        self.is_running = False

        self.sun = Surface((Manger.WIDTH, Manger.HEIGHT), pygame.SRCALPHA)
        self.sun.fill((0,0,0, 128))

        self.waiter = TimerTask(100000)
        self.on_changed_time = Event()
        self.__time = 0

    def update(self):
        if self.is_running:
            if self.waiter.run_periodic_task():
                if self.__time == 0:
                    self.change_time(1)
                else:
                    self.change_time(0)

    def get_time(self):
        return self.__time

    def start(self):
        self.change_time(0)

    def render(self, surface: Surface, camera):
        surface.blit(self.sun, (0, 0))

    def change_time(self, time):
        self.__time = time
        if time == 0:
            self.location.visible = False
            Manger.scene.camera.cam_color = day_color
        elif time == 1:
            self.location.visible = True
            Manger.scene.camera.cam_color = night_color
        self.on_changed_time.invoke(time)