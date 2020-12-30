import random
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.constants import EV3SIM_BOT_COMMAND
from ev3sim.code_helpers import CommandSystem
from ev3sim.objects.utils import magnitude_sq

class PlacementInteractor(PygameGuiInteractor):

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.spawnRandomPosition()

    def spawnRandomPosition(self):
        self.robot.body.position = [
            -55 + random.random() * 110,
            -40 + random.random() * 80,
        ]
        self.robot.position = self.robot.body.position
        self.restartBots()

    def restartBots(self):
        super().restartBots()
        ScriptLoader.instance.object_map["positionText"].text = "Waiting for response..."

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

        button_top_inc = self._size[1] / 5
        button_right = self._size[0] * 15 / 16
        button_size = self._size[0] / 8, button_top_inc / 2
        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_right - button_size[0], self._size[1] / 2 - button_size[1] / 2, *button_size), 
            text="Restart", 
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"restart-button", "preset-button")
        )
        self.addButtonEvent("restart-button", self.restartBots)
        self._all_objs.append(reset_but)

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self._size[0] - button_right, self._size[1] / 2 - button_size[1] / 2, *button_size), 
            text="Respawn",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"respawn-button", "preset-button")
        )
        self.addButtonEvent("respawn-button", self.spawnRandomPosition)
        self._all_objs.append(reset_but)

    def handleEvent(self, event):
        super().handleEvent(event)
        if (
            event.type == EV3SIM_BOT_COMMAND and 
            event.command_type == CommandSystem.TYPE_CUSTOM and
            isinstance(event.payload, str) and
            event.payload.startswith("Position: ")
        ):
            data = event.payload[10:]
            lines = data.split(", ")
            if len(lines) == 2 and lines[0].startswith("x: ") and lines[1].startswith("y: "):
                x = float(lines[0][3:])
                y = float(lines[1][3:])
                if magnitude_sq([x - self.robot.position[0], y - self.robot.position[1]]) < 20:
                    ScriptLoader.instance.object_map["positionText"].text = f"{x}, {y}" + " - Correct!"
                    ScriptLoader.instance.object_map["positionBG"].fill = "#22aa22"
                else:
                    ScriptLoader.instance.object_map["positionText"].text = f"{x}, {y}" + " - Wrong!"
                    ScriptLoader.instance.object_map["positionBG"].fill = "#aa2222"
