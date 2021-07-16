import random
from ev3sim.visual.objects import visualFactory
import pygame
import pygame_gui
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.utils import hex_to_pycolor, rgb_to_hex
from ev3sim.constants import EV3SIM_PRINT

class MovementInteractor(PygameGuiInteractor):

    MIDDLE_COORD = [-37.5, -12.5]
    GRID_SIZE = [100, 100]
    SQUARE_SIZE = 20

    COLORS = {k: hex_to_pycolor(v) for k, v in {
        "AliceBlue": "F0F8FF",
        "AntiqueWhite": "FAEBD7",
        "Aqua": "00FFFF",
        "Aquamarine": "7FFFD4",
        "Azure": "F0FFFF",
        "Beige": "F5F5DC",
        "Bisque": "FFE4C4",
        "Black": "000000",
        "BlanchedAlmond": "FFEBCD",
        "Blue": "0000FF",
        "BlueViolet": "8A2BE2",
        "Brown": "A52A2A",
        "BurlyWood": "DEB887",
        "CadetBlue": "5F9EA0",
        "Chartreuse": "7FFF00",
        "Chocolate": "D2691E",
        "Coral": "FF7F50",
        "CornflowerBlue": "6495ED",
        "Cornsilk": "FFF8DC",
        "Crimson": "DC143C",
        "Cyan": "00FFFF",
        "DarkBlue": "00008B",
        "DarkCyan": "008B8B",
        "DarkGoldenRod": "B8860B",
        "DarkGray": "A9A9A9",
        "DarkGrey": "A9A9A9",
        "DarkGreen": "006400",
        "DarkKhaki": "BDB76B",
        "DarkMagenta": "8B008B",
        "DarkOliveGreen": "556B2F",
        "DarkOrange": "FF8C00",
        "DarkOrchid": "9932CC",
        "DarkRed": "8B0000",
        "DarkSalmon": "E9967A",
        "DarkSeaGreen": "8FBC8F",
        "DarkSlateBlue": "483D8B",
        "DarkSlateGray": "2F4F4F",
        "DarkSlateGrey": "2F4F4F",
        "DarkTurquoise": "00CED1",
        "DarkViolet": "9400D3",
        "DeepPink": "FF1493",
        "DeepSkyBlue": "00BFFF",
        "DimGray": "696969",
        "DimGrey": "696969",
        "DodgerBlue": "1E90FF",
        "FireBrick": "B22222",
        "FloralWhite": "FFFAF0",
        "ForestGreen": "228B22",
        "Fuchsia": "FF00FF",
        "Gainsboro": "DCDCDC",
        "GhostWhite": "F8F8FF",
        "Gold": "FFD700",
        "GoldenRod": "DAA520",
        "Gray": "808080",
        "Grey": "808080",
        "Green": "008000",
        "GreenYellow": "ADFF2F",
        "HoneyDew": "F0FFF0",
        "HotPink": "FF69B4",
        "IndianRed": "CD5C5C",
        "Indigo": "4B0082",
        "Ivory": "FFFFF0",
        "Khaki": "F0E68C",
        "Lavender": "E6E6FA",
        "LavenderBlush": "FFF0F5",
        "LawnGreen": "7CFC00",
        "LemonChiffon": "FFFACD",
        "LightBlue": "ADD8E6",
        "LightCoral": "F08080",
        "LightCyan": "E0FFFF",
        "GoldenRodYellow": "FAFAD2",
        "LightGreen": "90EE90",
        "LightPink": "FFB6C1",
        "LightSalmon": "FFA07A",
        "LightSeaGreen": "20B2AA",
        "LightSkyBlue": "87CEFA",
        "LightSlateGray": "778899",
        "LightSlateGrey": "778899",
        "LightSteelBlue": "B0C4DE",
        "LightYellow": "FFFFE0",
        "Lime": "00FF00",
        "LimeGreen": "32CD32",
        "Linen": "FAF0E6",
        "Magenta": "FF00FF",
        "Maroon": "800000",
        "MediumAquaMarine": "66CDAA",
        "MediumBlue": "0000CD",
        "MediumOrchid": "BA55D3",
        "MediumPurple": "9370DB",
        "MediumSeaGreen": "3CB371",
        "MediumSlateBlue": "7B68EE",
        "MediumSpringGreen": "00FA9A",
        "MediumTurquoise": "48D1CC",
        "MediumVioletRed": "C71585",
        "MidnightBlue": "191970",
        "MintCream": "F5FFFA",
        "MistyRose": "FFE4E1",
        "Moccasin": "FFE4B5",
        "NavajoWhite": "FFDEAD",
        "Navy": "000080",
        "OldLace": "FDF5E6",
        "Olive": "808000",
        "OliveDrab": "6B8E23",
        "Orange": "FFA500",
        "OrangeRed": "FF4500",
        "Orchid": "DA70D6",
        "PaleGoldenRod": "EEE8AA",
        "PaleGreen": "98FB98",
        "PaleTurquoise": "AFEEEE",
        "PaleVioletRed": "DB7093",
        "PapayaWhip": "FFEFD5",
        "PeachPuff": "FFDAB9",
        "Peru": "CD853F",
        "Pink": "FFC0CB",
        "Plum": "DDA0DD",
        "PowderBlue": "B0E0E6",
        "Purple": "800080",
        "RebeccaPurple": "663399",
        "Red": "FF0000",
        "RosyBrown": "BC8F8F",
        "RoyalBlue": "4169E1",
        "SaddleBrown": "8B4513",
        "Salmon": "FA8072",
        "SandyBrown": "F4A460",
        "SeaGreen": "2E8B57",
        "SeaShell": "FFF5EE",
        "Sienna": "A0522D",
        "Silver": "C0C0C0",
        "SkyBlue": "87CEEB",
        "SlateBlue": "6A5ACD",
        "SlateGray": "708090",
        "SlateGrey": "708090",
        "Snow": "FFFAFA",
        "SpringGreen": "00FF7F",
        "SteelBlue": "4682B4",
        "Tan": "D2B48C",
        "Teal": "008080",
        "Thistle": "D8BFD8",
        "Tomato": "FF6347",
        "Turquoise": "40E0D0",
        "Violet": "EE82EE",
        "Wheat": "F5DEB3",
        "White": "FFFFFF",
        "WhiteSmoke": "F5F5F5",
        "Yellow": "FFFF00",
        "YellowGreen": "9ACD32",
    }.items()}

    keys = []

    def startUp(self):
        super().startUp()
        self.robot = self.robots[0]
        self.restart()

    def restart(self):
        if hasattr(self, "visible_text"):
            self.visible_text.kill()
        for key in self.keys:
            ScreenObjectManager.instance.unregisterVisual(key)
        self.keys = []
        self.white_done = False
        self.robot.body.position = self.MIDDLE_COORD
        self.robot.position = self.robot.body.position
        self.robot.body.angle = 0
        self.robot.rotation = self.robot.body.angle

        self.n_colors = random.randint(4, 7)
        self.chosen_colors = ["White", "Black"]
        while len(self.chosen_colors) < self.n_colors:
            col = random.choice(list(self.COLORS.keys()))
            if col in self.chosen_colors: continue
            self.chosen_colors.append(col)

        # Black at the back, white at the front.
        self.chosen_colors[1], self.chosen_colors[-1] = self.chosen_colors[-1], self.chosen_colors[1]
        # Generate positions.
        self.postitions = [(0, 0)]
        max_width = (self.GRID_SIZE[0] - self.SQUARE_SIZE) // (2 * self.SQUARE_SIZE)
        max_height = (self.GRID_SIZE[1] - self.SQUARE_SIZE) // (2 * self.SQUARE_SIZE)
        while len(self.postitions) < self.n_colors:
            x = random.randint(-max_width, max_width)
            y = random.randint(-max_height, max_height)
            if (x, y) in self.postitions: continue
            self.postitions.append((x, y))

        self.directions = []
        for i in range(len(self.postitions) - 1):
            x1, y1 = self.postitions[i]
            x2, y2 = self.postitions[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            string = ""
            if abs(dx) > abs(dy):
                if dx < 0:
                    string = string + "W" * (-dx)
                else:
                    string = string + "E" * dx
                if dy < 0:
                    string = string + "S" * (-dy)
                else:
                    string = string + "N" * dy
            else:
                if dy < 0:
                    string = string + "S" * (-dy)
                else:
                    string = string + "N" * dy
                if dx < 0:
                    string = string + "W" * (-dx)
                else:
                    string = string + "E" * dx
            self.directions.append(string)
        self.directions.append("END")


        self.createSquares()
        self.restartBots()
        self.postInstructions()

    def createSquares(self):
        for (x, y), col in zip(self.postitions, self.chosen_colors):
            key = f"square-{col}"
            square = visualFactory(**{
                "name": "Rectangle",
                "width": self.SQUARE_SIZE - 2,
                "height": self.SQUARE_SIZE - 2,
                "fill": rgb_to_hex(*self.COLORS[col]),
                "position": [
                    self.MIDDLE_COORD[0] + x * self.SQUARE_SIZE,
                    self.MIDDLE_COORD[1] + y * self.SQUARE_SIZE,
                ],
                "sensorVisible": True,
                "key": key,
                "zPos": 0.3,
            })
            ScreenObjectManager.instance.registerVisual(square, key)
            self.keys.append(key)

    def postInstructions(self):
        colander = list(zip(self.chosen_colors, self.directions))
        random.shuffle(colander)
        self.prints = [
            [f"{col} has r {self.COLORS[col][0]}, g {self.COLORS[col][1]}, b {self.COLORS[col][2]}", f"with directions {direction}"]
            for col, direction in colander
        ]
        self.words = [p for lines in self.prints for p in lines]
        self.words.insert(0, f"There are {self.n_colors} colours")
        self.show = [
            "<br>".join(lines)
            for lines in self.prints
        ]
        self.show.insert(0, f"There are {self.n_colors} colours")


        for word in self.words:
            ScriptLoader.instance.postInput(word)

        self.loadThemeData()
        self.visible_text = pygame_gui.elements.UITextBox(
            html_text="<br> <br>".join(self.show),
            relative_rect=pygame.Rect(
                1.7*self._size[0]/15 + self._size[0]/2,
                5 * self._size[1] / 20,
                0.95 * self._size[0]/2 - 1.7*self._size[0]/15,
                self._size[1]*6.5/10,
            ),
            manager=self,
            object_id=pygame_gui.core.ObjectID("text_instructions", "instruction_text"),
        )
        for i, (col, _d) in enumerate(colander):
            key = f"arrow-{i}"
            obj = visualFactory(**{
                "name": "Rectangle",
                "width": 5,
                "height": 5,
                "fill": self.COLORS[col],
                "stroke": "#000000",
                "stroke_width": 0.1,
                "zPos": 2,
                "position": [17.5, 24 - 12.6 * i],
                "key": key
            })
            ScreenObjectManager.instance.registerVisual(obj, key)
            self.keys.append(key)

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

        button_left = self._size[0] * 5 / 16 - button_size[0] / 2
        button_top = self._size[1] / 30 + (1/2) * 1.3 * button_size[1]

        reset_but = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_left, button_top, *button_size), 
            text="Reset",
            manager=self,
            object_id=pygame_gui.core.ObjectID(f"reset-button", "preset-button")
        )
        self.addButtonEvent("reset-button", self.restart)
        self._all_objs.append(reset_but)
