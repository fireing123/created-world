from pygameHelper import *

from components.hitObject                       import HitComponent, DamageEffect
from components.inventory                       import ItemIndex

from objects.bossAttakers import (
    BossArms,
    BossArrow,
    BossMiniArms,
    BossWall,
    FollowArrow,
    RotatingArm
)

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player                         import Player
    from objects.followCamera                   import FollowCamera
    from objects.UI.worldVoiceUI                import WorldVoice
    from objects.night                          import Night

class FakeRealBoss(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.head = ImageObject(self)
        self.components.append(self.head)

        self.animation = Animation(float('inf'), self.head, sheet="fakeEyes")
        self.components.append(self.animation)

        self.animation.change_image()

        self.body = FakeBossBody(name)
        self.body.init_instantiate()

        self.mini_arm = BossMiniArms(self.body, "./resource/boss/fake/punch.png", (4.17, 8.3))
        self.childrens.append(self.mini_arm)

        self.arm = BossArms(name, self.body, "./resource/boss/fake/punch.png", (8.3, 8.3))
        self.childrens.append(self.arm)

        self.wall = BossWall([0, 10000], name)
        self.childrens.append(self.wall)

        self.follow_arrow = FollowArrow(self.body, "./resource/boss/fake/punch.png", (8.3, 4.17))
        self.childrens.append(self.follow_arrow)
        
        self.rotating_arm = RotatingArm(self.body, "./resource/boss/fake/punch.png", (8.3, 8.3))
        self.childrens.append(self.rotating_arm)

        self.page_wait = TimerTask(98000)

        self.warning_wait = OnceTimerTask(2000)
        self.warning_index = 0

        self.is_mini_wave = False
        self.mini_wait = TimerTask(1000)

        self.is_arm_wave = False
        self.arm_wait = OnceTimerTask(600)
        self.arm_attack_wait = OnceTimerTask(400)

        self.is_arrow_wave = False
        self.arrow_wait = TimerTask(500)
        self.arrow_rotate = 0

        self.is_follow_wave = False
        self.follow_wait = TimerTask(1000)
        self.not_yet = True

    def delete(self):
        self.mini_arm.delete()
        self.arm.delete()
        self.wall.delete()
        self.follow_arrow.delete()
        self.rotating_arm.delete()
        return super().delete()

    def mini_attack(self):
        if self.mini_wait.run_periodic_task():
            self.mini_arm.mini_attack()

    def arm_attack(self):
        if self.arm_wait.run_periodic_task():
            self.arm.warning(Vector(random.random()*1000-500, 246))
            self.arm_attack_wait.reset()

        if self.arm_attack_wait.run_periodic_task():
            if not self.arm.location.visible:
                self.arm.location.visible = True
            self.arm_wait.reset()
            self.arm.attack(self.arm.warning_obj.location.position)
    
    def arrow_attack(self):
        if self.arrow_wait.run_periodic_task():
            vector = Vector(0, 15)
            vector = vector.rotate(self.arrow_rotate)
            self.arrow_rotate += 5
            if self.arrow_rotate >= 45:
                self.arrow_rotate = -45
            arrow = BossArrow([2400, 1400], vector, self.body, "./resource/boss/fake/punch.png", (2.085, 4.17))
            arrow.instantiate()

    def follow_attack(self):
        if self.follow_wait.run_periodic_task():
            self.follow_arrow.attack()

    def start_boss(self):
        c: 'FollowCamera' = Manger.scene.camera
        self.night.change_time(0)
        c.change_sound("start_boss")
        if not self.night.is_running:
            self.not_yet = True
        else:
            self.night.is_running = False
        self.location.position = [2400, 1250]
        self.wall.location.position = (-580, -120)
        self.location.visible = True
        self.page_wait.tick = 10000

    def start(self):
        self.night: 'Night' = Manger.scene.get_object("night")
        self.close()

    def update(self):
        if self.location.visible:
            if self.page_wait.run_periodic_task():
                self.warning_wait.reset()
                self.warning_index = random.choice(range(5))
                self.animation.pointToIndex(self.warning_index)

            if self.warning_wait.run_periodic_task():
                self.page(self.warning_index)

        if self.is_mini_wave:
            self.mini_attack()
            if not self.mini_arm.location.visible:
                self.mini_arm.location.visible = True
        else:
            if self.mini_arm.location.visible:
                self.mini_arm.location.visible = False

        if self.is_arm_wave:
            self.arm_attack()
        else:
            if self.arm.location.visible:
                self.arm.location.visible = False

        if self.is_arrow_wave:
            self.arrow_attack()

        if self.is_follow_wave:
            self.follow_attack()
            if not self.follow_arrow.location.visible:
                self.follow_arrow.location.visible = True
        else:
            if self.follow_arrow.location.visible:
                self.follow_arrow.location.visible = False

    def random_page(self):
        self.page(random.choice(range(5)))

    def close(self):
        self.is_arm_wave = False
        self.is_mini_wave = False
        self.is_arm_wave = False
        self.is_arrow_wave = False
        self.is_follow_wave = False
        self.rotating_arm.end()

    def end(self):
        self.close()
        if not self.not_yet:
            self.night.is_running = True
        self.location.position = [0, 10300]
        self.wall.location.position = [0, 10300]
        self.location.visible = False

    def page(self, index):
        self.close()
        match index:
            case 0:
                self.is_follow_wave = True
            case 1:
                self.is_arrow_wave = True
            case 2:
                self.is_mini_wave = True
            case 3:
                self.is_arm_wave = True
            case 4:
                self.rotating_arm.attack()

class FakeBossBody(GameObject):
    def __init__(self, parent_name):
        super().__init__(parent_name+"_body", 2, "living", True, [0, -100], 0, parent_name)
        self.image = ImageObject(self, value=Manger.surface_sheet["fboss"].images[0])
        self.components.append(self.image)

        self.rect = Rect(0, 0, 400, 400)
        self.heath = 1000

        self.hit_checker = HitComponent(self, self.rect)
        self.components.append(self.hit_checker)

        self.invincibility = TimerTask(100)
        
        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.hit_checker.hit_event.add_lisner(self.hit)

    def start(self):
        self.rect.center = self.location.world_position
        self.world_1: 'WorldVoice' = Manger.scene.get_object("world_1")
        self.player: 'Player' = Manger.scene.get_object("player")
        self.panelc = Manger.scene.get_object("d")
        self.altar_ui = Manger.scene.get_object("altar_ui")
        self.player.die_event.add_lisner(self.reset)

    def reset(self):
        self.heath = 1000
        boss: 'FakeRealBoss' = self.location.parent.object
        boss.page_wait.tick = float('inf')
        boss.end()

    def update(self):
        self.rect.center = self.location.world_position

    def hit(self, hiter, status, power):
        if self.invincibility.run_periodic_task():
            self.damage_effect.reset()
            match status:
                case ItemIndex.SWORD:
                    self.heath -= power
                case _:
                    self.heath -= power * 0.7
            if self.heath < 0:
                boss: 'FakeRealBoss' = self.location.parent.object
                boss.page_wait.tick = float('inf')
                boss.close()
                self.panelc.location.visible = True
                c: 'FollowCamera' = Manger.scene.camera
                c.change_sound("clear_boss")
                self.altar_ui.location.visible = True
                def end_world():
                    c.sound_manager.mixer_stop()
                    Game.stop("fake")
                self.world_1.talk_start("boss_die", end_world)
                self.location.parent.object.delete()
                self.player.delete()
                