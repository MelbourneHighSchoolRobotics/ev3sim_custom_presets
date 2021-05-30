import random
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.objects.base import objectFactory
from ev3sim.simulation.world import World
from ev3sim.visual.manager import ScreenObjectManager

class MovementInteractor(PygameGuiInteractor):

    BALL_COLLISION_TYPE = 3
    BOT_COLLISION_TYPE = 4

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.robot.shape.collision_type = self.BOT_COLLISION_TYPE
        self.setUpBall()
        self.spawnPosition()

    def setBotPos(self):
        self.robot.body.position = [-50, 35]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        self.setBotPos()

        self.target_position = [
            int(-30 + 80 * random.random()),
            int(-40 + 60 * random.random()),
        ]
        self.ball_centre.body.position = self.target_position
        self.ball_centre.position = self.target_position
        self.restartBots()

    def setUpBall(self):
        self.ball_centre = objectFactory(
            **{
                "visual": {"name": "Image", "image_path": "custom/Search and Destroy/ui/flag.png", "scale": 1.3, "zPos": 3},
                "physics": True,
                "key": "target",
            }
        )
        self.ball_centre.shape.sensor = True
        self.ball_centre.shape.collision_type = self.BALL_COLLISION_TYPE
        World.instance.registerObject(self.ball_centre)
        ScreenObjectManager.instance.registerObject(self.ball_centre, "target")

        handler = World.instance.space.add_collision_handler(self.BALL_COLLISION_TYPE, self.BOT_COLLISION_TYPE)
        saved_world_no = World.instance.spawn_no

        def handle_collide(arbiter, space, data):
            if World.instance.spawn_no != saved_world_no:
                return
            a, b = arbiter.shapes
            self.accepted()
            return False

        handler.begin = handle_collide

    def restartBots(self):
        super().restartBots()
        ScriptLoader.instance.object_map["positionText"].text = "Waiting..."
        ScriptLoader.instance.object_map["positionBG"].fill = "#666666"
        ScriptLoader.instance.postInput(str(self.target_position[0]))
        ScriptLoader.instance.postInput(str(self.target_position[1]))

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

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self._size[0] - button_right, self._size[1] / 2 - button_size[1] / 2, *button_size), 
            text="Respawn",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"respawn-button", "preset-button")
        )
        self.addButtonEvent("respawn-button", self.spawnPosition)
        self._all_objs.append(reset_but)

    def accepted(self):
        ScriptLoader.instance.object_map["positionText"].text = "Win!"
        ScriptLoader.instance.object_map["positionBG"].fill = "#22aa22"
