from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
import random
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.constants import EV3SIM_PRINT

class MonthInteractor(PygameGuiInteractor):

    animation_time = 0
    object_keys = []

    IN_BETWEEN_WAIT = 0.03
    SEPARATE_WAIT = 0.15

    NEUTRAL_BG = "#999999"
    GOOD_BG = "#44cc44"
    BAD_BG = "#cc4444"

    WEATHER_ICONS = {
        "Sunny": "wi-day-sunny.svg", 
        "Fog": "wi-fog.svg", 
        "Snow": "wi-day-snow.svg", 
        "Rain": "wi-day-rain.svg", 
        "Lightning": "wi-day-lightning.svg",
    }

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

        button_right = self._size[0] * 15 / 16
        button_top = 13 * self._size[1] / 16
        button_size = self._size[0] / 6, self._size[1] / 8
        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_right - button_size[0], button_top, *button_size), 
            text="Restart", 
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"restart-button", "preset-button")
        )
        self.addButtonEvent("restart-button", self.restart)
        self._all_objs.append(reset_but)

    def restart(self):
        self.number_of_days = random.randint(28, 31)
        self.weathers = [
            random.choice(list(self.WEATHER_ICONS.keys()))
            for _ in range(self.number_of_days)
        ]
        self.solutions = [
            self.weathers[1:4],
            self.weathers[-2:],
            self.weathers[4:12:7],
            self.weathers[-2:-5:-1],
        ]
        self.animation_time = 0
        self.animation_requests = [
            ("Start", i, w)
            for i, w in enumerate(self.weathers)
        ]
        self.message_counter = 0
        for key in self.object_keys:
            ScreenObjectManager.instance.unregisterVisual(key)
        self.object_keys = []
        self.restartBots()
        ScriptLoader.instance.postInput(self.number_of_days)
        for weather in self.weathers:
            ScriptLoader.instance.postInput(weather)

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            for key in m.split():
                if key not in self.WEATHER_ICONS.keys():
                    break
            else:
                for i, key in enumerate(m.split()):
                    self.animation_requests.append((self.message_counter, i, key))
                self.message_counter += 1

    def update(self, dt):
        super().update(dt)
        if self.animation_time > 0:
            self.animation_time -= dt
        
        while self.animation_time <= 0 and len(self.animation_requests) > 0:
            name, index, weather = self.animation_requests[0]
            self.animation_requests = self.animation_requests[1:]

            # Decide on position.
            if name == "Start":
                y_pos = 65 - (index // 16) * 16
                x_pos = -90 + (index % 16) * 12
                fill = self.NEUTRAL_BG
            else:
                y_pos = 20 - 25 * (name)
                x_pos = -90 + index * 12
                fill = self.BAD_BG
                if name < len(self.solutions):
                    if index < len(self.solutions[name]):
                        if self.solutions[name][index] == weather:
                            fill = self.GOOD_BG
                        else:
                            key3 = f"{name}-{index}-correction"
                            obj3 = visualFactory(**{
                                "name": "Image",
                                "image_path": f"custom/Days of the Month/ui/{self.WEATHER_ICONS[self.solutions[name][index]]}",
                                "hAlignment": "m",
                                "vAlignment": "m",
                                "zPos": 2,
                                "scale": 0.5,
                                "position": [x_pos, y_pos + 10],
                                "key": key3
                            })
                            self.object_keys.append(key3)
                            ScreenObjectManager.instance.registerVisual(obj3, key3)

            key1 = f"{name}-{index}"
            key2 = f"{name}-{index}-box"
            obj1 = visualFactory(**{
                "name": "Image",
                "image_path": f"custom/Days of the Month/ui/{self.WEATHER_ICONS[weather]}",
                "hAlignment": "m",
                "vAlignment": "m",
                "zPos": 2,
                "scale": 0.5,
                "position": [x_pos, y_pos],
                "key": key1
            })
            obj2 = visualFactory(**{
                "name": "Rectangle",
                "width": 10,
                "height": 10,
                "stroke": "#000000",
                "stroke_width": 0.4,
                "fill": fill,
                "zPos": 1,
                "position": [x_pos, y_pos],
                "key": key2,
            })

            self.object_keys.append(key1)
            self.object_keys.append(key2)
            ScreenObjectManager.instance.registerVisual(obj1, key1)
            ScreenObjectManager.instance.registerVisual(obj2, key2)

            if len(self.animation_requests) == 0 or self.animation_requests[0][0] != name:
                self.animation_time += self.SEPARATE_WAIT
            else:
                self.animation_time += self.IN_BETWEEN_WAIT



