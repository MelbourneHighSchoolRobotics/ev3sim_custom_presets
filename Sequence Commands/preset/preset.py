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

    current_index = 0
    TARGETS = (4, 7)

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.robot.shape.collision_type = self.BOT_COLLISION_TYPE
        self.robot.shape.parent = self.robot
        self.setUpBall()
        self.spawnPosition()

    def setBotPos(self):
        self.robot.body.position = [-50, 35]
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def spawnPosition(self):
        self.setBotPos()
        n_targets = random.randint(*self.TARGETS)
        c_position = [-50, 35]
        c_dir = 0
        self.commands = []
        self.positions = []
        for _ in range(n_targets):
            choices = [
                [(c_dir - 1) % 4, "Left", None, None], 
                [c_dir, "Straight", None, None], 
                [(c_dir + 1) % 4, "Right", None, None],
            ]
            to_remove = []
            for i in range(len(choices)):
                d, s, pos, distance = choices[i]
                if d == 0:
                    r = 50 - c_position[0]
                    if r < 20:
                        to_remove.append(i)
                    else:
                        distance = random.randint(20, r)
                        pos = [c_position[0] + distance, c_position[1]]
                elif d == 1:
                    r = c_position[1] + 35
                    if r < 20:
                        to_remove.append(i)
                    else:
                        distance = random.randint(20, r)
                        pos = [c_position[0], c_position[1] - distance]
                elif d == 2:
                    r = c_position[0] + 50
                    if r < 20:
                        to_remove.append(i)
                    else:
                        distance = random.randint(20, r)
                        pos = [c_position[0] - distance, c_position[1]]
                elif d == 3:
                    r = 35 - c_position[1]
                    if r < 20:
                        to_remove.append(i)
                    else:
                        distance = random.randint(20, r)
                        pos = [c_position[0], c_position[1] + distance]
                choices[i] = [d, s, pos, distance]
            for i in to_remove[::-1]:
                del choices[i]
            c_dir, s, c_position, distance = random.choice(choices)
            self.commands.append((s, distance))
            self.positions.append(c_position)

        ScriptLoader.instance.object_map["positionText"].text = f"0/{n_targets} Targets..."

        self.current_index = 0
        self.ball_centre.body.position = self.positions[self.current_index]
        self.ball_centre.position = self.positions[self.current_index]
        self.restartBots()
        ScriptLoader.instance.postInput(str(len(self.commands)))
        for direction, distance in self.commands:
            ScriptLoader.instance.postInput(f"Move {direction} for {distance}")

    def setUpBall(self):
        self.ball_centre = objectFactory(
            **{
                "visual": {"name": "Image", "image_path": "custom/Square Dance/ui/flag.png", "scale": 1.3, "zPos": 3},
                "physics": True,
                "key": "target",
            }
        )
        self.ball_centre.shape.sensor = True
        self.ball_centre.shape.collision_type = self.BALL_COLLISION_TYPE
        self.ball_centre.shape.parent = self.ball_centre
        World.instance.registerObject(self.ball_centre)
        ScreenObjectManager.instance.registerObject(self.ball_centre, "target")

        handler = World.instance.space.add_collision_handler(self.BALL_COLLISION_TYPE, self.BOT_COLLISION_TYPE)
        saved_world_no = World.instance.spawn_no

        def handle_collide(arbiter, space, data):
            if World.instance.spawn_no != saved_world_no:
                return
            a, b = arbiter.shapes
            self.current_index += 1
            if self.current_index < len(self.positions):
                if b.collision_type == self.BALL_COLLISION_TYPE:
                    a, b = b, a
                a.parent.body.position = self.positions[self.current_index]
                a.parent.position = a.parent.body.position
            else:
                a.parent.body.position = [1000, 1000]
                a.parent.position = a.parent.body.position
            ScriptLoader.instance.object_map["positionText"].text = f"{self.current_index}/{len(self.positions)} Targets{'!' if self.current_index == len(self.positions) else '...'}"
            return False

        handler.begin = handle_collide

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

    def solved(self):
        pass 
