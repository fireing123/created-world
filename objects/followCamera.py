from pygameHelper import *

from pygame import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.night import Night

class FollowCamera(CameraObject):
    def __init__(self, name, tag, visible, position, rotation, parent_name, maps, speed):
        super().__init__(name, tag, visible, position, rotation, parent_name)
        self.speed = speed
        self.maps: dict[str, Map] = {}        
        for map in maps:
            self.maps[map[0]] = Map(*map)

        self.map: Map = None
        self.changed_wait = TimerTask(2200)
        self.changed_wait.last_update = -2300

        self.changed_name = None

        self.once = {
            "timer": True
        }

        self.sound_manager = SoundManager({
            "error_world" : SoundSource(self, "./resource/sound/bgm/배달의민족 - 복귀해도 될까요.wav",       0, lambda dist: 0.1, "endPlay"),
            "world" :       SoundSource(self, "./resource/sound/bgm/배달의민족 - 충전할 땐 클래식을.wav",    0, lambda dist: 0.1, "endPlay"),
            "clear_boss" :  SoundSource(self, "./resource/sound/bgm/endBoss.wav",                           0, lambda dist: 0.3, "endPlay"),
            "cave" :        SoundSource(self, "./resource/sound/bgm/in_a_cave.wav",                         0, lambda dist: 0.2, "endPlay"),
            "start_boss" :  SoundSource(self, "./resource/sound/bgm/startBoss.wav",                         0, lambda dist: 0.3, "endPlay"),
            "out":          SoundSource(self, "./resource/sound/bgm/ending_of_the_world1.wav",              0, lambda dist: 0.1, "endPlay"),
            "death":        SoundSource(self, "./resource/sound/bgm/shock1.wav",                            0, lambda dist: 1,   "endPlay"),
            "night":        SoundSource(self, "./resource/sound/bgm/night.wav",                             0, lambda dist: 0.1, "endPlay")
        })

        self.end_event = None
        self.map_stop = False
    
    def change_sound(self, name, end_event=None):
        if name != None:
            if self.changed_name != name:
                self.sound_manager.play(name, loops=-1)
        else:
            self.sound_manager.mixer_stop()
            
        if self.end_event != None:
            self.end_event()
        self.end_event = end_event
        self.changed_name = name

    def on_time_changed(self, time):
        self.change_event(self.map)

    def move(self):
        for k, hidden in self.maps.items():
            if hidden.rect.collidepoint(self.player_location.world_position):
                if self.map != hidden:
                    self.map = hidden
                    return hidden
                break

    def change_event(self, map: 'Map'):
        if map != None:
            match map.name:
                case "ground":
                    if self.night.get_time() == 0:
                        self.change_sound("world")
                    else:
                        self.change_sound("night")
                case "cave" | "big_cave":
                    self.change_sound("cave")
                case "error" | "jump" | "boss":
                    if self.night.get_time() == 0:
                        self.change_sound("error_world")
                    else:
                        self.change_sound(None)
                case "timer":
                    self.change_sound("out")
                    if self.once["timer"]:
                        self.world.talk_start("night_world")
                        self.night.is_running = True
                        self.once["timer"] = False
            self.changed_wait.reset()

    def start(self):
        player = Manger.scene.get_object("player")
        self.world = Manger.scene.get_object("world_1")
        self.night: 'Night' = Manger.scene.get_object("night")
        self.night.on_changed_time.add_lisner(self.on_time_changed)
        self.player_location: Location = player.location

    def update(self):
        if not self.map_stop:
            map = self.move()
            self.change_event(map)

        if self.changed_wait.not_update_run():
            self.location.position = self.location.position.lerp(self.player_location.position, min(1, Manger.delta_time * self.speed)).floor_vector()

        lx = (self.map.size.x - Manger.WIDTH) // 2
        clampX = math.clamp(self.location.position.x, self.map.center.x - lx, self.map.center.x + lx)

        ly = (self.map.size.y - Manger.HEIGHT) // 2
        clampY = math.clamp(self.location.position.y, -ly + self.map.center.y, ly + self.map.center.y)

        if not self.changed_wait.not_update_run():
            self.location.position = self.location.position.lerp(
                Vector(clampX, clampY),
                min(1, Manger.delta_time * self.speed)
            ).floor_vector()
        else:
            self.location.position = Vector(clampX, clampY)


class Map:
    def __init__(self, name, center, size) -> None:
        self.name = name
        self.center = Vector(center)
        self.size = Vector(size)
        self.rect = Rect(0, 0, size[0], size[1])
        self.rect.center = center

    def __str__(self):
        return f"name: {self.name}\ncenter: {self.center}\nsize: {self.size}"