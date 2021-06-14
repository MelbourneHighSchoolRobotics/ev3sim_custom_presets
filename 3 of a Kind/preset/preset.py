import pygame
import pygame_gui
import random
import numpy as np
from ev3sim.constants import EV3SIM_PRINT
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.objects import visualFactory

class CardInteractor(PygameGuiInteractor):

    N_CARDS = (8, 15)
    ANIM_TOTAL = 1

    animation_time = 0

    def startUp(self):
        super().startUp()
        self.cards = []
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
        button_top = self._size[1] / 16
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
        for card in self.cards:
            self.destroyCard(card)
        # Spawn cards
        n_cards = random.randint(*self.N_CARDS)
        self.ending_data = [
            self.getCardPositionRotation(i, n_cards)
            for i in range(n_cards)
        ]
        self.createHand(n_cards)
        # Begin animation
        for i, card in enumerate(self.cards):
            card.begin_pos = (0, -90)
            card.end_pos = self.ending_data[i][0]
            card.begin_rot = 0
            card.end_rot = self.ending_data[i][1]
        self.animation_time = 0
        self.restartBots()
        # Send data
        ScriptLoader.instance.postInput(str(n_cards))
        for card in self.cards:
            ScriptLoader.instance.postInput(str(card.face_value))

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if "no" in m.lower() and "triples" in m.lower():
                # No triples - check this
                pass
            else:
                try:
                    a, b, c = list(map(int, m.split()))
                    assert 0 <= a < len(self.cards)
                    assert 0 <= b < len(self.cards)
                    assert 0 <= c < len(self.cards)
                    self.animation_time = 0
                    for card in self.cards:
                        card.begin_pos = card.end_pos
                        card.begin_rot = card.end_rot
                    self.cards[a].end_pos = (-40, 0)
                    self.cards[a].end_rot = 0
                    self.cards[b].end_pos = (0, 0)
                    self.cards[b].end_rot = 0
                    self.cards[c].end_pos = (40, 0)
                    self.cards[c].end_rot = 0
                except:
                    pass

    def createCard(self, suit, value, key):
        fname = f"custom/3 of a Kind/ui/card{suit}{value}.png"
        card = visualFactory(**{
            "name": "Image",
            "image_path": fname,
            "scale": 1.2,
            "zPos": 3,
        })
        card.face_value = value
        card.key = key
        ScreenObjectManager.instance.registerVisual(card, card.key)
        return card
    
    def destroyCard(self, card):
        ScreenObjectManager.instance.unregisterVisual(card.key)

    def createHand(self, n_cards):
        self.cards = [
            self.createCard(
                random.choice(["Clubs", "Diamonds", "Hearts", "Spades"]), 
                random.choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "A", "J", "K", "Q"]), 
                f"card-{i}"
            )
            for i in range(n_cards)
        ]

    def getCardPositionRotation(self, index, total):
        # Flip the positions for zfighting on our side.
        rotation = -30 * np.pi / 180 * (index - (total - 1) / 2) / ((total - 1) / 2)
        # Don't question it - the squaring sets height correctly.
        position = (10 * (index - (total - 1) / 2), -40 - 12*abs((index - (total - 1) / 2) / ((total - 1) / 2)) * abs((index - (total - 1) / 2) / ((total - 1) / 2)))
        return position, rotation

    def update(self, dt):
        super().update(dt)

        if self.animation_time < self.ANIM_TOTAL:
            self.animation_time += dt
            self.animation_time = min(self.ANIM_TOTAL, self.animation_time)

            t = self.animation_time / self.ANIM_TOTAL

            for card in self.cards:
                card.position = (
                    card.begin_pos[0] + (card.end_pos[0] - card.begin_pos[0]) * t,
                    card.begin_pos[1] + (card.end_pos[1] - card.begin_pos[1]) * t,
                )
                card.rotation = card.begin_rot + (card.end_rot - card.begin_rot) * t
