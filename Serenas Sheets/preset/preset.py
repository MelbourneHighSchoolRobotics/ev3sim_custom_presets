import pygame
import pygame_gui
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT, EV3SIM_MESSAGE_POSTED

class SheetInteractor(PygameGuiInteractor):

    animation_time = None

    area_match = "Area is "
    perimeter_match = "Double length perimeter is "
    total_match = "And so the cost is "

    TIMING_FIRST = 0
    TIMING_SECOND = 1
    TIMING_THIRD = 2

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
        self.received_count = 0
        self.posted_count = 0
        self.area_v = None
        self.perimeter_v = None
        self.cost_v = None
        self.width = None
        self.length = None
        ScriptLoader.instance.object_map["area_output"].text = "???"
        ScriptLoader.instance.object_map["area_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["perimeter_output"].text = "???"
        ScriptLoader.instance.object_map["perimeter_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["cost_output"].text = "???"
        ScriptLoader.instance.object_map["cost_box"].fill = self.NEUTRAL_BG
        ScriptLoader.instance.object_map["length_text"].text = ""
        ScriptLoader.instance.object_map["width_text"].text = ""
        self.setMood("neutral")
        self.restartBots()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            for match, name in [
                (self.area_match, "area"),
                (self.perimeter_match, "perimeter"),
                (self.total_match, "cost"),
            ]:
                if m.startswith(match):
                    setattr(self, f"{name}_v", m[len(match):-1])
                    self.received_count += 1
                    if self.received_count == 3:
                        self.startAnimation()
                    break

        if event.type == EV3SIM_MESSAGE_POSTED:
            if self.posted_count == 0:
                try:
                    self.length = int(event.message)
                    ScriptLoader.instance.object_map["length_text"].text = str(self.length)
                except:
                    pass
            elif self.posted_count == 1:
                try:
                    self.width = int(event.message)
                    ScriptLoader.instance.object_map["width_text"].text = str(self.width)
                except:
                    pass
            self.posted_count += 1

    def startAnimation(self):
        self.animation_time = 0

    def setMood(self, mood):
        ScriptLoader.instance.object_map["serena"].image_path = f"custom/Serenas Sheets/ui/serena_{mood}.png"

    def update(self, dt):
        super().update(dt)
        if self.animation_time is not None:
            new_time = self.animation_time + dt

            if self.animation_time <= self.TIMING_FIRST < new_time:
                ScriptLoader.instance.object_map["area_output"].text = self.area_v
                try:
                    if int(self.area_v) == self.width * self.length:
                        ScriptLoader.instance.object_map["area_box"].fill = self.GOOD_BG
                    else:
                        ScriptLoader.instance.object_map["area_box"].fill = self.BAD_BG
                        self.setMood("sad")    
                except:
                    ScriptLoader.instance.object_map["area_box"].fill = self.BAD_BG
                    self.setMood("sad")
            if self.animation_time <= self.TIMING_SECOND < new_time:
                ScriptLoader.instance.object_map["perimeter_output"].text = self.perimeter_v
                try:
                    if int(self.perimeter_v) == 2 * self.width + 4 * self.length:
                        ScriptLoader.instance.object_map["perimeter_box"].fill = self.GOOD_BG
                    else:
                        ScriptLoader.instance.object_map["perimeter_box"].fill = self.BAD_BG
                        self.setMood("sad")    
                except:
                    ScriptLoader.instance.object_map["perimeter_box"].fill = self.BAD_BG
                    self.setMood("sad")
            if self.animation_time <= self.TIMING_THIRD < new_time:
                ScriptLoader.instance.object_map["cost_output"].text = self.cost_v
                try:
                    if int(self.cost_v) == 2 * self.width + 4 * self.length + self.width * self.length:
                        ScriptLoader.instance.object_map["cost_box"].fill = self.GOOD_BG
                        self.setMood("happy")
                    else:
                        ScriptLoader.instance.object_map["cost_box"].fill = self.BAD_BG
                        self.setMood("sad")    
                except:
                    ScriptLoader.instance.object_map["cost_box"].fill = self.BAD_BG
                    self.setMood("sad")
                self.animation_time = None
                return

            self.animation_time = new_time


