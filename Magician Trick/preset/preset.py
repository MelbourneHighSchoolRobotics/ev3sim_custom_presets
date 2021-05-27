import pygame
import pygame_gui
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT

class MagicInteractor(PygameGuiInteractor):

    animation_time = None

    start_match = "Let's start with "
    other_match = lambda s, x: f"Multiplying by {x} gives "

    TIMING_FIRST = 0
    TIMING_SECOND = 1
    TIMING_THIRD = 2
    TIMING_FOURTH = 3

    NEUTRAL_BG = "#444444"
    GOOD_BG = "#44cc44"
    BAD_BG = "#cc4444"

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
        ScriptLoader.instance.object_map["start_output"].text = "???"
        ScriptLoader.instance.object_map["seven_output"].text = "???"
        ScriptLoader.instance.object_map["eleven_output"].text = "???"
        ScriptLoader.instance.object_map["thirteen_output"].text = "???"
        ScriptLoader.instance.object_map["start_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["seven_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["eleven_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["thirteen_box"].fill = self.NEUTRAL_BG
        self.start_num = None
        self.res = {}
        self.received_count = 0
        self.setMood("neutral")
        self.restartBots()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if m.startswith(self.start_match):
                self.start_num = m[len(self.start_match):-1]
                self.received_count += 1
            for d, n in [
                (7, "seven"),
                (11, "eleven"),
                (13, "thirteen"),
            ]:
                if m.startswith(self.other_match(d)):
                    self.res[d] = m[len(self.other_match(d)):-1]
                    self.received_count += 1
                    if self.received_count == 4:
                        self.startAnimation()

    def startAnimation(self):
        self.animation_time = 0

    def setMood(self, mood):
        ScriptLoader.instance.object_map["magician"].image_path = f"custom/Magician Trick/ui/magician_{mood}.png"

    def update(self, dt):
        super().update(dt)
        if self.animation_time is not None:
            new_time = self.animation_time + dt

            if self.animation_time <= self.TIMING_FIRST < new_time:
                ScriptLoader.instance.object_map["start_output"].text = str(self.start_num)
                try:
                    _x = int(self.start_num)
                    ScriptLoader.instance.object_map["start_box"].fill = self.GOOD_BG
                except:
                    ScriptLoader.instance.object_map["start_box"].fill = self.BAD_BG
                    self.setMood("sad")
            if self.animation_time <= self.TIMING_SECOND < new_time:
                ScriptLoader.instance.object_map["seven_output"].text = str(self.res[7])
                try:
                    if int(self.res[7]) != int(self.start_num) * 7:
                        ScriptLoader.instance.object_map["seven_box"].fill = self.BAD_BG
                        self.setMood("sad")
                    else:
                        ScriptLoader.instance.object_map["seven_box"].fill = self.GOOD_BG
                except:
                    ScriptLoader.instance.object_map["seven_box"].fill = self.BAD_BG
                    self.setMood("sad")
            if self.animation_time <= self.TIMING_THIRD < new_time:
                ScriptLoader.instance.object_map["eleven_output"].text = str(self.res[11])
                try:
                    if int(self.res[11]) != int(self.start_num) * 7 * 11:
                        ScriptLoader.instance.object_map["eleven_box"].fill = self.BAD_BG
                        self.setMood("sad")
                    else:
                        ScriptLoader.instance.object_map["eleven_box"].fill = self.GOOD_BG
                        self.setMood("happy")
                except:
                    ScriptLoader.instance.object_map["eleven_box"].fill = self.BAD_BG
                    self.setMood("sad")
            if self.animation_time <= self.TIMING_FOURTH < new_time:
                ScriptLoader.instance.object_map["thirteen_output"].text = str(self.res[13])
                try:
                    if int(self.res[13]) != int(self.start_num) * 7 * 11 * 13:
                        ScriptLoader.instance.object_map["thirteen_box"].fill = self.BAD_BG
                        self.setMood("sad")
                    else:
                        ScriptLoader.instance.object_map["thirteen_box"].fill = self.GOOD_BG
                        self.setMood("surprised")
                except:
                    ScriptLoader.instance.object_map["thirteen_box"].fill = self.BAD_BG
                    self.setMood("sad")
                self.animation_time = None
                return
            self.animation_time = new_time


