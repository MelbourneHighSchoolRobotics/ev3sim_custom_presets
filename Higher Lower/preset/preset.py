import random
import pygame
import pygame_gui
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT

class HigherInteractor(PygameGuiInteractor):

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
        show_answer = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_right - button_size[0], button_top + button_size[1] * 1.5, *button_size),
            text="Show Answer", 
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"show-button", "preset-button")
        )
        self.addButtonEvent("show-button", self.showAnswer)
        self._all_objs.append(show_answer)

    def restart(self):
        self.setMood("neutral")
        self.restartBots()
        # Choose a random number.
        self.chosen = random.randint(1, 100)
        ScriptLoader.instance.postInput(str(self.chosen))
        ScriptLoader.instance.object_map["answer_output"].text = "???"

    def showAnswer(self):
        ScriptLoader.instance.object_map["answer_output"].text = str(self.chosen)

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if "higher" in m.lower():
                self.setMood("higher")
            elif "lower" in m.lower():
                self.setMood("lower")
            elif "correct" in m.lower():
                self.setMood("correct")
                ScriptLoader.instance.object_map["answer_output"].text = str(self.chosen)

    def setMood(self, mood):
        ScriptLoader.instance.object_map["rachel"].image_path = f"custom/Higher Lower/ui/rachel_{mood}.png"
