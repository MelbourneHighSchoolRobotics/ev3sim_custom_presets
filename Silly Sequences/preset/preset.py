import pygame
import pygame_gui
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT

class SequenceInteractor(PygameGuiInteractor):

    animation_time = 0

    WAIT_TIME = 0.08

    NEUTRAL_BG = "#444444"
    GOOD_BG = "#44cc44"
    BAD_BG = "#cc4444"

    SOLUTIONS = {
        "easy": [1, 8, 27, 64],
        "medium": [1, 9, 25, 36, 49],
        "hard": [2, 4, 8, 16, 32, 64, 128]
    }

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
        for diff in ["easy", "medium", "hard"]:
            for v in range(len(self.SOLUTIONS[diff])):
                ScriptLoader.instance.object_map[f"{diff}_{v}_text"].text = "???"
                ScriptLoader.instance.object_map[f"{diff}_{v}_box"].fill = self.NEUTRAL_BG

        self.animating_spots = []
        self.animation_time = 0
        self.mode = None
        self.easy_index = 0
        self.medium_index = 0
        self.hard_index = 0

        self.solved = 0
        self.failed = False

        self.restartBots()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            for mode in ["easy", "medium", "hard"]:
                if mode in m.lower():
                    self.mode = mode
                    return True
            if self.mode is not None:
                try:
                    if getattr(self, f"{self.mode}_index") == len(self.SOLUTIONS[self.mode]):
                        return False
                    if "=" in m:
                        m = m.split("=")[1].strip()
                    v = int(m)
                    setattr(self, f"{self.mode}_index", getattr(self, f"{self.mode}_index") + 1)
                    self.animating_spots.append((self.mode, getattr(self, f"{self.mode}_index") - 1, v))
                    return True
                except:
                    return False

    def update(self, dt):
        super().update(dt)
        if self.animation_time > 0:
            self.animation_time -= dt
        while self.animation_time <= 0 and len(self.animating_spots) != 0:
            mode, index, value = self.animating_spots[0]
            self.animating_spots = self.animating_spots[1:]
            
            ScriptLoader.instance.object_map[f"{mode}_{index}_text"].text = str(value)

            if value == self.SOLUTIONS[mode][index]:
                ScriptLoader.instance.object_map[f"{mode}_{index}_box"].fill = self.GOOD_BG
            else:
                ScriptLoader.instance.object_map[f"{mode}_{index}_box"].fill = self.BAD_BG

            self.animation_time += self.WAIT_TIME


