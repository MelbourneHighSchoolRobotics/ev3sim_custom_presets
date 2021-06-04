import pygame
import random
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.visual.utils import hsl_to_rgb, rgb_to_hex
from ev3sim.constants import EV3SIM_PRINT
import pygame_gui

class ColorInteractor(PygameGuiInteractor):
    
    COLORS = [
        ("Green", 95, 130, 0.75, 1, 0.3, 0.7),
        ("Red", 344, 372, 0.75, 1, 0.3, 0.6),
        ("Blue", 220, 245, 0.8, 1, 0.3, 0.55),
    ]
    
    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
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
        self.restartBots()
        self.actual_colors = [(c[0], self.randomColor(*c[1:])) for c in self.COLORS]
        random.shuffle(self.actual_colors)
        self.animation_time = 0
        self.recieved = 0

    def randomColor(self, minHue, maxHue, minSat, maxSat, minLight, maxLight):
        h = random.randint(minHue, maxHue) % 360
        s = minSat + random.random() * (maxSat - minSat)
        l = minLight + random.random() * (maxLight - minLight)
        r, g, b = hsl_to_rgb(h, s, l)
        return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if "red" in m.lower():
                self.recieved += 1
                ScriptLoader.instance.object_map["colorText"].text = f"{self.recieved}: Red!"
            elif "green" in m.lower():
                self.recieved += 1
                ScriptLoader.instance.object_map["colorText"].text = f"{self.recieved}: Green!"
            elif "blue" in m.lower():
                self.recieved += 1
                ScriptLoader.instance.object_map["colorText"].text = f"{self.recieved}: Blue!"

    def update(self, dt):
        super().update(dt)
        if self.animation_time is not None:
            new_time = self.animation_time + dt
            if self.animation_time <= 0 and new_time > 0:
                ScriptLoader.instance.object_map["strip"].fill = self.actual_colors[0][1]
                ScriptLoader.instance.object_map["colorText"].text = "Waiting..."
            if self.animation_time <= 2 and new_time > 2:
                ScriptLoader.instance.object_map["strip"].fill = self.actual_colors[1][1]
                ScriptLoader.instance.object_map["colorText"].text = "Waiting..."
            if self.animation_time <= 4 and new_time > 4:
                ScriptLoader.instance.object_map["strip"].fill = self.actual_colors[2][1]
                ScriptLoader.instance.object_map["colorText"].text = "Waiting..."
            if self.animation_time <= 6 and new_time > 6:
                new_time = None
            self.animation_time = new_time
