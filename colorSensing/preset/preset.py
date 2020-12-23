import pygame
import random
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.visual.utils import hsl_to_rgb, rgb_to_hex
import pygame_gui

class ColorInteractor(PygameGuiInteractor):
    
    COLORS_1 = [
        ("Yellow", 55, 65, 0.9, 1, 0.45, 0.55),
        ("Green", 95, 130, 0.75, 1, 0.3, 0.7),
        ("Red", 344, 372, 0.75, 1, 0.3, 0.6),
        ("Blue", 220, 245, 0.8, 1, 0.3, 0.55),
    ]

    DRAWING_LIST = "COLORS_1"
    
    def startUp(self):
        self.setColor(*self.COLORS_1[1])
        super().startUp()
        self.robot = self.robots[0]

    def clearObjects(self):
        return super().clearObjects()

    def generateObjects(self):
        # Generate the left buttons
        generic_button_data = {
            "color-button": {
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
        self.ui_theme._load_element_colour_data_from_theme("colours", f"color-button", generic_button_data)
        self.ui_theme._load_element_font_data_from_theme("font", f"color-button", generic_button_data)
        self.ui_theme._load_element_misc_data_from_theme("misc", f"color-button", generic_button_data)
        self.ui_theme._load_fonts()

        self.currentColors = getattr(self, self.DRAWING_LIST)
        button_top_inc = self._size[1] / (len(self.currentColors) + 1)
        button_top_orig = button_top_inc / 4
        button_left = 3 * self._size[0] / 32
        button_size = self._size[0] / 8, button_top_inc / 2
        data = {}
        def click(i):
            if i == len(self.currentColors):
                i = random.randint(0, len(self.currentColors) - 1)
            self.setColor(*self.currentColors[i])
            self.restartBots()
        for i, entry in enumerate(self.currentColors + [("Random", 0, 0, 0, 0, 0.2, 0.2)]):
            # Create button
            but = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(button_left, button_top_orig + button_top_inc * i, *button_size), 
                text=entry[0], 
                manager=self,
                object_id=pygame_gui.core.ObjectID(f"color-button-{i}", "color-button")
            )
            self.addButtonEvent(f"color-button-{i}", click, i)
            self._all_objs.append(but)

            # Set colour.
            h = (entry[1] + entry[2]) // 2
            s = (entry[3] + entry[4]) / 2
            l = (entry[5] + entry[6]) / 2
            col = self.randomColor(h, h, s, s, l, l)

            data[f"color-button-{i}"] = {
                "colours": {
                    "normal_bg": col,
                    "hovered_bg": col,
                    "active_bg": col,
                }
            }
            self.ui_theme._load_element_colour_data_from_theme("colours", f"color-button-{i}", data)
            but.rebuild_from_changed_theme_data()
        
        print(1)
        # Create the reset button
        but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self._size[0] - button_size[0] - button_left, self._size[1]/2 - button_size[1]/2, *button_size), 
            text="Restart", 
            manager=self,
            object_id=pygame_gui.core.ObjectID("restart-button", "color-button")
        )
        self.addButtonEvent("restart-button", self.restartBots)
        self._all_objs.append(but)

        data["restart-button"] = {
            "colours": {
                "normal_bg": "#666666",
                "hovered_bg": "#666666",
                "active_bg": "#666666",
            }
        }
        self.ui_theme._load_element_colour_data_from_theme("colours", "restart-button", data)
        but.rebuild_from_changed_theme_data()

    def randomColor(self, minHue, maxHue, minSat, maxSat, minLight, maxLight):
        h = random.randint(minHue, maxHue) % 360
        s = minSat + random.random() * (maxSat - minSat)
        l = minLight + random.random() * (maxLight - minLight)
        r, g, b = hsl_to_rgb(h, s, l)
        return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))

    def setColor(self, cName, *args):
        r = self.randomColor(*args)
        ScriptLoader.instance.object_map["strip"].fill = r
        ScriptLoader.instance.object_map["colorText"].fill = r
        ScriptLoader.instance.object_map["colorText"].text = cName
