from pygameHelper import *

from pygameHelper.objects.components.physics    import physics_grounds
from components.hitObject                       import Attacker
from components.inventory                       import ItemIndex

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player                         import Player
    from objects.followCamera                   import FollowCamera

class BossMiniArms(GameObject):
    def __init__(self, body, path, size):
        super().__init__("arm", 2, "arm", False, [0, 0], 0, "parent")
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)

        self.is_attacking = False
        self.wait = TimerTask(400)
        self.rect = Rect(0, 0, 100, 200)
        
        self.attacker = Attacker(self, self.rect, except_object=body)
        self.components.append(self.attacker) 

        self.sound = SoundSource(self, "./resource/sound/boss/damage1.wav", 0, lambda dist: 0.3)

    def start(self):
        self.player: 'Player' = Manger.scene.get_object("player")
  
    def mini_attack(self):
        pos = Vector(self.player.location.world_position.x, 1412)
        self.location.position = pos
        self.is_attacking = True
        self.attacker.type = True
        self.wait.reset()

    def update(self):
        if self.is_attacking:
            self.location.translate(Vector(0, -14))
            self.rect.center = self.location.world_position

            if self.wait.run_periodic_task():
                self.sound.play()
                self.attacker.type = None
                self.is_attacking = False

            if self.attacker.type != True:
                self.attacker.type = None
                return 
            
            hits = self.attacker.hit_check(100, 20)

            if hits:
                self.attacker.type = None

class BossArms(GameObject):
    def __init__(self, parent_name, body, path, size):
        super().__init__(parent_name+"_arm", 2, "arm", False, [0, 0], 0, parent_name)
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)
        self.is_attacking = False
        self.wait = TimerTask(800)
        self.rect = Rect(0, 0, 100, 200)
        self.attacker = Attacker(self, self.rect, except_object=body)
        self.components.append(self.attacker) 

        self.warning_obj = Warning("warning_arm", 2, "ui", True, [0, 0], 0, parent_name)
        self.childrens.append(self.warning_obj)

        self.sound = SoundSource(self, "./resource/sound/boss/damage1.wav", 0, lambda dist: 0.6)

    def attack(self, pos):
        self.location.position = pos
        self.is_attacking = True
        self.attacker.type = True
        self.wait.reset()

    def warning(self, pos):
        self.warning_obj.warning(pos)

    def update(self):
        if self.is_attacking:
            self.location.translate(Vector(0, -10))
            self.rect.center = self.location.world_position

            if self.wait.run_periodic_task():
                self.attacker.type = None
                self.sound.play()
                self.is_attacking = False

            if self.attacker.type != True:
                self.attacker.type = None
                return 
            
            hits = self.attacker.hit_check(100, 20, "boss")

            if hits:
                self.attacker.type = None

class Warning(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, surface=(200, 1200))
        self.components.append(self.image)
        self.image.og_image.fill((227, 15, 0, 120))
        self.warinng_wait = OnceTimerTask(200)

    def update(self):
        if self.warinng_wait.run_periodic_task():
            self.location.visible = False

    def warning(self, pos):
        self.location.position = pos
        self.location.visible = True
        self.warinng_wait.reset()

class BossArrow(GameObject):
    def __init__(self, position, velocity, body, path, size):
        super().__init__("arm_arrow", 3, "arrow", True, position, 0, "parent")
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)

        self.rect = Rect(0, 0, 30, 50)

        self.physics = Physics(self, Rect(0, 0, 30, 50))
        self.physics.collision_enter_event.add_lisner(self.collision_enter)
        self.physics.air_friction = 0.001
        self.components.append(self.physics)

        self.attacker = Attacker(self, self.rect, except_object=body)
        self.components.append(self.attacker)

        self.physics.velocity = Vector(velocity)

    def update(self):
        self.location.translate(self.velocity)

    def collision_enter(self, collision, collision_type):
        self.delete()

    def update(self):
        self.rect.center = self.location.world_position

        hits = self.attacker.hit_check(ItemIndex.ARROW, 20)

        for hit_object in hits:
            if hit_object.object.tag == "living":
                try:
                    self.delete()
                except: pass
                break

class BossWall(GameObject):
    def __init__(self, position, parent_name):
        super().__init__(parent_name+"_wall", 2, "wall", True, position, 0, parent_name)
        self.image = ImageObject(self, surface=(16, 512))
        self.components.append(self.image)

        self.rect = Rect(0, 0, 16, 512)

    def update(self):
        self.rect.center = self.location.world_position

    def start(self):
        physics_grounds.append(self.rect)

    def delete(self):
        try:
            physics_grounds.remove(self.rect)
        except:pass
        return super().delete()
        
class FollowArrow(GameObject):
    def __init__(self, body, path, size):
        super().__init__("follow_arrow", 2, "arrow", False, [2000, 1000], 0, "parent")
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)

        self.rect = Rect(0, 0, 100, 200)

        self.attacker = Attacker(self, self.rect, except_object=body)
        self.components.append(self.attacker)

        self.is_attacking = False
        self.wait = TimerTask(500)
        self.speed = 4

    def attack(self):
        pos = self.player.location.world_position - self.location.position
        pos.normalize_ip()
        pos *= 150
        self.pos = self.location.position + pos 
        self.is_attacking = True
        self.attacker.type = True
        self.wait.reset()

    def update(self):
        if self.is_attacking:
            self.location.position = self.location.position.lerp(self.pos, min(1, Manger.delta_time * self.speed))
            self.rect.center = self.location.world_position

            if self.wait.run_periodic_task():
                self.attacker.type = None
                self.is_attacking = False

            if self.attacker.type != True:
                self.attacker.type = None
                return 
            
            hits = self.attacker.hit_check(100, 10)

            if hits:
                self.attacker.type = None
        else:
            vel = self.player.location.world_position - self.location.world_position
            if vel != Vector(0, 0):
                vel.normalize_ip()
                self.location.rotation = Vector(0, 0).angle_to(vel)

    def start(self):
        self.player = Manger.scene.get_object("player")

class RotatingArm(GameObject):
    def __init__(self, body, path, size):
        super().__init__("rotating_arm", 2, "arm", False, [2400, 1200], 0, "parent")
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)

        self.is_attacking = False
        self.wait = TimerTask(500)
        self.rect = Rect(0, 0, 100, 200)
        self.attacker = Attacker(self, self.rect, except_object=body)
        self.components.append(self.attacker) 

        self.cam: 'FollowCamera' = Manger.scene.camera
        self.sound = SoundSource(self, "./resource/sound/boss/damage1.wav", 0, lambda dist: 0.6)
        self.velocity = Vector(3, 3)

    def attack(self):
        self.is_attacking = True
        self.attacker.type = True
        self.location.visible = True

    def end(self):
        self.is_attacking = False
        self.attacker.type = False
        self.location.visible = False

    def update(self):
        if self.is_attacking:
            self.location.translate(self.velocity)
            self.location.rotation += 5
            self.rect.center = self.location.world_position

            #render pos
            visible_pos = self.cam(self.render_position)
            visible_rect = self.rect.copy()
            visible_rect.center = visible_pos
            if visible_rect.top < 0 or visible_rect.bottom > Manger.HEIGHT:
                self.velocity.y *= -1
                self.sound.play()
                self.attacker.type = True
            if visible_rect.left < 0 or visible_rect.right > Manger.WIDTH:
                self.velocity.x *= -1
                self.sound.play()
                self.attacker.type = True
            #render pos

            if self.wait.not_update_run():
                if self.attacker.type != True:
                    self.attacker.type = None
                    return

                hits = self.attacker.hit_check(100, 20)

                if hits:
                    self.wait.reset()
                    self.attacker.type = None