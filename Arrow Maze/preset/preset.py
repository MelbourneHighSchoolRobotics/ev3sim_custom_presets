import yaml
import math
from os.path import join
import pygame
import pygame_gui
from ev3sim.objects.base import objectFactory
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.file_helper import find_abs_directory

class MazeInteractor(PygameGuiInteractor):

    COLOURS = {
        "R": "#ff0000",
        "G": "#00ff00",
        "B": "#0000ff",
        "E": "#ffffff"
    }

    width = 20
    margin = 3
    offset = [2.5, 1.5]

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.arrows = []
        self.loadMap("maps/1.yaml")
        self.spawnPosition()

    def restartBots(self):
        super().restartBots()
        if hasattr(self, "grid"):
            ScriptLoader.instance.postInput(str(self.grid))

    def loadMap(self, map_path):
        # load map
        custom_dir = find_abs_directory("workspace/custom/")
        full_path = join(custom_dir, "Arrow Maze", map_path)
        with open(full_path, "r") as f:
            conf = yaml.safe_load(f)
        # Despawn old stuff
        for arrow in self.arrows:
            ScreenObjectManager.instance.unregisterVisual(arrow.key)
            for child in arrow.children:
                ScreenObjectManager.instance.unregisterVisual(child.key)
        self.arrows = []
        self.dimensions = conf["dimensions"]
        self.spawn = conf["spawn"]
        self.grid = conf["grid"]
        self.rotation = conf.get("rotation", 0) * math.pi / 180
        # Spawn colours
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                arrow_obj = {
                    "name": "Image",
                    "image_path": 'custom/Arrow Maze/ui/arrow.png',
                    "hAlignment": "m",
                    "vAlignment": "m",
                    "scale": (self.width - self.margin) / 200,
                    "zPos": 1,
                }
                children = [
                    {
                        "visual": arrow_obj,
                    }
                ]
                if self.grid[y][x] == "L":
                    children[0]["rotation"] = math.pi
                elif self.grid[y][x] == "R":
                    children[0]["rotation"] = 0
                elif self.grid[y][x] == "U":
                    children[0]["rotation"] = math.pi / 2
                elif self.grid[y][x] == "D":
                    children[0]["rotation"] = - math.pi / 2
                else:
                    children = []
                c_obj = objectFactory(
                    visual={
                        "name": "Rectangle",
                        "width": self.width - self.margin,
                        "height": self.width - self.margin,
                        "fill": "#ffffff",
                        "stroke_width": 0,
                        "zPos": 0.5
                    },
                    children=children,
                    key=f"sq-{x}-{y}",
                    position=[
                        self.width * (x-self.offset[0]), -self.width * (y-self.offset[1]),
                    ],
                )
                
                ScreenObjectManager.instance.registerObject(c_obj, c_obj.key)
                self.arrows.append(c_obj)

    def setBotPos(self):
        self.robot.body.angle = self.rotation
        self.robot.body.position = [self.width * (self.spawn[0]-self.offset[0]), -self.width * (self.spawn[1]-self.offset[1])]
        self.robot.position = self.robot.body.position
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        self.setBotPos()

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

        def event(x):
            self.loadMap(f"maps/{x}.yaml")
            self.setBotPos()
            self.restartBots()

        button_top_inc = self._size[1] / 5
        button_size = self._size[0] / 8, button_top_inc / 2
        for x in range(1, 3):
            but = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self._size[0] / 2 - 5 * button_size[0] + 3 * x * button_size[0], self._size[1] - button_size[1] * 2, *button_size), 
                text=f"Map {x}", 
                manager=self,
                object_id=pygame_gui.core.ObjectID(f"preset-button-{x}", "preset-button")
            )
            self.addButtonEvent(f"preset-button-{x}", event, x)
            self._all_objs.append(but)
