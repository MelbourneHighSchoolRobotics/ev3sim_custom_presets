from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
import random
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT

class ServiceInteractor(PygameGuiInteractor):

    PLAN_NAMES = [
        "Standard",
        "Premium",
        "Super",
    ]

    USER_NAMES = [
        "Alan Turing",
        "Ada Lovelace",
        "Charles Babbage",
        "Grace Hopper",
    ]

    COLOURS = [
        "#f94144",
        "#f8961e",
        "#f9c74f",
        "#90be6d",
        "#577590",
        "#277da1",
        "#9c6644",
        "#4d194d",
        "#e09f3e",
    ]

    animation_time = 0
    object_keys = []
    WAIT_TIME = 0.5

    NEUTRAL_BG = "#999999"
    GOOD_BG = "#44cc44"
    BAD_BG = "#cc4444"

    def startUp(self):
        super().startUp()
        self.restart()

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

        button_left = self._size[0] / 16
        button_top = self._size[1] / 16
        button_size = self._size[0] / 6, self._size[1] / 8
        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left, button_top, *button_size), 
            text="Restart", 
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"restart-button", "preset-button")
        )
        self.addButtonEvent("restart-button", self.restart)
        self._all_objs.append(reset_but)

        self.visible_text = pygame_gui.elements.UITextBox(
            html_text=self.cur_text if hasattr(self, "cur_text") else "",
            relative_rect=pygame.Rect(
                -2*self._size[0]/15 + self._size[0]/2,
                self._size[1] / 10,
                0.95 * self._size[0]/2 + 2*self._size[0]/15,
                self._size[1]*8.5/10,
            ),
            manager=self,
            object_id=pygame_gui.core.ObjectID("text_instructions", "instruction_text"),
        )
        self._all_objs.append(self.visible_text)

    def restart(self):
        # Figure out some actions to complete.
        # Step 1: Create some plans.
        self.shows = []
        self.prints = []
        self.expected = []
        self.expected_indicies = []
        self.cur_text = ""
        self.cur_colors = self.COLOURS[:]
        random.shuffle(self.cur_colors)
        n_plans = random.randint(2, 3)
        plan_start = random.randint(0, len(self.PLAN_NAMES)-1)
        plans = [self.PLAN_NAMES[(x+plan_start) % len(self.PLAN_NAMES)] for x in range(n_plans)]
        for x in range(n_plans):
            self.prints.append(f"Can you create a new plan called {plans[x]} please.")
            self.shows.append(f"Can you create a new plan called <font color=\"{self.cur_colors[x]}\">{plans[x]}</font> please.")
        # Step 2: Create some users.
        n_users = random.randint(2, 4)
        user_start = random.randint(0, len(self.USER_NAMES)-1)
        users = {
            f"u000{x}": {
                "full_name": self.USER_NAMES[(x + user_start) % len(self.USER_NAMES)],
                "plan": random.choice(plans),
                "color": self.cur_colors[x+n_plans],
            }
            for x in range(n_users)
        }
        for user_id in users:
            self.prints.append(f"We have a new user called {users[user_id]['full_name']} with user_id {user_id}. They want to join {users[user_id]['plan']}.")
            self.shows.append(f"We have a new user called {users[user_id]['full_name']} with user_id <font color=\"{users[user_id]['color']}\">{user_id}</font>. They want to join {users[user_id]['plan']}.")
        # Step 3: Starting changing stuff.
        n_extra_steps = random.randint(10,20)
        for x in range(n_extra_steps):
            if random.random() < 0.45:
                uid = random.choice(list(users.keys()))
                while True:
                    plan = random.choice(plans)
                    if plan != users[uid]["plan"]: break
                self.prints.append(f"{uid} wants to change their plan to {plan}.")
                self.shows.append(f"<font color=\"{users[uid]['color']}\">{uid}</font> wants to change their plan to <font color=\"{self.cur_colors[plans.index(plan)]}\">{plan}</font>.")
                users[uid]["plan"] = plan
            elif random.random() < 0.35/0.55:
                uid = random.choice(list(users.keys()))
                plan = random.choice(plans)
                self.prints.append(f"{uid} wants to know if they are still on {plan}.")
                self.shows.append(f"Q: <font color=\"{users[uid]['color']}\">{uid}</font> wants to know if they are still on <font color=\"{self.cur_colors[plans.index(plan)]}\">{plan}</font>.")
                self.expected_indicies.append(x + n_users + n_plans)
                if plan == users[uid]["plan"]:
                    self.expected.append("Yes they are")
                else:
                    self.expected.append(f"No they aren't. They are on {users[uid]['plan']} now.")
            else:
                plan = random.choice(plans)
                self.prints.append(f"How many people are currently on the {plan} plan?")
                self.shows.append(f"Q: How many people are currently on the <font color=\"{self.cur_colors[plans.index(plan)]}\">{plan}</font> plan?")
                n_users_on_plan = len([u for u in users.values() if u['plan'] == plan])
                self.expected_indicies.append(x + n_users + n_plans)
                self.expected.append(f"There are {n_users_on_plan} people on {plan}.")
        self.prints.append("That's all for today")
        self.shows.append("That's all for today")
        self.num_message = len(self.shows)
        self.given = []
        self.animation_time = 0
        for key in self.object_keys:
            ScreenObjectManager.instance.unregisterVisual(key)
        self.object_keys = []
        self.restartBots()

    def addResponse(self, message):
        # Handle if matches expected. Give a specific colour.
        self.given.append(message)
        if len(self.given) <= len(self.expected) and self.given[-1] == self.expected[len(self.given)-1]:
            col = self.GOOD_BG
        else:
            col = self.BAD_BG
        key = f"given-{len(self.given)}"
        text = visualFactory(**{
            "name": "Text",
            "hAlignment": "l",
            "vAlignment": "baseline",
            "text": self.given[-1],
            "font_style": "fonts/Poppins-Regular.ttf",
            "fill": col,
            "font_size": 20,
            "position": [-95, 50 - 9 * len(self.given)],
            "zPos": 5,
            "key": key,
        })
        self.object_keys.append(key)
        ScreenObjectManager.instance.registerVisual(text, key)

    def addMessage(self, message):
        self.cur_text = self.cur_text + "<br>" + message
        self.visible_text.html_text = self.cur_text
        self.visible_text.rebuild()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if m.startswith("Yes they ") or m.startswith("No they ") or m.startswith("There are "):
                self.addResponse(m)

    def update(self, dt):
        super().update(dt)
        if self.animation_time > 0:
            self.animation_time -= dt
        
        while self.animation_time <= 0 and len(self.shows) > 0:
            text = self.shows[0]
            self.shows = self.shows[1:]
            message = self.prints[0]
            self.prints = self.prints[1:]
            ScriptLoader.instance.postInput(message)

            self.addMessage(text)


            self.animation_time += self.WAIT_TIME



