from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
import random
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT
from ev3sim.visual.manager import ScreenObjectManager

class MovementInteractor(PygameGuiInteractor):

    spawn_radius = 22
    N_SPAWNS = (2, 5)

    FILLS = [
        "#ff0000",
        "#00ff00",
        "#0000ff",
    ]

    width = 120
    height = 90

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.setUpAlien()
        self.reset()

    def reset(self):
        self.index = 0
        self.runs = random.randint(*self.N_SPAWNS)
        self.setBotPos()
        self.spawnAlien()
        self.restartBots()

    def setBotPos(self):
        self.robot.body.position = [0, 0]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def setUpAlien(self):
        self.alien_centre = ScriptLoader.instance.object_map["IR_BALL"]
        self.alien_radius = visualFactory(
            **{
                "name": "Circle",
                "radius": self.spawn_radius,
                "stroke_width": 0,
                "zPos": 2.5,
                "sensorVisible": True,
            }
        )
        ScreenObjectManager.instance.registerVisual(self.alien_radius, "alien-radius")

    def spawnAlien(self):
        while True:
            x = (-self.width / 2 + self.spawn_radius) + random.random() * (self.width - 2 * self.spawn_radius)
            y = (-self.height / 2 + self.spawn_radius) + random.random() * (self.height - 2 * self.spawn_radius)
            if (self.robot.position[0] - x) * (self.robot.position[0] - x) + (self.robot.position[1] - y) * (self.robot.position[1] - y) > (self.spawn_radius * 2) * (self.spawn_radius * 2):
                break
        self.alien_centre.body.position = [x, y]
        self.alien_centre.position = [x, y]
        self.alien_centre.body.velocity = [0, 0]
        self.alien_centre.body.angle = 0
        self.alien_centre.body.angular_velocity = 0
        self.alien_centre.rotation = 0
        self.alien_radius.position = [x, y]
        if self.index < self.runs:
            self.alien_radius.fill = random.choice(self.FILLS)
        else:
            self.alien_radius.fill = "#000000"

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
        self.addButtonEvent("respawn-button", self.reset)
        self._all_objs.append(reset_but)

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if "red" in m.lower():
                if self.alien_radius.fill[0] == 255:
                    # Good! Next respawn point.
                    self.index += 1
                    self.spawnAlien()
            elif "green" in m.lower():
                if self.alien_radius.fill[1] == 255:
                    # Good! Next respawn point.
                    self.index += 1
                    self.spawnAlien()
            elif "blue" in m.lower():
                if self.alien_radius.fill[2] == 255:
                    # Good! Next respawn point.
                    self.index += 1
                    self.spawnAlien()
