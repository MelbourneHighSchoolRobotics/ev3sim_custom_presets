import pygame
import pygame_gui
import random
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor

class MovementInteractor(PygameGuiInteractor):

    BOT_SPAWN = [0, -15]
    BALL_SPAWN = [0, 15]
    BALL_RANDOMISER = 45

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.spawnPosition()

    def spawnPosition(self):
        self.robot.body.position = self.BOT_SPAWN[:]
        self.robot.position = self.robot.body.position
        self.robot.body.velocity = [0, 0]
        ScriptLoader.instance.object_map["IR_BALL"].body.position = [
            (random.random()-0.5) * self.BALL_RANDOMISER + self.BALL_SPAWN[0],
            self.BALL_SPAWN[1]
        ]
        ScriptLoader.instance.object_map["IR_BALL"].position = ScriptLoader.instance.object_map["IR_BALL"].body.position
        ScriptLoader.instance.object_map["IR_BALL"].body.velocity = [0, 0]
        self.restartBots()

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

        button_size = self._size[0] / 8, self._size[1] / 10

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self._size[0] / 2 - button_size[0] / 2, self._size[1] - 3 * button_size[1], *button_size), 
            text="Respawn",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"respawn-button", "preset-button")
        )
        self.addButtonEvent("respawn-button", self.spawnPosition)
        self._all_objs.append(reset_but)
