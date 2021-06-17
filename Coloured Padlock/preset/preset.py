import random
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.objects.base import objectFactory
from ev3sim.simulation.world import World
from ev3sim.visual.manager import ScreenObjectManager

class MovementInteractor(PygameGuiInteractor):

    GOAL_COLLISION_TYPE = 3
    BOT_COLLISION_TYPE = 4
    BALL_COLLISION_TYPE = 5

    COLOURS = ["#ff0000", "#00ff00", "#0000ff"]
    Y_POSITIONS = [35.83, 12.5, -10.83]
    X_POSITIONS = [-10, 22.5, 55]
    INDICATOR_POSITIONS = [-23.3, 9.2, 41.7]

    def startUp(self):
        super().startUp()
        self.buttons = []
        self.robot = self.robots[0]
        self.robot.shape.collision_type = self.BOT_COLLISION_TYPE
        self.setUpGoal()
        self.spawnPosition()

        handler = World.instance.space.add_collision_handler(self.BOT_COLLISION_TYPE, self.BALL_COLLISION_TYPE)
        saved_world_no = World.instance.spawn_no

        def handle_collide(arbiter, space, data):
            if World.instance.spawn_no != saved_world_no:
                return
            a, b = arbiter.shapes
            if not hasattr(a, "movement_index"):
                a, b = b, a
            self.collect(*a.movement_index)
            return False

        handler.begin = handle_collide

        handler_2 = World.instance.space.add_collision_handler(self.GOAL_COLLISION_TYPE, self.BOT_COLLISION_TYPE)

        def handle_collide(arbiter, space, data):
            if World.instance.spawn_no != saved_world_no:
                return
            a, b = arbiter.shapes
            self.accepted()
            return False

        handler_2.begin = handle_collide

    def setBotPos(self):
        self.robot.body.position = [-50, 35]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle
        self.robot.body.angular_velocity = 0

    def spawnPosition(self):
        self.setBotPos()

        for but in self.buttons:
            World.instance.unregisterObject(but)
        self.buttons = []

        self.states = [random.randint(0, 2) for _ in range(3)]
        for x in range(3):
            c_key = f"movement_bot_colour-{x}"
            o_key = f"movement_bot-button-{x}"
            if c_key in ScreenObjectManager.instance.objects:
                ScreenObjectManager.instance.unregisterVisual(c_key)
            if o_key in ScreenObjectManager.instance.objects:
                ScreenObjectManager.instance.unregisterVisual(o_key)
            for y in range(3):
                if o_key+f"-{y}" in ScreenObjectManager.instance.objects:
                    ScreenObjectManager.instance.unregisterVisual(o_key+f"-{y}")
            c_obj = visualFactory(
                name="Rectangle",
                width=5,
                height=5,
                position=[
                    self.INDICATOR_POSITIONS[x], -35,
                ],
                fill=self.COLOURS[self.states[x]],
                sensorVisible=True,
                stroke_width=0,
                zPos=0.5,
            )
            ScreenObjectManager.instance.registerVisual(c_obj, c_key)
            buttonLight = visualFactory(
                name="Circle",
                radius=0.5,
                fill=self.COLOURS[self.states[x]],
                position=[
                    self.X_POSITIONS[x],
                    self.Y_POSITIONS[self.states[x]],
                ],
                stroke_width=0,
                zPos=0.6,
            )
            ScreenObjectManager.instance.registerVisual(buttonLight, o_key)
            for y in range(3):
                button = objectFactory(
                    visual={
                        "name": "Rectangle",
                        "width": 5,
                        "height": 5,
                        "fill": "#666666",
                        "stroke_width": 0.1,
                        "stroke": "#ffffff",
                        "zPos": 0.5,
                    },
                    position=[
                        self.X_POSITIONS[x],
                        self.Y_POSITIONS[y],
                    ],
                    physics=True,
                    key=o_key+f"-{y}"
                )
                button.shape.sensor = True
                button.shape.collision_type = self.BALL_COLLISION_TYPE
                button.shape.movement_index = (x, y)
                self.buttons.append(button)
                World.instance.registerObject(button)
                ScreenObjectManager.instance.registerObject(button, o_key+f"-{y}")


        self.restartBots()

    def setUpGoal(self):
        self.goal = objectFactory(
            **{
                "visual": {"name": "Rectangle", "width": 5, "height": 20, "fill": "#00ff00", "stroke_width": 0.1, "zPos": 3},
                "physics": True,
                "key": "target",
                "position": [57.5, -35]
            }
        )
        self.goal.shape.sensor = True
        self.goal.shape.collision_type = self.GOAL_COLLISION_TYPE
        World.instance.registerObject(self.goal)
        ScreenObjectManager.instance.registerObject(self.goal, "target")

    def restartBots(self):
        super().restartBots()
        ScriptLoader.instance.object_map["positionText"].text = "Start..."
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

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self._size[0] - button_right, self._size[1] / 2 - button_size[1] / 2, *button_size), 
            text="Respawn",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"respawn-button", "preset-button")
        )
        self.addButtonEvent("respawn-button", self.spawnPosition)
        self._all_objs.append(reset_but)

    def collect(self, x, y):
        if y == self.states[x]:
            ScriptLoader.instance.object_map["positionText"].text = f"Passed Gate {x+1}!"
            amount = 4 + 2 * x
            ScriptLoader.instance.object_map["positionBG"].fill = f"#22{amount*11}22"
            self.collected[x] = True
        else:
            ScriptLoader.instance.object_map["positionText"].text = f"Incorrect Gate!"
            ScriptLoader.instance.object_map["positionBG"].fill = f"#ff2222"

    def accepted(self):
        for x in range(3):
            if not self.collected[x]:
                break
        else:
            ScriptLoader.instance.object_map["positionText"].text = "Win!"
            ScriptLoader.instance.object_map["positionBG"].fill = "#22aa22"
            return
        ScriptLoader.instance.object_map["positionText"].text = "Missed a Gate!"
        ScriptLoader.instance.object_map["positionBG"].fill = "#aa2222"
            
