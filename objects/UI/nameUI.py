from pygameHelper import *

from components.signs import change_name

class NameUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, path="./resource/ui/wyname.png", size=(3, 3), follow=True, collide=True)
        self.components.append(self.image)

        self.info = Text(name+"_text", layer, "text", True, [0 ,50], 0, name, 30, (0, 0, 0), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.info)
        self.info.text = "닉네임을 정하세요.\n(한글 가능)(5자 이내)"
        
        self.field = InputField(name+"_field", layer, "field", True, [-160, -15], 0, name, 40, (0, 0, 0), "./font/DungGeunMo.ttf", 0, "./resource/ui/name.png", 5, "Nickname...")
        self.childrens.append(self.field)
        self.field.input_event.add_lisner(lambda name: self.scene_change())

        self.button = Button(name+"_button", layer, "tag", True, [0, -100], 0, name, "./resource/inventory/signs/button.png")
        self.childrens.append(self.button)
        self.button.is_click.add_lisner(self.scene_change)

        self.button_text = Text(name+"_button_text", layer, "text", True, [0 ,0], 0, name+"_button", 30, (0, 0, 0), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.button_text)
        self.button_text.text = "확인"
        
        self.is_ready = False

    def scene_change(self):
        change_name(self.field.text)
        self.story.talk_start("start", self.question)

    def render(self, surface: Surface, camera):
        if self.is_ready:
            self.story.location.visible = True

    def question(self):
        self.button_visible(True)
        self.is_ready = True

    def button_click(self, value):
        if value:
            self.story.talk_start("tutorial", lambda: Game.stop("tutorial"))
        else:
            self.story.talk_start("skip", lambda: Game.stop("next"))
        self.button_visible(False)

    def button_visible(self, value):
        self.yes.location.visible = value
        self.no.location.visible = value

    def start(self):
        self.story = Manger.scene.get_object("story")

        self.yes = Button(self.story.name+"_button", self.story.layer, "tag", False, [-150, -100], 0, self.story.name, None, surface=(200, 50))
        self.yes.is_click.add_lisner(lambda: self.button_click(True))
        self.yes.instantiate()

        self.yes_text = Text(self.yes.name+"_text", self.story.layer, "text", True, [0 ,0], 0, self.yes.name, 50, (255, 255, 255), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.yes_text.text = "YES"
        self.yes_text.instantiate()
    
        self.no = Button(self.story.name+"_yes_button", self.story.layer, "tag", False, [150, -100], 0, self.story.name, None, surface=(200, 50))
        self.no.is_click.add_lisner(lambda: self.button_click(False))
        self.no.instantiate()

        self.no_text = Text(self.no.name+"_text", self.story.layer, "text", True, [0 ,0], 0, self.no.name, 50, (255, 255, 255), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.no_text.text = "NO"
        self.no_text.instantiate()