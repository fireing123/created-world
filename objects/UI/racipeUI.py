from pygameHelper import (
    UI,
    ImageObject,
    Vector,
    TimerTask,
    OnceTimerTask,
    Manger,
    Text
)

from collections import deque

class RacipeUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/ui/racipe_alarm.png", size=(6, 6), follow=True)
        self.components.append(self.image)

        self.image_ui = RacipeImageUI(name+"_image", layer, "image", True, [-50, 0], 0, name)
        self.childrens.append(self.image_ui)

        self.text = Text(name+"_text", layer, "text", True, [-20, 28], 0, name, 20, [0, 0, 0], "./font/DungGeunMo.ttf", 5)
        self.childrens.append(self.text)

        self.text.text = "레시피\n획득"

        self.queue = deque()
        self.visible = False
        self.wait = TimerTask(1000)
        self.hide = OnceTimerTask(3000)
        self.hide.once = True

        self.speed = 2

    def on_get_racipe(self, index):
        self.queue.append(index)

    def set_racipe(self, index):
        image = self.get_image(index)
        self.image_ui.image.set_orginal_image(image)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None

    def update(self):

        if self.visible:
            self.location.position = self.location.position.lerp(Vector(505, -360), min(1, Manger.delta_time * self.speed))
        else:
            self.location.position = self.location.position.lerp(Vector(505, -500), min(1, Manger.delta_time * self.speed))

        if self.queue:
            if self.visible:
                self.wait.reset()

            if self.wait.run_periodic_task():
                self.visible = True
                index = self.queue.popleft()
                self.set_racipe(index)
                self.hide.reset()

        if self.hide.run_periodic_task():
            self.wait.reset()
            self.visible = False

class RacipeImageUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, follow=True)
        self.components.append(self.image)