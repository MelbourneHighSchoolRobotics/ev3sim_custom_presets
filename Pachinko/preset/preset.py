from ev3sim.visual.objects import visualFactory
import pygame
import pymunk
from ev3sim.constants import EV3SIM_PRINT
from ev3sim.objects.base import objectFactory, STATIC_CATEGORY
from ev3sim.simulation.interactor import PygameGuiInteractor
from ev3sim.simulation.loader import ScriptLoader
from ev3sim.simulation.world import World
from ev3sim.visual.manager import ScreenObjectManager
from ev3sim.visual.utils import screenspace_to_worldspace

class PachinkoInteractor(PygameGuiInteractor):

    N_POINTS = 30
    CUTOFFS = [5, 14, 19, 23]
    RESPONSES = ["Small", "Large", "Jumbo", "Medium", "Teensy"]

    SQUARE_COLLISION_TYPE = 3
    BALL_COLLISION_TYPE = 4

    bumper_lines = 2
    bumper_radius = 1.5
    double_spots = 35
    bumper_y_distance = 25

    def startUp(self):
        super().startUp()
        self.posted = False
        self.ball = objectFactory(
            **{
                "visual": {"name": "Circle", "radius": 2, "fill": "#000000", "zPos": 10},
                "physics": True,
                "key": "falling_ball",
                "position": [0, 130],
                "friction": 0.75
            }
        )
        self.ball.shape.collision_type = self.BALL_COLLISION_TYPE
        World.instance.registerObject(self.ball)
        ScreenObjectManager.instance.registerObject(self.ball, self.ball.key)

        ended_cutoffs = [0] + self.CUTOFFS + [self.N_POINTS]
        sq_width = 200 / self.N_POINTS * 0.8
        barricade_width = (200 - (sq_width * self.N_POINTS)) / self.N_POINTS
        for x in range(1, len(ended_cutoffs)):
            for y in range(ended_cutoffs[x-1], ended_cutoffs[x]):
                key = f"square_{y}"
                square = objectFactory(
                    **{
                        "visual": {"name": "Rectangle", "width": sq_width, "height": 10, "fill": f"area_{x}_color", "zPos": 3},
                        "physics": True,
                        "key": key,
                        "position": [
                            200 * (y + 0.5) / self.N_POINTS - 100,
                            -70,
                        ]
                    }
                )
                square.shape.sensor = True
                square.shape.collision_type = self.SQUARE_COLLISION_TYPE
                square.shape.sq_index = (x+1, y+1)
                World.instance.registerObject(square)
                ScreenObjectManager.instance.registerObject(square, key)
                num = visualFactory(
                    **{
                        "name": "Text",
                        "text": str(y+1),
                        "font_style": "fonts/Poppins-Regular.ttf",
                        "fill": "#000000",
                        "font_size": 24,
                        "position": [
                            200 * (y + 0.5) / self.N_POINTS - 100,
                            -70,
                        ],
                        "hAlignment": "m",
                        "vAlignment": "m",
                        "zPos": 5,
                        "key": f"text_{y}",
                    }
                )
                ScreenObjectManager.instance.registerVisual(num, f"text_{y}")
        for y in range(self.N_POINTS + 1):
            key = f"barricade_{y}"
            barricade = objectFactory(
                **{
                    "visual": {"name": "Rectangle", "width": barricade_width, "height": 15, "fill": "#000000", "zPos": 3},
                    "physics": True,
                    "static": True,
                    "key": key,
                    "position": [
                        y * 200 / self.N_POINTS - 100,
                        -67.5,
                    ]
                }
            )
            World.instance.registerObject(barricade)
            ScreenObjectManager.instance.registerObject(barricade, key)
        for x in range(self.bumper_lines):
            more = x % 2 == 0
            for y in range(self.double_spots // 2 + more):
                key = f"bumper_{x}_{y}"
                position = [
                    200 / (self.double_spots + 1) * ((2*y+1) if more else (2*y+2)) - 100,
                    -55 + (x+1) * self.bumper_y_distance,
                ]
                bumper = objectFactory(
                    **{
                        "visual": {"name": "Circle", "radius": self.bumper_radius, "fill": "#000000", "zPos": 3},
                        "physics": True,
                        "static": True,
                        "key": key,
                        "position": position,
                    }
                )
                World.instance.registerObject(bumper)
                ScreenObjectManager.instance.registerObject(bumper, key)
        ScriptLoader.instance.object_map["drop"].shape.sensor = True

        handler = World.instance.space.add_collision_handler(self.BALL_COLLISION_TYPE, self.SQUARE_COLLISION_TYPE)
        saved_world_no = World.instance.spawn_no

        def handle_collide(arbiter, space, data):
            if World.instance.spawn_no != saved_world_no:
                return
            a, b = arbiter.shapes
            if not hasattr(a, "sq_index"):
                a, b = b, a
            self.onFallen(a.sq_index)
            return False

        handler.begin = handle_collide

    def dropBall(self, position):
        self.restartBots()
        self.posted = False
        ScriptLoader.instance.object_map["prize_box"].fill = "#ffffff"
        ScriptLoader.instance.object_map["prize_output"].text = "???"
        self.ball.body.position = [x for x in position]
        self.ball.position = self.ball.body.position

    def tick(self, tick) -> bool:
        super().tick(tick)
        if self.ball is not None:
            self.ball.body.angle = 0
            self.ball.rotation = 0
            self.ball.apply_force([0, -1000])

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == EV3SIM_PRINT:
            m = event.message.rstrip()
            if m.endswith("Prize!"):
                try:
                    result = m.split()[0]
                    for i, response in enumerate(self.RESPONSES):
                        if response == result:
                            ScriptLoader.instance.object_map["prize_box"].fill = f"area_{i+1}_color"
                            ScriptLoader.instance.object_map["prize_output"].text = response
                    else:
                        pass
                except:
                    pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_pos = screenspace_to_worldspace(event.pos)
            shapes = World.instance.space.point_query(
                [float(v) for v in m_pos], 0.0, pymunk.ShapeFilter(mask=STATIC_CATEGORY)
            )
            if shapes:
                max_z = max(pq.shape.obj.clickZ for pq in shapes)
                shapes = [pq for pq in shapes if pq.shape.obj.clickZ == max_z]
            for shape in shapes:
                if shape.shape.obj.key == "drop":
                    self.dropBall(m_pos)
            
    def onFallen(self, sq_indicies):
        if self.posted:
            return
        ScriptLoader.instance.postInput(str(sq_indicies[1]))
        self.posted = True
