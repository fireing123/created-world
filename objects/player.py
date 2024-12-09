from pygameHelper                   import *
from pygameHelper                   import mouse

from components.inventory           import ItemIndex, is_foods
from components.trigger             import trigger_object
from components.tile                import is_grass_type, is_stone_type, is_dirt_type
from components.hitObject           import Attacker, DamageEffect
from components.itemDroper          import ItemDroper

from components.weapon.sword        import Sword
from components.weapon.axe          import Axe
from components.weapon.pickaxe      import Pickaxe
from components.weapon.pickaxeIron  import PickaxeIron
from components.weapon.punch        import Punch
from components.weapon.bow          import Bow

from objects.followCamera           import FollowCamera
from objects.livingObject           import LivingObject
from objects.nomalParticle          import PixelParticle

from pygame.surface                 import Surface as Surface

import random
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.wing               import Wing
    from objects.UI.InventoryUI     import InventoryWindow
    from objects.UI.hotbar          import HotBar
    from objects.tileCollision      import CollisionTile
    from objects.UI.worldVoiceUI    import WorldVoice
    from objects.realboss           import RealBoss
    from objects.fakeboss           import FakeRealBoss

import pygame

class Player(LivingObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 100, Rect(0, 0, 32, 64))
        self.save_point = Vector(position)
        
        self.die_event.add_lisner(self.on_death_event)
        self.hit_checker.hit_event.add_lisner(self.hit)
        
        self.physics.collision_enter_event.add_lisner(self.on_collision_stay)
        self.feet_type = None

        self.image = ImageObject(self)
        self.components.append(self.image)

        bow_walk_animation =        Animation(60,           self.image, sheet='playerBowWalk')
        bow_idle_animation =        Animation(float('inf'), self.image, sheet='playerBowWalkIdle')
        walk_animation =            Animation(40,           self.image, sheet="playerWalk")
        running_animation =         Animation(40,           self.image, sheet="playerRunning")
        idle_animation =            Animation(1000,         self.image, sheet="playerIdle")
        punch1_animation =          Animation(float('inf'), self.image, sheet="playerPunch1")
        punch2_animation =          Animation(float('inf'), self.image, sheet="playerPunch2")
        sword1_animation =          Animation(40,           self.image, sheet="playerSword1",       once=True)
        sword2_animation =          Animation(40,           self.image, sheet="playerSword2",       once=True)
        pickaxe_animation =         Animation(50,           self.image, sheet="playerPickaxe",      once=True)
        pickaxe_iron_animation =    Animation(50,           self.image, sheet="playerPickaxeIron",  once=True)
        axe_animation =             Animation(100,          self.image, sheet="playerAxe",          once=True)
        axe_end_animation =         Animation(50,           self.image, sheet="playerAxeEnd",       once=True)
        jump_animation =            Animation(float('inf'), self.image, sheet="playerJump")
        player_bow_jump_animation = Animation(float('inf'), self.image, sheet="playerBowJump")
        idle_animation.change_image()

        self.animation_manager = AnimationManager(self, {
            "walk":         walk_animation,
            "idle":         idle_animation,
            "trigger":      idle_animation,
            "auto":         idle_animation,
            "punch1":       punch1_animation,
            "punch2":       punch2_animation,
            "sword1":       sword1_animation,
            "sword2":       sword2_animation,
            "pickaxe":      pickaxe_animation,
            "pickaxeIron":  pickaxe_iron_animation,
            "axe":          axe_animation,
            "axeEnd":       axe_end_animation,
            "bowWalk":      bow_walk_animation,
            "bowIdle":      bow_idle_animation,
            "jump":         jump_animation,
            "running":      running_animation,
            "bowJump":      player_bow_jump_animation
        }, "idle")

        self.state = "idle"
        self.components.append(self.animation_manager)

        self.hunger = 100

        self.hunger_wait = TimerTask(6400)
        self.invincibility = TimerTask(100)
        
        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.bow_arm = BowArm(name+"_bow_arm", layer, "arm", True, [0, 7], 0, name)
        
        self.bow_item = Bow(self, self.bow_arm)
        self.components.append(self.bow_item)

        self.punch_item = Punch(self)
        self.components.append(self.punch_item)

        self.sword_item = Sword(self)
        self.components.append(self.sword_item)

        self.pickaxe_item = Pickaxe(self)
        self.components.append(self.pickaxe_item)

        self.pickaxe_iron_item = PickaxeIron(self)
        self.components.append(self.pickaxe_iron_item)

        self.axe_item = Axe(self)
        axe_animation.on_end.add_lisner(self.axe_item.axe_hit)
        axe_animation.on_end.add_lisner(lambda: self.change_animation("axeEnd"))
        self.components.append(self.axe_item)

        self.droper = ItemDroper(self)
        self.components.append(self.droper)

        self.sound_listener = SoundListener(self)

        self.sound_manager = SoundManager({
            "broken": SoundSource(self, "./resource/sound/broken/game_explosion6.wav", 0, lambda dist: 0.4),
            "eat": SoundSource(self, "./resource/sound/eat/eating.wav", 0, lambda dist: 0.5),
            "damage": SoundSource(self, "./resource/sound/player/damage2.wav", 0, lambda dist: 0.3)
        })

        self.walk_stone = []

        self.walk_wait = TimerTask(500)

        self.running_wait = TimerTask(250)
        self.running_effect_wait = TimerTask(160)

        self.ground_key = 0

        for i in [
            "./resource/sound/walk/stone/walk1.wav",
            "./resource/sound/walk/stone/walk2.wav",
            "./resource/sound/walk/stone/walk3.wav"
        ]:
            sound = SoundSource(self, i, 0, lambda dist: 0.6)
            self.walk_stone.append(sound)
            self.components.append(sound)

        self.walk_grass = []

        for i in [
            "./resource/sound/walk/grass/grassWalk1.wav",
            "./resource/sound/walk/grass/grassWalk2.wav"
        ]:
            sound = SoundSource(self, i, 0, lambda dist: 0.3)
            self.walk_grass.append(sound)
            self.components.append(sound)

        self.y_vel = 0

    def change_animation(self, state, **kwargs):
        self.state = state
        if "key" in kwargs:
            self.animation_manager.change_animation(kwargs["key"], kwargs.get("reset", False))
        else:
            self.animation_manager.change_animation(state, kwargs.get("reset", False))

    def start(self):
        super().start()
        self.bow_arm.instantiate()
        self.wing: 'Wing' =                 Manger.scene.get_object('playerWing')
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.tilemap: 'CollisionTile' =     Manger.scene.get_object("map_renderer")
        self.hotbar: 'HotBar' =             Manger.scene.get_object("hotbar")
        self.world_1: 'WorldVoice' =        Manger.scene.get_object("world_1")
        self.real_boss: 'RealBoss' =        Manger.scene.get_object("realboss")
        self.fake_boss: 'FakeRealBoss' =    Manger.scene.get_object("fakeboss")
        self.inventoryPanel = self.inventory.location.parent.object

        self.wing.ready_animation.on_end.add_lisner(self.wing_jump)

    def update(self):
        if self.physics.on_ground:
            if self.ground_key <= 1:
                self.ground_key = 2
            else:
                self.ground_key = 3
        else:
            if self.ground_key >= 2:
                self.ground_key = 1
            else:
                self.ground_key = 0

        if self.physics.velocity.y < -1:
            self.y_vel = self.physics.velocity.y

        self.rect.center = self.location.world_position
        if self.state in ["idle", "walk", "bowWalk", "bowIdle", "jump", "running", "bowJump"]:
            self.moving()

            if not self.physics.on_ground:
                self.change_animation('bowJump' if self.bow_arm.location.visible else 'jump')
            elif self.physics.on_ground and self.state in ["jump", "bowJump"]:
                self.change_animation('bowIdle' if self.bow_arm.location.visible else 'idle')
            
        if self.hunger_wait.run_periodic_task():
            if self.hunger > 0:
                self.hunger -= 2
                if self.heath != 100:
                    self.hp_add(6)
                    self.hunger -= 3
            else:
                self.hp_sub(3)

        if self.wing.animation_manager.state == "ready":
            self.physics.velocity.y += gravity

        if self.inventory.armor_slot.item.info.index == ItemIndex.WING:
            self.wing.location.visible = True
        else:
            self.wing.location.visible = False

        if self.physics.on_ground:
            self.wing.use = False

        if self.state != "auto": # 표지판이나 보스전언을 제외함
            for trigger in trigger_object:
                if trigger.rect.collidepoint(*self.location.world_position):
                    if trigger.type == 0 and Input.get_key_down(trigger.key):
                        trigger.on_interaction.invoke()
                    elif trigger.type == 1 and Input.get_mouse_down(trigger.key):
                        trigger.on_interaction.invoke()

            focus_slot = self.hotbar.get_focuse_slot()

            item_index = focus_slot.item.info.index

            if not self.inventoryPanel.location.world_visible:
                if Input.get_mouse_down(0):
                    match item_index: 
                        case ItemIndex.BOW:
                            self.bow_item.ready()
                        case ItemIndex.AXE:
                            self.axe_item.axe()

                        case ItemIndex.SWORD:
                            self.sword_item.sword()

                        case ItemIndex.PICKAXE:
                            self.pickaxe_item.pickaxe()

                        case ItemIndex.IRON_PICKAXE:
                            self.pickaxe_iron_item.pickaxe_iron()

                        case _:
                            self.punch_item.punch()
                elif Input.get_mouse_down(2):
                    if item_index in is_foods:
                        focus_slot.item.sub_item(1)
                        self.hunger_add(is_foods[item_index])
                        self.sound_manager.play('eat')

                if self.bow_arm.location.visible:
                    if Input.get_mouse(0):
                        self.bow_item.charge()
                
                    if Input.get_mouse_up(0):
                        self.bow_item.shot()
        
            if self.bow_arm.location.visible:
                if self.animation_manager.state == 'idle':
                    self.animation_manager.change_animation("bowIdle")
            else:
                if self.animation_manager.state == 'bowIdle':
                    self.animation_manager.change_animation("idle")

    def on_death_event(self):
        for y in self.inventory.data:
            for x in y:
                if not x.item.info.is_zero():
                    copy_info = x.item.info.copy()
                    x.item.clear()
                    self.droper.drop_item(copy_info, rand=True)
        for x in [self.inventory.armor_slot, self.inventory.boots_slot]:
            if not x.item.info.is_zero():
                    copy_info = x.item.info.copy()
                    x.item.clear()
                    self.droper.drop_item(copy_info, rand=True)
        
        self.location.position = self.save_point.copy()
        self.heath = self.max_heath
        self.hunger = 100
        c: 'FollowCamera' = Manger.scene.camera
        c.move()
        def event():
            c.change_event(c.map)
        c.change_sound('death')
        if self.real_boss.location.visible:
            self.world_1.talk_start("death_real_boss_world", event)
        elif self.fake_boss.location.visible:
            self.world_1.talk_start("death_boss_world", event)
        else:
            self.world_1.talk_start("death_world", event)

    def hit(self, hiter: Attacker, status, power):
        if self.invincibility.run_periodic_task():
            match status:
                case ItemIndex.SWORD:
                    self.hp_sub(int(power * 1))
                case _:
                    self.hp_sub(int(power * 0.6))

            self.knockback(hiter.object, Vector(3, 3))

    def wing_jump(self):
        self.physics.velocity.y = 15

    def on_collision_stay(self, collision: Rect, collision_type):
        if collision_type != 0: return

        nx = math.floor(collision.centerx / 48)
        ny = math.floor((collision.bottom + 24) / 48)
        
        self.feet_type = self.tilemap.get_tile((nx, ny))

        index = 2
    
        if self.feet_type in is_grass_type:
            index = 0
        elif self.feet_type in is_dirt_type:
            index = 1
        elif self.feet_type in is_stone_type:
            index = 2

        if self.ground_key == 2:
            if self.y_vel > -9.5:
                pass
            elif self.y_vel > -16.5:
                for i in range(3):
                    particle = PixelParticle("pice", self.physics.rect.midtop, Vector(6*(0.5-random.random()), 3), "pixelParticles", index)
                    particle.instantiate()
            else:
                for i in range(14):
                    particle = PixelParticle("pice", self.physics.rect.midtop, Vector(14*(0.5-random.random()), 3), "pixelParticles", index)
                    particle.instantiate()

    def hunger_add(self, value):
        self.hunger = min(self.hunger + value, 100)

    def hp_add(self, value):
        self.heath = min(self.heath + value, 100)

    def hp_sub(self, value):
        self.sound_manager.play("damage")
        self.damage_effect.reset()
        if self.inventory.armor_slot.item.info.index == ItemIndex.BREASTPLATE:
            self.heath = self.heath - (value * 0.7)
        else:
            self.heath = self.heath - value
        
        if self.heath <= 0:
            self.die_event.invoke()

    def durability_sub(self, value):
        item = self.hotbar.get_focuse_slot().item
        info = item.info
        if info.durability != None:
            info.durability -= value
            item.on_change_item()
            if info.durability < 0:
                self.sound_manager.play("broken")
                item.sub_item(1)

    def speed_manager(self):
        if self.bow_arm.location.visible:
            return (2, 'bowWalk', self.walk_wait)
        elif pygame.key.get_mods() & pygame.KMOD_SHIFT and self.inventory.boots_slot.item.info.index == ItemIndex.BOOTS:
            return (5, 'running', self.running_wait)
        else:
            return (3, 'walk', self.walk_wait)

    def moving(self):
        if not self.bow_arm.location.visible and pygame.key.get_mods() & pygame.KMOD_SHIFT and self.inventory.boots_slot.item.info.index == ItemIndex.BOOTS:
            if (Input.get_key(K_a) or Input.get_key(K_d)) and self.running_effect_wait.run_periodic_task():
                index = 2
    
                if self.feet_type in is_grass_type:
                    index = 0
                elif self.feet_type in is_dirt_type:
                    index = 1
                elif self.feet_type in is_stone_type:
                    index = 2

                if self.ground_key == 3:
                    particle = PixelParticle("pice", self.physics.rect.midtop, Vector(-self.physics.velocity.x * 0.6 * random.random(), 3), "pixelParticles", index)
                    particle.instantiate()
    
        if Input.get_key(K_d) and not Input.get_key(K_a):
            limited_speed, animation_key, wait_task = self.speed_manager()
            self.image.set_flip(False)
            if self.physics.on_ground:
                if self.physics.velocity.x < limited_speed:
                    self.physics.add_force(Vector(2, 0))
                    self.change_animation(animation_key)
                if wait_task.run_periodic_task():
                    if self.feet_type in is_grass_type:
                        sound = random.choice(self.walk_grass)
                        sound.play()
                    if self.feet_type in is_stone_type:
                        sound = random.choice(self.walk_stone)
                        sound.play()
            else:
                if self.physics.velocity.x < (limited_speed - 1):
                    self.physics.add_force(Vector(1, 0))

        if Input.get_key(K_a) and not Input.get_key(K_d):
            limited_speed, animation_key, wait_task = self.speed_manager()
            self.image.set_flip(True)
            if self.physics.on_ground:
                if self.physics.velocity.x > -limited_speed:
                    self.physics.add_force(Vector(-2, 0))
                    self.change_animation(animation_key)
                if wait_task.run_periodic_task():
                    if self.feet_type in is_grass_type:
                        sound = random.choice(self.walk_grass)
                        sound.play()
                    if self.feet_type in is_stone_type:
                        sound = random.choice(self.walk_stone)
                        sound.play()
            else:
                if self.physics.velocity.x > -(limited_speed - 1):
                    self.physics.add_force(Vector(-1, 0))

        if Input.get_key_up(K_a) or Input.get_key_up(K_d) or (Input.get_key(K_a) and Input.get_key(K_d)):
            self.change_animation('bowIdle' if self.bow_arm.location.visible else 'idle')

        if Input.get_key_down(K_SPACE):
            if self.physics.on_ground:
                self.physics.add_force(Vector(0, 10)) 
            elif self.inventory.armor_slot.item.info.index == ItemIndex.WING:
                if not self.wing.use:
                    self.wing.use = True
                    self.wing.start_animation()

class BowArm(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation =    Animation(float('inf'), self.image, sheet='playerBowIdle')
        charge_animation =  Animation(300,          self.image, sheet='playerBowCharge', once=True)

        idle_animation.change_image()

        self.animation_manager = AnimationManager(self, {
            'idle': idle_animation,
            'charge': charge_animation
        }, 'idle')
        
        self.components.append(self.animation_manager)

        self.diretion = Vector(1, 0)

    def update(self):
        if self.location.world_visible:
            pos = Manger.scene.camera(self.render_position)
            mus_pos = Vector(mouse.get_pos())
            self.diretion = (mus_pos - pos).normalize()
            self.diretion.y *= -1
            angle = Vector(0, 0).angle_to(self.diretion)
            self.location.rotation = angle
            self.location.parent.object.image.set_flip(angle > 90 or angle < -90)

