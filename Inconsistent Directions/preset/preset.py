import math
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

    BALL_COLLISION_TYPE = 3
    BOT_COLLISION_TYPE = 4

    MIDDLE_COORD = [-125, -50]
    UNIT_DISTANCE = 18

    MAPPING = {
        "North": [0, 1],
        "South": [0, -1],
        "East": [-1, 0],
        "West": [1, 0],
    }

    OPPOSITES = {
        "North": "South",
        "South": "North",
        "East": "West",
        "West": "East",
    }

    ROTATION = {
        "North": 90,
        "South": 270,
        "East": 180,
        "West": 0,
    }

    keys = []

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.robot.shape.collision_type = self.BOT_COLLISION_TYPE
        self.robot.shape.parent = self.robot
        self.setUpBall()
        self.respawn("Easy")

    def respawn(self, difficulty):
        if difficulty == "Easy":
            n_actions = 5
            opposite_chance = 0.3
            reverse_chance = -0.0001
            ranged_opposite_chance = -0.0001
        elif difficulty == "Medium":
            n_actions = 10
            opposite_chance = 0.2
            reverse_chance = 0.2
            ranged_opposite_chance = -0.0001
        elif difficulty == "Hard":
            n_actions = 20
            opposite_chance = 0.05
            reverse_chance = 0.05
            ranged_opposite_chance = 0.1
        else:
            raise ValueError(f"Unexpected difficulty {difficulty}")
        self.actions = [random.choice(list(self.MAPPING.keys())) for _ in range(n_actions)]
        self.relative_ball_positions = []
        mih, mah, miv, mav = 0, 0, 0, 0
        ch, cv = 0, 0
        for action in self.actions:
            dx, dy = self.MAPPING[action]
            ch += dx
            cv += dy
            self.relative_ball_positions.append((ch, cv))
            mih = min(mih, ch)
            mah = max(mah, ch)
            miv = min(miv, cv)
            mav = max(mav, cv)
        self.bot_spawn_position = [
            self.MIDDLE_COORD[0] + self.UNIT_DISTANCE * (-mih-mah) / 2,
            self.MIDDLE_COORD[1] + self.UNIT_DISTANCE * (-miv-mav) / 2,
        ]
        self.ball_positions = [
            (
                self.bot_spawn_position[0] + x * self.UNIT_DISTANCE,
                self.bot_spawn_position[1] + y * self.UNIT_DISTANCE,
            )
            for x, y in self.relative_ball_positions
        ]
        # Decide on the directives.
        self.directives = [[idx, action] for idx, action in enumerate(self.actions)]
        random.shuffle(self.directives)
        inserted_directives = []
        for x in range(len(self.directives)):
            # Should there be a crazy directive at index x?
            if random.random() < opposite_chance:
                inserted_directives.append([x, "OPPOSITE", None])
            elif random.random() < reverse_chance / (1 - opposite_chance):
                inserted_directives.append([x, "REVERSE", None])
            elif random.random() < ranged_opposite_chance / (1 - opposite_chance - reverse_chance):
                length = random.randint(1, len(self.actions)-1)
                position = random.randint(0, len(self.actions) - length - 1)
                inserted_directives.append([x, "RANGED_OPPOSITE", (position, position + length)])
        for idx, action, arg in inserted_directives[::-1]:
            if action == "OPPOSITE":
                for x in range(idx+1):
                    self.directives[x][1] = self.OPPOSITES[self.directives[x][1]]
            elif action == "REVERSE":
                for x in range(idx+1):
                    self.directives[x][0] = len(self.actions) - self.directives[x][0] - 1
                    self.directives[x][1] = self.OPPOSITES[self.directives[x][1]]
            elif action == "RANGED_OPPOSITE":
                for x in range(idx+1):
                    if arg[0] <= self.directives[x][0] <= arg[1]:
                        self.directives[x][1] = self.OPPOSITES[self.directives[x][1]]
            self.directives.insert(idx+1, [action, arg])
        self.words = [f"Here's how you get home in {len(self.actions)} steps:"]
        self.show = self.words[:]
        for d0, d1 in self.directives:
            if d0 == "OPPOSITE":
                self.words.append("For everything I've said - I meant the opposite.")
                self.show.append("For everything I've said - I meant the <b>opposite</b>.")
            elif d0 == "REVERSE":
                self.words.append("For everything I've said - They were to go from home to here!")
                self.show.append("For everything I've said - They were to go <b>from</b> home <b>to</b> here!")
            elif d0 == "RANGED_OPPOSITE":
                self.words.append(f"For all steps from {d1[0]+1} to {d1[1]+1}, I meant the opposite.")
                self.show.append(f"For all steps from {d1[0]+1} to {d1[1]+1}, I meant the <b>opposite</b>.")
            else:
                self.words.append(f"Step number {d0+1} is to go {d1}.")
                self.show.append(f"Step number {d0+1} is to go <i>{d1}</i>.")
        self.words.append("And then you're home!")
        self.show.append("And then you're home!")
        for word in self.words:
            ScriptLoader.instance.postInput(word)
        if hasattr(self, "visible_text"):
            self.visible_text.kill()
        self.loadThemeData()
        self.visible_text = pygame_gui.elements.UITextBox(
            html_text="<br>".join(self.show),
            relative_rect=pygame.Rect(
                1.25*self._size[0]/15 + self._size[0]/2,
                self._size[1] / 20,
                self._size[0]/2 - 1.25*self._size[0]/15,
                self._size[1]*9/10,
            ),
            manager=self,
            object_id=pygame_gui.core.ObjectID("text_instructions", "instruction_text"),
        )
        for key in self.keys:
            ScreenObjectManager.instance.unregisterVisual(key)
        self.keys = []
        for i, action in enumerate(self.actions):
            key = f"arrow-{i}"
            obj = visualFactory(**{
                "name": "Image",
                "image_path": f"custom/Inconsistent Directions/ui/arrow.png",
                "hAlignment": "m",
                "vAlignment": "m",
                "zPos": 2,
                "scale": 0.025,
                "position": [40, 92 - 15 * i],
                "rotation": self.ROTATION[action] * math.pi / 180,
                "key": key
            })
            ScreenObjectManager.instance.registerVisual(obj, key)
            self.keys.append(key)
        self.reset()
    
    def reset(self):
        self.setBotPos()
        self.spawnBall()
        self.restartBots()

    def setBotPos(self):
        self.robot.body.position = self.bot_spawn_position
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

    def spawnBall(self):
        self.current_index = 0
        self.ball_centre.body.position = self.ball_positions[self.current_index]
        self.ball_centre.position = self.ball_positions[self.current_index]

    def setUpBall(self):
        self.ball_centre = objectFactory(
            **{
                "visual": {"name": "Image", "image_path": "custom/Square Dance/ui/flag.png", "scale": 0.6, "zPos": 3},
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
            if self.current_index < len(self.ball_positions):
                if b.collision_type == self.BALL_COLLISION_TYPE:
                    a, b = b, a
                a.parent.body.position = self.ball_positions[self.current_index]
                a.parent.position = a.parent.body.position
            else:
                # Hide me
                a.parent.body.position = [1000, 1000]
                a.parent.position = a.parent.body.position
            return False

        handler.begin = handle_collide

    def loadThemeData(self):
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
            },
            "instruction_text": {
                "colours": {
                    "normal_text": "#000000",
                    "normal_border": "#00000000",
                    "dark_bg": "#00000000",
                },
                "font": {
                    "name": "Poppins",
                    "size": "14",
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
                    "shadow_width": 0,
                    "border_width": 0,
                }
            }
        }
        self.ui_theme._load_element_colour_data_from_theme("colours", f"preset-button", generic_button_data)
        self.ui_theme._load_element_font_data_from_theme("font", f"preset-button", generic_button_data)
        self.ui_theme._load_element_misc_data_from_theme("misc", f"preset-button", generic_button_data)
        self.ui_theme._load_element_colour_data_from_theme("colours", f"instruction_text", generic_button_data)
        self.ui_theme._load_element_font_data_from_theme("font", f"instruction_text", generic_button_data)
        self.ui_theme._load_element_misc_data_from_theme("misc", f"instruction_text", generic_button_data)
        self.ui_theme._load_fonts()

    def generateObjects(self):
        self.loadThemeData()

        button_size = self._size[0] / 8, self._size[1] / 10

        button_left = [
            self._size[0] / 4 + ((index % 2) - 2/3) * 1.5 * button_size[0]
            for index in range(4)
        ]
        button_top = [
            self._size[1] / 30 + (index // 2) * 1.3 * button_size[1]
            for index in range(4)
        ]

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left[0], button_top[0], *button_size), 
            text="Reset",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"reset-button", "preset-button")
        )
        self.addButtonEvent("reset-button", self.reset)
        self._all_objs.append(reset_but)
        easy_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left[1], button_top[1], *button_size), 
            text="Easy",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"easy-button", "preset-button")
        )
        self.addButtonEvent("easy-button", lambda: self.respawn("Easy"))
        self._all_objs.append(easy_but)
        medium_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left[2], button_top[2], *button_size), 
            text="Medium",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"medium-button", "preset-button")
        )
        self.addButtonEvent("medium-button", lambda: self.respawn("Medium"))
        self._all_objs.append(medium_but)
        hard_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left[3], button_top[3], *button_size), 
            text="Hard",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"hard-button", "preset-button")
        )
        self.addButtonEvent("hard-button", lambda: self.respawn("Hard"))
        self._all_objs.append(hard_but)
