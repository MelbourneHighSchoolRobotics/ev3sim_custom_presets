import random
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.objects.base import objectFactory
from ev3sim.simulation.world import World
from ev3sim.visual.manager import ScreenObjectManager

class MovementInteractor(PygameGuiInteractor):

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.setUpGoal()
        self.spawnPosition()

    def setBotPos(self):
        self.robot.body.position = [self.alien.position[0] - 60 + 45 * random.random(), 0]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        self.alien.body.position = [50 * random.random(), 0]
        self.alien.position = self.alien.body.position
        self.distance_rect.position = [self.alien.position[0] - 35, 0]

        self.setBotPos()
        self.restartBots()

    def setUpGoal(self):
        self.alien = objectFactory(
            **{
                "visual": {"name": "Image", "image_path": "custom/Social Distancing/ui/ship.png", "scale": 1, "zPos": 3},
                "physics": True,
                "key": "target",
            }
        )
        World.instance.registerObject(self.alien)
        ScreenObjectManager.instance.registerObject(self.alien, "target")

        self.distance_rect = visualFactory(
            **{
                "name": "Rectangle",
                "width": 5,
                "height": 90,
                "fill": "#00ff00",
                "zPos": 3
            }
        )
        ScreenObjectManager.instance.registerVisual(self.distance_rect, "rect")

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

