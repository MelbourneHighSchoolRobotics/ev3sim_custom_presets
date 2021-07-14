import random
from ev3sim.visual.objects import visualFactory
from ev3sim.visual.utils import hsl_to_rgb
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.manager import ScreenObjectManager
import numpy as np

class MovementInteractor(PygameGuiInteractor):

    BALL_COLLISION_TYPE = 3
    BOT_COLLISION_TYPE = 4

    TARGETS = (2, 5)

    PLACES = [
        "Home",
        "Store",
        "Restaurant",
        "Museum",
        "Hotel",
    ]

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.robot.shape.collision_type = self.BOT_COLLISION_TYPE
        self.robot.shape.parent = self.robot
        self.spawnPosition()

    def setBotPos(self):
        self.robot.body.position = [0, 0]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        for x in range(self.TARGETS[1]):
            if f"place-{x}" in ScreenObjectManager.instance.objects:
                ScreenObjectManager.instance.unregisterVisual(f"place-{x}")
        self.setBotPos()
        n_targets = random.randint(*self.TARGETS)
        offset = random.randint(0, 359)
        places = self.PLACES[:]
        random.shuffle(places)
        self.commands = []
        for x in range(n_targets):
            distance = random.randint(20, 40)
            bearing = int(360 * x / n_targets + offset) % 360
            self.commands.append((places[x], bearing, distance))
            obj = visualFactory(**{
                "name": "Image", 
                "image_path": f"custom/Locations Fixing/ui/{places[x]}.png", 
                "position": [distance * np.cos(bearing * np.pi / 180), distance * np.sin(bearing * np.pi / 180)],
                "fill": [255 * x for x in hsl_to_rgb(random.randint(0, 359), 1, 0.5)],
                "scale": 1.3, 
                "zPos": 3
            })
            ScreenObjectManager.instance.registerVisual(obj, f"place-{x}")

        self.restartBots()
        ScriptLoader.instance.postInput(str(n_targets))
        for s, b, d in self.commands:
            ScriptLoader.instance.postInput(f"{s} is {d} away at {b} degrees.")
        location = random.randint(0, n_targets-1)
        ScriptLoader.instance.postInput(f"Go to {self.commands[location][0]}")


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
            relative_rect=pygame.Rect(self._size[0] - button_right, self._size[1] / 2 - button_size[1] / 2, *button_size), 
            text="Respawn",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"respawn-button", "preset-button")
        )
        self.addButtonEvent("respawn-button", self.spawnPosition)
        self._all_objs.append(reset_but)

