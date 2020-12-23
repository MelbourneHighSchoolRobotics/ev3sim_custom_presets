from ev3sim.objects.base import STATIC_CATEGORY
import pygame
import pymunk
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.simulation.world import World
import random
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import IInteractor
from ev3sim.visual.utils import hsl_to_rgb, rgb_to_hex, screenspace_to_worldspace

class ColorInteractor(IInteractor):
    
    COLORS_1 = [
        ("Yellow", 55, 65, 0.9, 1, 0.45, 0.55),
        ("Green", 95, 130, 0.75, 1, 0.3, 0.7),
        ("Red", 344, 372, 0.75, 1, 0.3, 0.6),
        ("Blue", 220, 245, 0.8, 1, 0.3, 0.55),
    ]

    
    def startUp(self):
        self.setColor(*self.COLORS_1[1])
        self.clearColorButtons()
        self.addColorButtons(self.COLORS_1)
        super().startUp()
        self.robot = self.robots[0]

    def clearColorButtons(self):
        # If we want multiple difficulties (likely).
        for key in ScriptLoader.instance.object_map:
            if key.startswith("color-button"):
                World.instance.unregisterObject(ScriptLoader.instance.object_map[key])
                ScreenObjectManager.instance.unregisterVisual(key)
                del ScriptLoader.instance.object_map[key]

    def addColorButtons(self, colorList):
        self.currentColors = colorList
        elems = []
        inc = 36 / (len(colorList) + 1)
        for i in range(len(colorList)):
            h = (colorList[i][1] + colorList[i][2]) // 2
            s = (colorList[i][3] + colorList[i][4]) / 2
            l = (colorList[i][5] + colorList[i][6]) / 2
            elems.append({
                "type": "object",
                "physics": True,
                "static": True,
                "visual": {
                    "name": "Rectangle",
                    "width": 6,
                    "height": 3,
                    "fill": self.randomColor(h, h, s, s, l, l),
                    "stroke_width": 0.1,
                    "stroke": "#ffffff",
                    "zPos": 0.3,
                },
                "key": f"color-button-{i}",
                "position": [-16, 18 - inc * (i+0.5)],
            })
            elems.append({
                "type": "visual",
                "name": "Text",
                "text": colorList[i][0],
                "font_style": "fonts/Poppins-Regular.ttf",
                "fill": "#ffffff",
                "zPos": 0.4,
                "key": f"color-button-{i}-text",
                "position": [-16, 18 - inc * (i+0.5)],
                "hAlignment": "m",
                "vAlignment": "m",
            })
        elems.append({
                "type": "object",
            "physics": True,
            "static": True,
            "visual": {
                "name": "Rectangle",
                "width": 6,
                "height": 3,
                "fill": "#444444",
                "stroke_width": 0.1,
                "stroke": "#ffffff",
                "zPos": 0.3,
            },
            "key": f"color-button-{len(colorList)}",
            "position": [-16, 18 - inc * (len(colorList)+0.5)],
        })
        elems.append({
            "type": "visual",
            "name": "Text",
            "text": "?",
            "font_style": "fonts/Poppins-Regular.ttf",
            "fill": "#ffffff",
            "zPos": 0.4,
            "key": f"color-button-{len(colorList)}-text",
            "position": [-16, 18 - inc * (len(colorList)+0.5)],
            "hAlignment": "m",
            "vAlignment": "m",
        })
        ScriptLoader.instance.loadElements(elems)

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

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_pos = screenspace_to_worldspace(event.pos)
            shapes = World.instance.space.point_query(
                [float(v) for v in m_pos], 0.0, pymunk.ShapeFilter(mask=STATIC_CATEGORY)
            )
            for shape in shapes:
                if shape.shape.obj.key.startswith("color-button"):
                    index = int(shape.shape.obj.key.split("-")[2])
                    if index == len(self.currentColors):
                        index = random.randint(0, len(self.currentColors)-1)
                    self.setColor(*self.currentColors[index])
                    self.restartBots()
                if shape.shape.obj.key == "restart-button":
                    self.restartBots()
