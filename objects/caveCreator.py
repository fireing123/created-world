from pygameHelper import (
    GameObject, 
    Rect, 
    TimerTask, 
    OnceTimerTask
)

from objects.zombie     import Zombie
from objects.alotabones import Bones
from objects.slime      import Sime

class CaveCreator(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, rect: Rect, monster_type, monster_count):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.max_count = monster_count
        self.monster_type = monster_type

        self.rect = Rect(0, 0, *rect)

        self.spawn_wait = TimerTask(15000)

        self.index = 0

        self.monsters: dict[GameObject, OnceTimerTask] = {}

    @property
    def uuid(self):
        self.index += 1
        return self.index

    def get_attribute(self):
        return self.name + f'_{self.uuid}', self.layer, "notliving", True, self.location.world_position, 0, "parent"

    def start(self):
        self.rect.center = self.location.world_position

    def update(self):
        if len(self.monsters) == 0:
            if self.spawn_wait.run_periodic_task():
                for i in range(self.max_count):
                    par = self.get_attribute()
                    match self.monster_type:
                        case "bone":
                            monster = Bones(*par)
                        case "zombie":
                            monster = Zombie(*par)
                        case "slime":
                            monster = Sime(*par)
                    monster.instantiate()
                    once = OnceTimerTask(5000)
                    once.once = True
                    once.last_update -= once.tick
                    self.monsters[monster] = once
                    def on_death():
                        try:
                            self.spawn_wait.reset()
                            self.monsters.pop(monster)
                        except: pass
                    monster.die_event.add_lisner(on_death)

        for monster, task in self.monsters.items():
            if task.once:
                if not self.rect.collidepoint(monster.location.world_position):
                    task.reset()
            
            if task.run_periodic_task():
                monster.location.position = self.location.world_position