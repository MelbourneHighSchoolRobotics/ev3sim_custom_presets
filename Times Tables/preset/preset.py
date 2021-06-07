import random
import pygame
import pygame_gui
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.objects import Line, visualFactory
from ev3sim.constants import EV3SIM_PRINT

class TimestablesInteractor(PygameGuiInteractor):

    animation_time = 0

    WAIT_TIME = 0.03

    def startUp(self):
        super().startUp()
        self.restart()

    def generateObjects(self):
        generic_button_data = {
            "preset-button": {
                "colours": {
                    "normal_text": "#ffffff",
                    "hovered_text": "#ffffff",
                    "active_text": "#ffffff",
                    "normal_border": "#dddddd",
                    "hovered_border": "#eeeeee",
                    "active_border": "#ffffff",
                },
                "font": {
                    "name": "Poppins",
                    "size": "20",
                    "regular_resource": {
                        "package": "ev3sim.assets.fonts",
                        "resource": "Poppins-Regular.ttf"
                    },
                    "bold_resource": {
                        "package": "ev3sim.assets.fonts",
                        "resource": "Poppins-Bold.ttf"
                    },
                    "italic_resource": {
                        "package": "ev3sim.assets.fonts",
                        "resource": "Poppins-Italic.ttf"
                    },
                    "bold_italic_resource": {
                        "package": "ev3sim.assets.fonts",
                        "resource": "Poppins-BoldItalic.ttf"
                    },
                },
                "misc": {
                    "shape": "rounded_rectangle",
                    "shape_corner_radius": "6",
                    "border_width": "4",
                }
            }
        }
        self.ui_theme._load_element_colour_data_from_theme("colours", f"preset-button", generic_button_data)
        self.ui_theme._load_element_font_data_from_theme("font", f"preset-button", generic_button_data)
        self.ui_theme._load_element_misc_data_from_theme("misc", f"preset-button", generic_button_data)
        self.ui_theme._load_fonts()

        button_right = self._size[0] * 15 / 16
        button_top = self._size[1] / 16
        button_size = self._size[0] / 6, self._size[1] / 8
        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_right - button_size[0], button_top, *button_size), 
            text="Restart", 
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"restart-button", "preset-button")
        )
        self.addButtonEvent("restart-button", self.restart)
        self._all_objs.append(reset_but)

    def restart(self):
        keys = (
            [f"{x}-{y}-text" for x in range(13) for y in range(13)] + 
            [f"{x}-{y}-bg" for x in range(13) for y in range(13)] + 
            [f"{x}-row" for x in range(14)] +
            [f"{y}-col" for y in range(14)] +
            [f"{x}-row-title" for x in range(13)] +
            [f"{y}-col-title" for y in range(13)]
        )
        for key in keys:
            if key in ScreenObjectManager.instance.objects:
                ScreenObjectManager.instance.unregisterVisual(key)
        self.times_width = random.randint(1, 12)
        self.times_height = random.randint(1, 12)
        top_left = (-85, 65)
        bottom_right = (15, -45)
        s_width = bottom_right[0] - top_left[0]
        s_height = top_left[1] - bottom_right[1]
        for x in range(self.times_width):
            for y in range(self.times_height):
                text = visualFactory(**{
                    "name": "Text",
                    "text": "??",
                    "font_style": "fonts/Poppins-Regular.ttf",
                    "fill": "text_color",
                    "font_size": 24,
                    "position": [
                        top_left[0] + s_width * (x + 1.5) / (1 + self.times_width), 
                        top_left[1] - s_height * (y + 1.5) / (1 + self.times_height),
                    ],
                    "hAlignment": "m",
                    "vAlignment": "m",
                    "zPos": 4,
                    "key": f"{x}-{y}-text",
                })
                ScreenObjectManager.instance.registerVisual(text, f"{x}-{y}-text")
                bg = visualFactory(**{
                    "name": "Rectangle",
                    "width": s_width / (1 + self.times_width),
                    "height": s_height / (1 + self.times_height),
                    "position": [
                        top_left[0] + s_width * (x + 1.5) / (1 + self.times_width), 
                        top_left[1] - s_height * (y + 1.5) / (1 + self.times_height),
                    ],
                    "fill": "default_text_bg",
                    "zPos": 3,
                    "key": f"{x}-{y}-bg",
                })
                ScreenObjectManager.instance.registerVisual(bg, f"{x}-{y}-bg")
        for x in range(self.times_width+1):
            line = Line()
            line.initFromKwargs(
                start=[
                    top_left[0] + s_width * (x + 1) / (1 + self.times_width),
                    top_left[1],
                ],
                end=[
                    top_left[0] + s_width * (x + 1) / (1 + self.times_width),
                    bottom_right[1],
                ],
                fill="line_color",
                zPos=5,
            )
            ScreenObjectManager.instance.registerVisual(line, f"{x}-row")
        for y in range(self.times_height+1):
            line = Line()
            line.initFromKwargs(
                start=[
                    top_left[0],
                    top_left[1] - s_height * (y + 1) / (1 + self.times_height),
                ],
                end=[
                    bottom_right[0],
                    top_left[1] - s_height * (y + 1) / (1 + self.times_height),
                ],
                fill="line_color",
                zPos=5,
            )
            ScreenObjectManager.instance.registerVisual(line, f"{y}-col")
        for x in range(self.times_width):
            text = visualFactory(**{
                "name": "Text",
                "text": str(x+1),
                "font_style": "fonts/Poppins-Regular.ttf",
                "fill": "text_color",
                "font_size": 24,
                "position": [
                    top_left[0] + s_width * (x + 1.5) / (1 + self.times_width), 
                    top_left[1] - s_height * (0.5) / (1 + self.times_height),
                ],
                "hAlignment": "m",
                "vAlignment": "m",
                "zPos": 4,
                "key": f"{x}-row-title",
            })
            ScreenObjectManager.instance.registerVisual(text, f"{x}-row-title")
        for y in range(self.times_height):
            text = visualFactory(**{
                "name": "Text",
                "text": str(y+1),
                "font_style": "fonts/Poppins-Regular.ttf",
                "fill": "text_color",
                "font_size": 24,
                "position": [
                    top_left[0] + s_width * (0.5) / (1 + self.times_width), 
                    top_left[1] - s_height * (y + 1.5) / (1 + self.times_height),
                ],
                "hAlignment": "m",
                "vAlignment": "m",
                "zPos": 4,
                "key": f"{y}-col-title",
            })
            ScreenObjectManager.instance.registerVisual(text, f"{y}-col-title")

        self.animating_spots = []
        self.animation_time = 0

        self.solved = 0
        self.failed = False

        ScriptLoader.instance.postInput(str(self.times_height))
        ScriptLoader.instance.postInput(str(self.times_width))

        self.setMood("neutral")
        self.restartBots()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if "=" not in m:
                return False
            s = m.split("=")
            if "*" not in s[0] or len(s[0].split("*")) != 2:
                return False
            a, b = s[0].split("*")
            c = s[1]
            try:
                a, b, c = int(a.strip()), int(b.strip()), int(c.strip())
                if a < 1 or a > self.times_height or b < 1 or b > self.times_width:
                    return False
                self.animating_spots.append((a, b, c))
                # Handled
                return True
            except:
                return False

    def setMood(self, mood):
        ScriptLoader.instance.object_map["magician"].image_path = f"custom/Magician Trick/ui/magician_{mood}.png"

    def update(self, dt):
        super().update(dt)
        if self.animation_time > 0:
            self.animation_time -= dt
        while self.animation_time <= 0 and len(self.animating_spots) != 0:
            a, b, c = self.animating_spots[0]
            self.animating_spots = self.animating_spots[1:]
            ScreenObjectManager.instance.objects[f"{b-1}-{a-1}-text"].text = str(c)
            if a * b == c:
                ScreenObjectManager.instance.objects[f"{b-1}-{a-1}-bg"].fill = "correct_text_bg"
                self.solved += 1
                if not self.failed:
                    if self.solved - 1 < self.times_width * self.times_height / 2 <= self.solved:
                        self.setMood("happy")
                    if self.solved - 1 < self.times_width * self.times_height <= self.solved:
                        self.setMood("surprised")
            else:
                ScreenObjectManager.instance.objects[f"{b-1}-{a-1}-bg"].fill = "incorrect_text_bg"
                if not self.failed:
                    self.failed = True
                    self.setMood("sad")
            self.animation_time += self.WAIT_TIME
