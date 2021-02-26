from ev3sim.code_helpers import CommandSystem
from ev3sim.constants import EV3SIM_BOT_COMMAND
import yaml
from os.path import join
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
from ev3sim.objects.base import objectFactory
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.world import World
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.file_helper import find_abs_directory

class MazeInteractor(PygameGuiInteractor):

    COLOURS = {
        "R": "#ff0000",
        "G": "#00ff00",
        "B": "#0000ff",
    }

    width = 20
    offset = [2, 1.5]

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.walls = []
        self.colours = []
        self.loadMap("maps/1.yaml")
        self.spawnPosition()

    def loadMap(self, map_path):
        # load map
        custom_dir = find_abs_directory("workspace/custom/")
        full_path = join(custom_dir, "colourMaze_2", map_path)
        with open(full_path, "r") as f:
            conf = yaml.safe_load(f)
        # Despawn old stuff
        for col in self.colours:
            ScreenObjectManager.instance.unregisterVisual(col.key)
        self.colours = []
        for wall in self.walls:
            ScreenObjectManager.instance.unregisterVisual(wall.key)
            World.instance.unregisterObject(wall)
        self.walls = []
        self.dimensions = conf["dimensions"]
        self.spawn = conf["spawn"]
        self.passcode = conf["passcode"]
        self.colour_map = conf["colours"]
        self.wall_map = conf["walls"]
        # Spawn colours
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                c_key = f"movement_bot_colour-{x}-{y}"
                c_obj = visualFactory(
                    name="Rectangle",
                    width=self.width,
                    height=self.width,
                    position=[
                        self.width * (x-self.offset[0]), -self.width * (y-self.offset[1]),
                    ],
                    fill=self.COLOURS[self.colour_map[y*self.dimensions[0]+x]],
                    sensorVisible=True,
                    stroke_width=0,
                    zPos=0.5,
                )
                c_obj.key = c_key
                ScreenObjectManager.instance.registerVisual(c_obj, c_key)
                self.colours.append(c_obj)
        # Spawn walls
        # First, vertical
        for x in range(self.dimensions[0] + 1):
            for y in range(self.dimensions[1]):
                if self.wall_map[(y+1)*self.dimensions[0] + y * (self.dimensions[0] + 1) + x] == "*":
                    wall_key = f"movement_bot_wall-vert-{x}-{y}"
                    wall_obj = objectFactory(
                        visual={
                            "name": "Rectangle",
                            "height": self.width,
                            "width": 2,
                            "stroke_width": 0,
                            "fill": "#000000",
                            "zPos": 0.7,
                        },
                        position=[
                            (x - 0.5 - self.offset[0]) * self.width,
                            -self.width * (y-self.offset[1]),
                        ],
                        rotation=0,
                        physics=True,
                        static=True,
                        key=wall_key
                    )
                    self.walls.append(wall_obj)
                    World.instance.registerObject(wall_obj)
                    ScreenObjectManager.instance.registerObject(wall_obj, wall_key)
        # Next, horizontal
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1] + 1):
                if self.wall_map[y*(2 * self.dimensions[0] + 1) + x] == "*":
                    wall_key = f"movement_bot_wall-horizontal-{x}-{y}"
                    wall_obj = objectFactory(
                        visual={
                            "name": "Rectangle",
                            "height": 2,
                            "width": self.width,
                            "stroke_width": 0,
                            "fill": "#000000",
                            "zPos": 0.7,
                        },
                        position=[
                            (x - self.offset[0]) * self.width,
                            -self.width * (y-self.offset[1]-0.5),
                        ],
                        rotation=0,
                        physics=True,
                        static=True,
                        key=wall_key
                    )
                    self.walls.append(wall_obj)
                    World.instance.registerObject(wall_obj)
                    ScreenObjectManager.instance.registerObject(wall_obj, wall_key)


    def setBotPos(self):
        self.robot.body.angle = 0
        self.robot.body.position = [self.width * (self.spawn[0]-self.offset[0]), -self.width * (self.spawn[1]-self.offset[1])]
        self.robot.position = self.robot.body.position
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        self.setBotPos()

        self.restartBots()

    def restartBots(self):
        super().restartBots()
        ScriptLoader.instance.object_map["positionText"].text = "Waiting..."
        ScriptLoader.instance.object_map["positionBG"].fill = "#666666"
        self.collected = [False]*3

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
        def event():
            self.setBotPos()
            self.restartBots()
        self.addButtonEvent("restart-button", event)
        self._all_objs.append(reset_but)
            
    def handleEvent(self, event):
        super().handleEvent(event)
        if (
            event.type == EV3SIM_BOT_COMMAND and 
            event.command_type == CommandSystem.TYPE_CUSTOM and
            isinstance(event.payload, str)
        ):
            if event.payload == self.passcode:
                ScriptLoader.instance.object_map["positionText"].text = event.payload + " - Correct!"
                ScriptLoader.instance.object_map["positionBG"].fill = "#22aa22"
            else:
                ScriptLoader.instance.object_map["positionText"].text = event.payload + " - Wrong!"
                ScriptLoader.instance.object_map["positionBG"].fill = "#aa2222"
